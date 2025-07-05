from django.apps import AppConfig
from decouple import config

class MailConfig(AppConfig):
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_PASSWORD = config('EMAIL_PASSWORD')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_BACKEND = config('EMAIL_BACKEND')