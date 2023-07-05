from mindl_framework import AppRoute, render
from mindl_framework.views import BaseView, CreateView, ListView
from patterns.behavioral import EmailNotifier, FileWriter, SMSNotifier
from patterns.creation import Engine, Logger

db = Engine()
logger = Logger('views', FileWriter())
sms_notifier = SMSNotifier()
email_notifier = EmailNotifier()


@AppRoute('/')
class Index(BaseView):
    template_name = 'index.html'


@AppRoute('/about/')
class About(BaseView):
    template_name = 'about.html'


@AppRoute('/contact/')
class Contact(BaseView):
    template_name = 'contact.html'


@AppRoute('/categories/')
class CategoryList(ListView):
    template_name = 'list_category.html'
    queryset = db.categories
    context_objects_name = 'categories'


@AppRoute('/category/create/')
class CategoryCreate(CreateView):
    template_name = 'create_category.html'

    def create_object(self, data):
        name = data['name']
        db.create_category(name=name)


@AppRoute('/items/')
class ItemList(ListView):
    template_name = 'list_item.html'
    queryset = db.items
    context_objects_name = 'items'


@AppRoute('/create-item/')
class ItemCreate(CreateView):
    category_id = ''

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            _type = data['type']
            title = data['title']
            if self.category_id:
                category = db.get_category(self.category_id)
                item = db.create_item(_type=_type, title=title, category=category)

                item.observers += [sms_notifier, email_notifier]

                logger.log(f'New item {title} added.')
                return '200 OK', render(template_name='list_item.html', context={'items': category.items,
                                                                                 'category_name': category.name})
            logger.log(f'Error with adding new item')
        else:
            data = request['data']
            if data.get('cat_id'):
                self.category_id = int(data.get('cat_id'))
            return '200 OK', render(template_name='create_item.html')


@AppRoute('/copy-item/')
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


@AppRoute('/users/buyers/')
class BuyerList(ListView):
    template_name = 'list_user.html'
    queryset = db.buyers
    context_objects_name = 'users'


@AppRoute('/users/sellers/')
class BuyerList(ListView):
    template_name = 'list_user.html'
    queryset = db.sellers
    context_objects_name = 'users'


@AppRoute('/user/create/')
class CreateUser(CreateView):
    template_name = 'create_user.html'

    def create_object(self, data):
        _type = data['type']
        name = data['name']
        db.create_user(_type=_type, name=name)


@AppRoute('/item/add-to-buyer/')
class AddItemToBuyer(CreateView):
    template_name = 'add_item_to_user.html'
    extra_context = {
        'items': db.items,
        'buyers': db.buyers
    }

    def create_object(self, data):
        item = db.get_item(int(data['item_id']))
        buyer = db.get_buyer(data['buyer_name'])
        item.add_buyer(buyer)
