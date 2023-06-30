from patterns.creation import Engine, Logger
from mindl_framework import BaseView, render

db = Engine()
logger = Logger()


class Index(BaseView):
    template_name = 'index.html'
    extra_context = {'title': 'Главная'}


class About(BaseView):
    template_name = 'about.html'
    extra_context = {'title': 'О нас'}


class Contact(BaseView):
    template_name = 'contact.html'


class CategoryList(BaseView):
    categories = db.categories
    template_name = 'list_category.html'
    extra_context = {'categories': categories}


class CategoryCreate:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data.get('name')
            db.create_category(name=name)
            logger.log(f'New category {name} added.')
            return '200 OK', render(template_name='list_category.html', context={'categories': db.categories})


        else:
            context = {'title': 'Создать категорию'}
            return '200 OK', render(template_name='create_category.html', context=context)


class ItemList:
    def __call__(self, request):
        cat_id = request.get('data').get('cat_id')

        if not cat_id:
            items = db.items
            category_name = 'все'
        else:
            category = db.get_category(int(cat_id))
            category_name = category.name
            items = category.items

        return '200 OK', render(template_name='list_item.html', context={'items': items,
                                                                         'category_name': category_name})


class ItemCreate:
    category_id = ''

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            _type = data['type']
            title = data['title']
            if self.category_id:
                category = db.get_category(self.category_id)
                db.create_item(_type=_type, title=title, category=category)
                logger.log(f'New item {title} added.')
                return '200 OK', render(template_name='list_item.html', context={'items': category.items,
                                                                                 'category_name': category.name})
            logger.log(f'Error with adding new item')
        else:
            data = request['data']
            if data.get('cat_id'):
                self.category_id = int(data.get('cat_id'))
            return '200 OK', render(template_name='create_item.html')


class ItemCopy:
    def __call__(self, request):
        item_id = request.get('data').get('id')
        item = None
        if item_id:
            item = db.get_item(int(item_id))
        if item:
            new_item = item.clone()
            new_item.id += 1
            new_item.title = f'copy_{item.title}'
            db.items.append(new_item)

            context = {
                'items': db.items,
                'category_name': 'все'
            }
            logger.log(f'Item {item.title} copied.')

            return '200 OK', render(template_name='list_item.html', context=context)






