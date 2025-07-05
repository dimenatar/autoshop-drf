from django.apps import AppConfig
from decouple import config

class DBConfig(AppConfig):
    DB_ENGINE = config('DB_ENGINE')
    POSTGRES_NAME = config('POSTGRES_NAME')
    POSTGRES_USER =config('POSTGRES_USER')
    POSTGRES_HOST =config('POSTGRES_HOST')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_PORT = config('POSTGRES_PORT')
    POSTGRES_DB = config('POSTGRES_DB')