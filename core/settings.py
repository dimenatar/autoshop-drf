from pathlib import Path

from core.configs.DB_config import DBConfig
from core.configs.celery_config import CeleryConfig
from core.configs.django_config import DjangoConfig

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = DjangoConfig.SECRET_KEY
DEBUG = DjangoConfig.IS_DEBUG
ALLOWED_HOSTS = DjangoConfig.ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.configs.django_config',
    'core.configs.smtp_config',
    'core.configs.DB_config',
    'django_celery_results',
    'django_celery_beat',
    'autoshops',
    'cars',
    'discounts',
    'sales',
    'suppliers',
    'users',
    'available_cars',
    'offers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': DBConfig.DB_ENGINE,
        'NAME': DBConfig.DB_NAME,
        'USER': DBConfig.USER,
        'HOST': DBConfig.HOST,
        'PASSWORD': DBConfig.PASSWORD,
        'PORT': DBConfig.PORT,
        "OPTIONS": {
            "options": "-c client_encoding=utf8"
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_RESULT_BACKEND = CeleryConfig.CELERY_RESULT_BACKEND
CELERY_BROKER_URL = CeleryConfig.CELERY_BROKER_URL
CELERY_CACHE_BACKEND = CeleryConfig.CELERY_CACHE_BACKEND

CELERY_BEAT_SCHEDULE = CeleryConfig.CELERY_BEAT_SCHEDULE