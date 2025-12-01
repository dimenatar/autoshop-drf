from django.urls import path

from suppliers import views

urlpatterns = [
    path('supplier-stats/', views.SupplierStatisticsView.as_view(), name='users'),
    path('stats/', views.SuppliersTotalStatisticsView.as_view(), name='users'),
]