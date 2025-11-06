from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from core.views import HomeView, LoginView, RegisterView, PasswordResetView, PasswordResetConfirmView

schema_view = get_schema_view(
    openapi.Info(
        title="AutoShop API",
        default_version='1.0.0',
        description="AutoShop API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [

    #FRONT
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    #API
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),

    #SWAGGER
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #OTHER
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
