from wsgiref.simple_server import make_server

from urls import routes

from mindl_framework import Application
from urls import fronts

app = Application(routes=routes, fronts=fronts)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Server started in port 8000...')
        httpd.serve_forever()
