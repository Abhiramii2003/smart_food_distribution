from django import forms
from .models import NGO

class NGORegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = NGO
        fields = ['name', 'location', 'contact_person', 'email', 'password']

class NGOLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
