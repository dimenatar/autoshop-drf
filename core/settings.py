from pathlib import Path

from core.configs.DBConfig import DBConfig
from core.configs.djangoConfig import DjangoConfig

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = DjangoConfig.DJANGO_SECRET_KEY
DEBUG = DjangoConfig.DJANGO_IS_DEBUG
ALLOWED_HOSTS = DjangoConfig.ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autoshops',
    'cars',
    'discounts',
    'sales',
    'suppliers',
    'users',
    'available_cars',
    'offers',
    'core.configs.djangoConfig',
    'core.configs.mailConfig',
    'core.configs.DBConfig',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DBConfig.POSTGRES_NAME,
        'USER': DBConfig.POSTGRES_USER,
        'HOST': DBConfig.POSTGRES_HOST,
        'PASSWORD': DBConfig.POSTGRES_PASSWORD,
        'PORT': DBConfig.POSTGRES_PORT,
        'POSTGRES_DB': DBConfig.POSTGRES_DB,
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
