from copy import deepcopy
from datetime import datetime


class BaseUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Buyer(BaseUser):
    pass


class Seller(BaseUser):
    pass


class UserFactory:
    types = {
        'buyer': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, _type, username, password):
        try:
            return cls.types[_type](username, password)
        except KeyError:
            raise KeyError(f'Тип пользователя <{_type}> не найден.')


class ItemPrototype:
    def clone(self):
        return deepcopy(self)


class Item(ItemPrototype):
    current_id = 1

    def __init__(self, title, category):
        self.id = Item.current_id
        self.title = title
        self.category = category

        self.category.items.append(self)
        Item.current_id += 1


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

    @staticmethod
    def create_user(_type, username, password):
        return UserFactory.create(_type=_type, username=username, password=password)

    def create_category(self, name, category=None):
        new_category = Category(name=name, category=category)
        self.categories.append(new_category)
        return new_category

    def create_item(self, _type, title, category):
        new_item = ItemFactory.create(_type=_type, title=title, category=category)
        self.items.append(new_item)
        return new_item

    def get_item(self, _id):
        for item in self.items:
            if item.id == _id:
                return item
        raise Exception(f'Товар с id <{_id}> не найдена.')

    def get_category(self, _id):
        for category in self.categories:
            if category.id == _id:
                return category
        raise Exception(f'Категория с id <{_id}> не найдена.')


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Logger(metaclass=Singleton):
    @staticmethod
    def log(msg):
        dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f'LOG [{dt}] ---> {msg}')

