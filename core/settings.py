import os
from pathlib import Path

from core.configs.DB_config import DBConfig
from core.configs.django_config import DjangoConfig
from core.configs.smtp_config import SMTPClientConfig
from core.configs.allauth_config import AllAuthConfig
from core.configs.jwt_config import JWTConfig
from core.configs.rest_auth_config import RestAuthConfig

django_config = DjangoConfig()
db_config = DBConfig()
smtp_config = SMTPClientConfig()
allauth_config = AllAuthConfig()
jwt_config = JWTConfig()
rest_auth_config = RestAuthConfig()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = django_config.SECRET_KEY
DEBUG = django_config.IS_DEBUG
ALLOWED_HOSTS = django_config.ALLOWED_HOSTS

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'bootstrap5',

    # Local apps
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
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': db_config.DB_ENGINE,
        'NAME': db_config.DB_NAME,
        'USER': db_config.USER,
        'HOST': db_config.HOST,
        'PASSWORD': db_config.PASSWORD,
        'PORT': db_config.PORT,
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


LANGUAGE_CODE = django_config.LANGUAGE_CODE
TIME_ZONE = django_config.TIME_ZONE
USE_I18N = django_config.USE_I18N
USE_TZ = django_config.USE_TZ


STATIC_URL = django_config.STATIC_URL
DEFAULT_AUTO_FIELD = django_config.DEFAULT_AUTO_FIELD


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
}


SIMPLE_JWT = jwt_config.simple_jwt

REST_AUTH = rest_auth_config.rest_auth
REST_USE_JWT = rest_auth_config.USE_JWT
JWT_AUTH_COOKIE = rest_auth_config.JWT_AUTH_COOKIE

# Bootstrap5
BOOTSTRAP5 = {
    'include_jquery': True,
}

SITE_ID = allauth_config.SITE_ID
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = allauth_config.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS
ACCOUNT_EMAIL_REQUIRED = allauth_config.ACCOUNT_EMAIL_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = allauth_config.ACCOUNT_EMAIL_VERIFICATION
ACCOUNT_AUTHENTICATION_METHOD = allauth_config.ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_EMAIL_SUBJECT_PREFIX = allauth_config.ACCOUNT_EMAIL_SUBJECT_PREFIX
ACCOUNT_DEFAULT_HTTP_PROTOCOL = allauth_config.ACCOUNT_DEFAULT_HTTP_PROTOCOL
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = allauth_config.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = allauth_config.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
LOGIN_REDIRECT_URL = allauth_config.LOGIN_REDIRECT_URL
ACCOUNT_LOGOUT_REDIRECT_URL = allauth_config.ACCOUNT_LOGOUT_REDIRECT_URL
ACCOUNT_USERNAME_REQUIRED = allauth_config.ACCOUNT_USERNAME_REQUIRED
ACCOUNT_UNIQUE_EMAIL = allauth_config.ACCOUNT_UNIQUE_EMAIL

EMAIL_BACKEND = smtp_config.BACKEND
EMAIL_HOST = smtp_config.HOST
EMAIL_PORT = smtp_config.PORT
EMAIL_USE_TLS = smtp_config.USE_TLS
EMAIL_HOST_USER = smtp_config.HOST_USER
EMAIL_HOST_PASSWORD = smtp_config.PASSWORD
DEFAULT_FROM_EMAIL = smtp_config.HOST_USER
