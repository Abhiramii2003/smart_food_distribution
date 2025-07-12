from django.shortcuts import render, redirect
from .forms import SurplusFoodForm

# Create your views here.

def surplus_food_view(request):
    if request.method == 'POST':
        form = SurplusFoodForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'restaurant/success.html')
    else:
        form = SurplusFoodForm()
    return render(request, 'restaurant/surplus_form.html', {'form': form})