from copy import deepcopy
from datetime import datetime
from sqlite3 import connect

from Lesson_7_Mindlin.mindl_framework.exceptions import (ORMDeleteException,
                                                         ORMInsertException,
                                                         ORMRecordNotFound,
                                                         ORMUpdateException)

from .behavioral import FileWriter, Subject
from .db_api import DomainObject


class BaseUser:
    def __init__(self, name):
        self.name = name


class Buyer(BaseUser, DomainObject):
    def __init__(self, name):
        super().__init__(name)
        self.items = []


class Seller(BaseUser):
    def __init__(self, name):
        super().__init__(name)
        self.items = []


class UserFactory:
    types = {
        'buyer': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, _type, name):
        try:
            return cls.types[_type](name)
        except KeyError:
            raise KeyError(f'Тип пользователя <{_type}> не найден.')


class ItemPrototype:
    def clone(self):
        return deepcopy(self)


class Item(ItemPrototype, Subject):
    current_id = 1

    def __init__(self, title, category):
        super().__init__()
        self.id = Item.current_id
        self.title = title
        self.category = category
        self.buyers = []

        self.category.items.append(self)
        Item.current_id += 1

    def add_buyer(self, buyer):
        self.buyers.append(buyer)
        buyer.items.append(self)
        self.notify()


class DigitalItem(Item):
    pass


class PhysicalItem(Item):
    pass


class ItemFactory:
    types = {
        'digital': DigitalItem,
        'physical': PhysicalItem
    }

    @classmethod
    def create(cls, _type, title, category):
        try:
            return cls.types[_type](title, category)
        except KeyError:
            raise KeyError(f'Тип товара <{_type}> не найден.')


class Category:
    current_id = 1

    def __init__(self, name, category):
        self.id = Category.current_id
        self.name = name
        self.category = category
        self.items = []

        Category.current_id += 1

    def items_count(self):
        cnt = len(self.items)
        if self.category:
            cnt += self.category.items_count()
        return cnt


class Engine:
    def __init__(self):
        self.buyers = []
        self.sellers = []
        self.categories = []
        self.items = []

    def create_user(self, _type, name):
        user = UserFactory.create(_type=_type, name=name)
        if _type == 'buyer':
            self.buyers.append(user)
        else:
            self.sellers.append(user)
        return user

    def create_category(self, name, category=None):
        new_category = Category(name=name, category=category)
        self.categories.append(new_category)
        return new_category

    def create_item(self, _type, title, category):
        item = ItemFactory.create(_type=_type, title=title, category=category)
        self.items.append(item)
        return item

    def get_item(self, _id):
        for item in self.items:
            if item.id == _id:
                return item
        raise Exception(f'Товар с id <{_id}> не найдена.')

    def get_buyer(self, name):
        for buyer in self.buyers:
            if buyer.name == name:
                return buyer

    def get_category(self, _id):
        for category in self.categories:
            if category.id == _id:
                return category
        raise Exception(f'Категория с id <{_id}> не найдена.')


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, msg):
        dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        text = f'LOG [{dt}] ---> {msg}'
        self.writer.write(text)


connection = connect('db.sqlite')


class RecordNotFound:
    pass


class BuyerMapper:
    def __init__(self, _connection):
        self.connection = _connection
        self.cursor = _connection.cursor()
        self.tablename = 'buyer'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            _id, name = item
            buyer = Buyer(name=name)
            buyer.id = _id
            result.append(buyer)

        return result

    def get_by_id(self, _id):
        statement = f'SELECT * FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (_id,))
        result = self.cursor.fetchone()
        if result:
            return Buyer(*result)
        else:
            raise ORMRecordNotFound(f'Record id={_id} not found in table {self.tablename}.')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as error:
            raise ORMInsertException(error.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as error:
            raise ORMUpdateException(error.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id, ))
        try:
            self.connection.commit()
        except Exception as error:
            raise ORMDeleteException(error.args)


class SellerMaper(BuyerMapper):
    def __init__(self, _connection):
        super().__init__(_connection)
        self.tablename = 'seller'


class MapperRegistry:
    mappers = {
        'buyer': BuyerMapper,
        'seller': SellerMaper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Buyer):
            return BuyerMapper(connection)

    @classmethod
    def get_current_mapper(cls, _type):
        return cls.mappers[_type](connection)
