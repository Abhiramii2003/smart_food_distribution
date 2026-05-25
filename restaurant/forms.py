from django import forms
from .models import SurplusFood, Restaurant

class RestaurantRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'district', 'location', 'contact_email', 'password']

class RestaurantLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class SurplusFoodForm(forms.ModelForm):
    class Meta:
        model = SurplusFood
        fields = ['event_type', 'attendees', 'menu_type', 'prepared_quantity']
