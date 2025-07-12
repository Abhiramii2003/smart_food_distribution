from django.shortcuts import render, redirect, get_object_or_404
from restaurant.models import SurplusFood
from .models import NGO, AcceptedFood
from .forms import NGORegistrationForm, NGOLoginForm
from django.contrib import messages


# Create your views here.
def ngo_dashboard(request):
    ngo_id = request.session.get('ngo_id')
    if not ngo_id:
        return redirect('ngo_login')

    ngo = get_object_or_404(NGO, pk=ngo_id)

    accepted_ids = AcceptedFood.objects.values_list('surplus_food_id', flat=True)
    available_food = SurplusFood.objects.exclude(id__in=accepted_ids)
    accepted_food = AcceptedFood.objects.filter(ngo=ngo).select_related('surplus_food')

    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        food = get_object_or_404(SurplusFood, pk=food_id)
        AcceptedFood.objects.create(ngo=ngo, surplus_food=food)
        return redirect('ngo_dashboard')

    return render(request, 'ngo/dashboard.html', {
        'food_list': available_food,
        'accepted_list': accepted_food,
    })



def ngo_register(request):
    if request.method == 'POST':
        form = NGORegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('ngo_login')
    else:
        form = NGORegistrationForm()
    return render(request, 'ngo/register.html', {'form': form})

def ngo_login(request):
    if request.method == 'POST':
        form = NGOLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                ngo = NGO.objects.get(email=email, password=password)
                request.session['ngo_id'] = ngo.id
                return redirect('ngo_dashboard')
            except NGO.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = NGOLoginForm()
    return render(request, 'ngo/login.html', {'form': form})

def ngo_logout(request):
    request.session.flush()
    return redirect('ngo_login')