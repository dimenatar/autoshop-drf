from django.urls import path

from autoshops import views

urlpatterns = [
    path('shop-stats/', views.AutoShopStatisticsView.as_view(), name='autoshops'),
    path('stats/', views.AutoShopsTotalStatisticsView.as_view(), name='autoshops'),
]
