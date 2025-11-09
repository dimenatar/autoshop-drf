from decouple import config
from datetime import timedelta


class JWTConfig:
    ACCESS_TOKEN_LIFETIME_MINUTES = config('ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)
    REFRESH_TOKEN_LIFETIME_DAYS = config('REFRESH_TOKEN_LIFETIME_DAYS', default=1, cast=int)
    ROTATE_REFRESH_TOKENS = config('ROTATE_REFRESH_TOKENS', default=False, cast=bool)
    BLACKLIST_AFTER_ROTATION = config('BLACKLIST_AFTER_ROTATION', default=True, cast=bool)
    ALGORITHM = config('JWT_ALGORITHM', default='HS256')
    SIGNING_KEY = config('DJANGO_SECRET_KEY')
    AUTH_HEADER_TYPES = config('JWT_AUTH_HEADER_TYPES', default='Bearer')
    AUTH_HEADER_NAME = config('JWT_AUTH_HEADER_NAME', default='HTTP_AUTHORIZATION')
    USER_ID_FIELD = config('JWT_USER_ID_FIELD', default='id')
    USER_ID_CLAIM = config('JWT_USER_ID_CLAIM', default='user_id')

    @property
    def simple_jwt(self) -> dict:
        return {
            'ACCESS_TOKEN_LIFETIME': timedelta(minutes=self.ACCESS_TOKEN_LIFETIME_MINUTES),
            'REFRESH_TOKEN_LIFETIME': timedelta(days=self.REFRESH_TOKEN_LIFETIME_DAYS),
            'ROTATE_REFRESH_TOKENS': self.ROTATE_REFRESH_TOKENS,
            'BLACKLIST_AFTER_ROTATION': self.BLACKLIST_AFTER_ROTATION,
            'UPDATE_LAST_LOGIN': False,
            'ALGORITHM': self.ALGORITHM,
            'SIGNING_KEY': self.SIGNING_KEY,
            'VERIFYING_KEY': None,
            'AUDIENCE': None,
            'ISSUER': None,
            'AUTH_HEADER_TYPES': (self.AUTH_HEADER_TYPES,),
            'AUTH_HEADER_NAME': self.AUTH_HEADER_NAME,
            'USER_ID_FIELD': self.USER_ID_FIELD,
            'USER_ID_CLAIM': self.USER_ID_CLAIM,
            'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
            'TOKEN_TYPE_CLAIM': 'token_type',
            'JTI_CLAIM': 'jti',
            'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
            'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
            'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
        }
