from .templator import render


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        path = path if path[-1] == '/' else path + '/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()

        request = {}
        for front in self.fronts:
            front(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]


class BaseView:
    template_name = None
    template_folder = 'templates'
    extra_context = {}

    def __call__(self, request):
        context = {**request, **self.extra_context}
        return '200 OK', render(self.template_name, folder=self.template_folder, context=context)


class PageNotFound:
    def __call__(self, request):
        return '404 NOT FOUND', '<h1>Page not found</h1>'
