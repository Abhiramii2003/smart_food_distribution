from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
    path('logistics/', views.ngo_logistics, name='ngo_logistics'),
    path('analytics/', views.ngo_analytics, name='ngo_analytics'),
    path('register/', views.ngo_register, name='ngo_register'),
    path('login/', views.ngo_login, name='ngo_login'),
    path('logout/', views.ngo_logout, name='ngo_logout'),
]
