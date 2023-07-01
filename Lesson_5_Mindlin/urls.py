from datetime import datetime
from platform import platform

from views import About, Contact, Index, CategoryList, CategoryCreate, ItemCreate, ItemList, ItemCopy


def add_datetime_to_context(request):
    request['date'] = datetime.strftime(datetime.now(), '%d.%m.%Y')
    request['time'] = datetime.strftime(datetime.now(), '%H:%M')


def add_os_to_context(request):
    request['os'] = platform()


# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/contact/': Contact(),
#     '/categories/': CategoryList(),
#     '/category/create/': CategoryCreate(),
#     '/items/': ItemList(),
#     '/create-item/': ItemCreate(),
#     '/copy-item/': ItemCopy()
# }

fronts = [
    add_datetime_to_context,
    add_os_to_context
]
