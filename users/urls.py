from django.urls import path

from users import views

urlpatterns = [
    path('user-stats/', views.UserStatisticsView.as_view(), name='users'),
    path('stats/', views.UsersTotalStatisticsView.as_view(), name='users'),
]