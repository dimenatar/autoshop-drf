from decouple import config


class RestAuthConfig:
    USE_JWT = config('REST_AUTH_USE_JWT', default=True, cast=bool)
    JWT_AUTH_HTTPONLY = config('REST_AUTH_JWT_HTTPONLY', default=False, cast=bool)
    JWT_AUTH_COOKIE = config('REST_AUTH_JWT_COOKIE', default='autoshop-auth')
    JWT_AUTH_REFRESH_COOKIE = config('REST_AUTH_JWT_REFRESH_COOKIE', default='autoshop-refresh')

    @property
    def rest_auth(self) -> dict:
        return {
            'USE_JWT': self.USE_JWT,
            'JWT_AUTH_HTTPONLY': self.JWT_AUTH_HTTPONLY,
            'JWT_AUTH_COOKIE': self.JWT_AUTH_COOKIE,
            'JWT_AUTH_REFRESH_COOKIE': self.JWT_AUTH_REFRESH_COOKIE,
            'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
            'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer',
            'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
        }
