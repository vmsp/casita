from django.urls import path
from django.urls import reverse_lazy


class CableSite:
    """Encapsulates an instance of the Cable application, ready to be hooked
    into a URLconf.

    Component views are registered using the register() method and get_urls() is
    called afterwards to retrieve valid Django view functions and their paths.
    """
    def __init__(self, name='cable'):
        self.name = name
        self._components = []
        self._urls = {}

    def register(self, component, view):
        url = f'{view.__module__}/{view.__name__}/'
        self._components.append(
            (component, reverse_lazy(f'{self.name}:{url}')))
        self._urls[url] = view

    def get_urls(self):
        return [path(url, view, name=url) for url, view in self._urls.items()]

    @property
    def urls(self):
        return self.get_urls(), 'cable', self.name

    def get_component(self, name):
        for component, url in self._components:
            if component.__name__ == name:
                return component, url


site = CableSite()
