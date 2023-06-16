from mindl_framework import BaseView


class Index(BaseView):
    template_name = 'index.html'
    extra_context = {'title': 'Главная'}


class About(BaseView):
    template_name = 'about.html'
    extra_context = {'title': 'О нас'}
