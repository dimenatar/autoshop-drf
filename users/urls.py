from django.urls import path

from users.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, EmailVerificationAPIView, \
    PasswordResetRequestAPIView, PasswordResetConfirmAPIView

app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('users/register/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/verify-email/<str:key>/', EmailVerificationAPIView.as_view(), name='verify-email'),
    path('users/request-reset/', PasswordResetRequestAPIView.as_view(), name='request-password-reset'),
    path('users/reset-password/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='reset-password'),
]
