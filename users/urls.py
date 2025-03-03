from django.urls import path

from users.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name = 'user'),
    path('users/', RegistrationAPIView.as_view(), name='users'),
    path('users/login/', LoginAPIView.as_view(), name='users/login'),
]