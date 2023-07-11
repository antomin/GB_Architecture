from .decos import debug
from .templator import render


class BaseView:
    template_name = 'template.html'
    template_folder = 'templates'
    extra_context = {}

    def get_context_data(self):
        return self.extra_context

    def render_template(self, request):
        context = {**request['context'], **self.get_context_data()}
        return '200 OK', render(self.template_name, folder=self.template_folder, context=context)

    def __call__(self, request):
        return self.render_template(request)


class ListView(BaseView):
    template_name = 'list.html'
    queryset = []
    context_objects_name = 'objects'

    def get_queryset(self):
        return self.queryset

    def get_context_data(self):
        queryset = self.get_queryset()
        context = {self.context_objects_name: queryset, **self.extra_context}
        return context


class CreateView(BaseView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request: dict) -> dict:
        return request.get('data', {})

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)

        return super().__call__(request)


class PageNotFound:
    def __call__(self, request):
        return '404 NOT FOUND', '<h1>Page not found</h1>'
