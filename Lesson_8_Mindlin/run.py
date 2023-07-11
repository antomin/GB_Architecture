from wsgiref.simple_server import make_server

import views
from create_db import create_db
from mindl_framework import Application
from urls import fronts

app = Application(fronts=fronts)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Server started in port 8000...')
        httpd.serve_forever()
