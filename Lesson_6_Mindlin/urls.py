from datetime import datetime
from platform import platform


def add_datetime_to_context(context):
    context['date'] = datetime.strftime(datetime.now(), '%d.%m.%Y')
    context['time'] = datetime.strftime(datetime.now(), '%H:%M')


def add_os_to_context(context):
    context['os'] = platform()


fronts = [
    add_datetime_to_context,
    add_os_to_context
]
