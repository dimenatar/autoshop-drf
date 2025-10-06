from django.apps import AppConfig
from decouple import config

class SMTPClientConfig(AppConfig):
    HOST_USER = config('EMAIL_HOST_USER')
    PASSWORD = config('EMAIL_PASSWORD')
    PORT = config('EMAIL_PORT')
    USE_TLS = config('EMAIL_USE_TLS')
    HOST = config('EMAIL_HOST')
    BACKEND = config('EMAIL_BACKEND')