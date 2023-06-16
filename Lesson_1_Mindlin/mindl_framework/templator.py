from os import path

from jinja2 import Template


def render(template_name, folder, context):
    template_path = path.join(folder, template_name)

    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())
        return template.render(**context)
