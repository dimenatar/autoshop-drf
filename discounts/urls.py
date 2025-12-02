from django.urls import path

from discounts import views

urlpatterns = [
    path('general/', views.GeneralDiscountListView.as_view()),
    path('general/<int:pk>', views.GeneralDiscountView.as_view()),
    path('user-personal/', views.UserPersonalDiscountListView.as_view()),
    path('user-personal/<int:pk>', views.UserPersonalDiscountView.as_view()),
    path('autoshop-personal/', views.AutoShopPersonalDiscountListView.as_view()),
    path('autoshop-personal/<int:pk>', views.AutoShopPersonalDiscountView.as_view()),
    path('car/', views.CarDiscountListView.as_view()),
    path('car/<int:pk>', views.CarDiscountView.as_view()),
]
