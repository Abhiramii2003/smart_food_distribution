from django.urls import path
from . import views

urlpatterns = [
    path('surplus/', views.surplus_food_view, name='surplus_food'),
]
