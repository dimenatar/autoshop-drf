from decouple import config
from django.apps import AppConfig


class DjangoConfig(AppConfig):
    IS_DEBUG = config('DJANGO_IS_DEBUG', default=True, cast=bool)
    ALLOWED_HOSTS = list(config('ALLOWED_HOSTS').split(','))
    SECRET_KEY = config('DJANGO_SECRET_KEY')
    PG_DATA = config('PG_DATA')
    SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE')
