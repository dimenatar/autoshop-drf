import os
from datetime import timedelta
from pathlib import Path

from core.configs.DB_config import DBConfig
from core.configs.django_config import DjangoConfig
from core.configs.smtp_config import SMTPClientConfig

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = DjangoConfig.SECRET_KEY
DEBUG = DjangoConfig.IS_DEBUG
ALLOWED_HOSTS = DjangoConfig.ALLOWED_HOSTS

INSTALLED_APPS = [
    #django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #configs
    'core.configs.django_config',
    'core.configs.smtp_config',
    'core.configs.DB_config',
    #tools
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'bootstrap5',
    #my apps
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
    'allauth.account.middleware.AccountMiddleware',
]
ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTH_USER_MODEL = "users.User"
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

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
# ВЫНЕСТИ ВСЕ В КОНФИГИ
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_COOKIE': 'autoshop-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'autoshop-refresh',
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'

BOOTSTRAP5 = {
    'include_jquery': True,
}

SITE_ID = 1

ACCOUNT_EMAIL_CONFIRMATION_URL = '/api/v1/auth/registration/account-confirm-email/{}/'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[AutoShop] '

EMAIL_BACKEND = SMTPClientConfig.BACKEND
EMAIL_HOST = SMTPClientConfig.HOST
EMAIL_PORT = SMTPClientConfig.PORT
EMAIL_USE_TLS = bool(SMTPClientConfig.USE_TLS)
EMAIL_HOST_USER = SMTPClientConfig.HOST_USER
EMAIL_HOST_PASSWORD = SMTPClientConfig.PASSWORD
DEFAULT_FROM_EMAIL = SMTPClientConfig.HOST_USER
