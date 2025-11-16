from decouple import config


class DBConfig:
    DB_ENGINE = config('DB_ENGINE')
    DB_NAME = config('POSTGRES_NAME')
    USER = config('POSTGRES_USER')
    HOST = config('POSTGRES_HOST')
    PASSWORD = config('POSTGRES_PASSWORD')
    PORT = config('POSTGRES_PORT')
    DB = config('POSTGRES_DB')
