from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, context=None, folder='templates'):
    if context is None:
        context = {}
    env = Environment()
    env.loader = FileSystemLoader(folder)

    template = env.get_template(template_name)

    return template.render(**context)
