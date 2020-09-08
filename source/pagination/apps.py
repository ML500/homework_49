from django.apps import AppConfig


# https://stackoverflow.com/a/47154840/3187374
# also:
# https://stackoverflow.com/a/37430196/3187374
class PaginationConfig(AppConfig):
    name = 'pagination'

    def ready(self):
        from django.conf import settings
        from . import defaults
        for key in dir(defaults):
            if key.isupper() and not hasattr(settings, key):
                setattr(settings, key, getattr(defaults, key))
