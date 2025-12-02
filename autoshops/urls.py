from django.urls import path

from autoshops import views

urlpatterns = [
    path('', views.AutoShopListView.as_view()),
    path('<int:pk>', views.AutoShopView.as_view()),
]
