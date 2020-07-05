import django


class SetupDjango:
    def __init__(self):
        # Make sure DJANGO_SETTINGS_MODULE is set before calling this.
        django.setup()
