from django import forms
from .models import SurplusFood

class SurplusFoodForm(forms.ModelForm):
    class Meta:
        model = SurplusFood
        fields = ['restaurant', 'event_type', 'attendees', 'menu_type', 'prepared_quantity']
