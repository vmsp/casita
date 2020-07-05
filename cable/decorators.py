import functools
import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

from cable import core
from cable.sites import site


def component_view(component):
    @functools.wraps(component)
    def view(request, *args, **kwargs):
        data = json.loads(request.body)
        state = data['state']
        fun = data.get('fun')

        template_name, context = component(state)
        if fun:
            context['fun']()

        html = render_to_string(template_name, context)
        return HttpResponse(
            core.add_attrs(html, reverse(view), context))

    view.csrf_exempt = True
    site.register(component, view)
    return view
