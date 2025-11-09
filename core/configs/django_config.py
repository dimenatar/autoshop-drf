from decouple import config


class DjangoConfig:
    IS_DEBUG = config('DJANGO_IS_DEBUG', default=True, cast=bool)
    ALLOWED_HOSTS = list(config('ALLOWED_HOSTS').split(','))
    SECRET_KEY = config('DJANGO_SECRET_KEY')
    PG_DATA = config('PG_DATA')
    SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE')
    BASE_URL = config('BASE_URL')
    LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
    TIME_ZONE = config('TIME_ZONE', default='UTC')
    USE_I18N = config('USE_I18N', default=True, cast=bool)
    USE_TZ = config('USE_TZ', default=True, cast=bool)
    STATIC_URL = config('STATIC_URL', default='static/')
    DEFAULT_AUTO_FIELD = config('DEFAULT_AUTO_FIELD', default='django.db.models.BigAutoField')
