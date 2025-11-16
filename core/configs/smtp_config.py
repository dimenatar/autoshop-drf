from decouple import config


class SMTPClientConfig:
    HOST_USER = config('EMAIL_HOST_USER')
    PASSWORD = config('EMAIL_PASSWORD')
    PORT = config('EMAIL_PORT', cast=int)
    USE_TLS = config('EMAIL_USE_TLS', cast=bool)
    HOST = config('EMAIL_HOST')
    BACKEND = config('EMAIL_BACKEND')
