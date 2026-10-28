from django.urls import path
from . import views


urlpatterns = [
    path('cars/', views.get_cars, name='car-list'),
    path('cars/<int:pk>/', views.get_car_detail, name='car-detail'),

    path('dealers/', views.get_dealers, name='dealer-list'),
    path('dealers/<int:pk>/', views.get_dealer_detail, name='dealer-detail'),
]