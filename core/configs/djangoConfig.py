from django.apps import AppConfig
from decouple import config

class DjangoConfig(AppConfig):
    DJANGO_IS_DEBUG = config('DJANGO_IS_DEBUG', default=True, cast=bool)
    ALLOWED_HOSTS = list(config('ALLOWED_HOSTS').split(','))
    DJANGO_SECRET_KEY = config('DJANGO_SECRET_KEY')
    PG_DATA = config('PG_DATA')
    DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE')