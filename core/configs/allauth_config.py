from decouple import config


class AllAuthConfig:
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = config('ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS', default=1, cast=int)
    ACCOUNT_EMAIL_REQUIRED = config('ACCOUNT_EMAIL_REQUIRED', default=True, cast=bool)
    ACCOUNT_EMAIL_VERIFICATION = config('ACCOUNT_EMAIL_VERIFICATION', default="mandatory")
    ACCOUNT_AUTHENTICATION_METHOD = config('ACCOUNT_AUTHENTICATION_METHOD', default='email')
    ACCOUNT_EMAIL_SUBJECT_PREFIX = config('ACCOUNT_EMAIL_SUBJECT_PREFIX', default="AutoShop - ")
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = config('ACCOUNT_DEFAULT_HTTP_PROTOCOL', default="http")
    SITE_ID = config('SITE_ID', default=1, cast=int)

    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = config(
        'ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL',
        default='/api/users/email-verified/'
    )
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = config(
        'ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL',
        default='/api/users/email-verified/'
    )
    LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/api/user/')
    ACCOUNT_LOGOUT_REDIRECT_URL = config('ACCOUNT_LOGOUT_REDIRECT_URL', default='/api/users/login/')

    ACCOUNT_USERNAME_REQUIRED = config('ACCOUNT_USERNAME_REQUIRED', default=False, cast=bool)
    ACCOUNT_UNIQUE_EMAIL = config('ACCOUNT_UNIQUE_EMAIL', default=True, cast=bool)
    SITE_NAME = config('SITE_NAME', default="AutoShop")
