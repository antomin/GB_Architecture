from .requests_utils import get_get_params, get_post_params
from .route import AppRoute
from .views import PageNotFound


class Application:
    def __init__(self, fronts):
        self.routes = AppRoute.routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        path = path if path[-1] == '/' else path + '/'

        request = {}
        data = {}

        method = environ['REQUEST_METHOD']

        request['method'] = method

        if method == 'POST':
            data = get_post_params(environ)

        if method == 'GET':
            data = get_get_params(environ)

        request['data'] = data

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()

        request['context'] = {}

        for front in self.fronts:
            front(request['context'])

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]
