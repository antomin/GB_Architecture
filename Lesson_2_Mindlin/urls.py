from datetime import datetime
from platform import platform

from views import About, Index, Contact


def add_datetime_to_context(request):
    request['date'] = datetime.strftime(datetime.now(), '%d.%m.%Y')
    request['time'] = datetime.strftime(datetime.now(), '%H:%M')


def add_os_to_context(request):
    request['os'] = platform()


routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact()
}

fronts = [add_datetime_to_context, add_os_to_context]
