from django.db import models
from restaurant.models import SurplusFood

# Create your models here.



class NGO(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, default='temp1234')
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AcceptedFood(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    surplus_food = models.ForeignKey(SurplusFood, on_delete=models.CASCADE)
    accepted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ngo.name} accepted {self.surplus_food}"
