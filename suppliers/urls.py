from django.urls import path

from suppliers import views

urlpatterns = [
    path('', views.SupplierListView.as_view()),
    path('<int:pk>', views.SupplierView.as_view()),
]
