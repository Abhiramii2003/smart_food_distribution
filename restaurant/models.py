from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_email = models.EmailField()
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SurplusFood(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    attendees = models.PositiveIntegerField()
    menu_type = models.CharField(max_length=50, choices=[('veg', 'Veg'), ('non-veg', 'Non-Veg'), ('mixed', 'Mixed')])
    prepared_quantity = models.FloatField(help_text="in kg")
    predicted_surplus = models.FloatField(help_text="AI will predict this", null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.event_type} ({self.attendees} guests)"
