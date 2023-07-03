class AppRoute:
    routes = dict()

    def __init__(self, path):
        self.path = path

    def __call__(self, view):
        self.routes[self.path] = view()
