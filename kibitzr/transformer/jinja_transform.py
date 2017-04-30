from jinja2 import Template

from .utils import bake_parametrized


def jinja_transform(content, code, conf):
    context = {
        'conf': conf,
        'content': content,
        'lines': content.splitlines(),
    }
    template = Template(code)
    return True, template.render(context)


JINJA_REGISTRY = {
    'jinja': bake_parametrized(jinja_transform, pass_conf=True)
}
