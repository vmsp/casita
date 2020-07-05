from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CableConfig(AppConfig):
    name = 'cable'
    verbose_name = 'Cable'

    def ready(self):
        autodiscover_modules('components')
