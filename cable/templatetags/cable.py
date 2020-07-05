from django import template
from django.template.loader import render_to_string
from django.urls import reverse

from cable import core
from cable.sites import site

register = template.Library()


class ComponentNode(template.Node):
    def __init__(self, component_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._component_name = component_name

    def render(self, context):
        comp, url = site.get_component(self._component_name)
        template_name, context = comp({})
        html = render_to_string(template_name, context)
        return core.add_attrs(html, url)


@register.tag
def component(parser, token):
    try:
        tag_name, component_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f'{tag_name} tag requires exactly one argument')

    if (not (component_name[0] == component_name[-1]
             and component_name[0] in ('"', "'"))):
        raise template.TemplateSyntaxError(
            f'{tag_name} template argument should be in quotes')

    return ComponentNode(component_name[1:-1])
