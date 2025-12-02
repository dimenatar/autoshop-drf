from django.urls import path

from offers import views

urlpatterns = [
    path('user/', views.UserOfferListView.as_view()),
    path('user/<int:pk>', views.UserOfferView.as_view()),
    path('autoshop/', views.AutoShopOfferListView.as_view()),
    path('autoshop/<int:pk>', views.AutoShopOfferView.as_view()),
]
