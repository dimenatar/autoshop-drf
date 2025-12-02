from django.urls import path

from cars import views

urlpatterns = [
    path('', views.CarListView.as_view()),
    path('<int:pk>', views.CarView.as_view()),
]
