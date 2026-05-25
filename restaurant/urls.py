from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.restaurant_login, name='restaurant_login'),
    path('register/', views.restaurant_register, name='restaurant_register'),
    path('logout/', views.restaurant_logout, name='restaurant_logout'),
    path('dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('surplus/', views.surplus_food_view, name='surplus_food'),
]
