from django.shortcuts import render, redirect, get_object_or_404
from restaurant.models import SurplusFood
from .models import NGO, AcceptedFood, Volunteer
from .forms import NGORegistrationForm, NGOLoginForm
from django.contrib import messages
from datetime import datetime

# Create your views here.
def ngo_dashboard(request):
    ngo_id = request.session.get('ngo_id')
    if not ngo_id:
        return redirect('ngo_login')

    ngo = get_object_or_404(NGO, pk=ngo_id)

    # Step 1: Exclude already accepted food
    accepted_ids = AcceptedFood.objects.values_list('surplus_food_id', flat=True)
    food_qs = SurplusFood.objects.exclude(id__in=accepted_ids)

    # Step 2: Apply filters from GET params
    # district = request.GET.get('district')
    # date_str = request.GET.get('date')  # Expecting format YYYY-MM-DD
    # event_type = request.GET.get('event_type')

    # if district:
    #     food_qs = food_qs.filter(restaurant__district__icontains=district)

    # if date_str:
    #     try:
    #         date = datetime.strptime(date_str, '%Y-%m-%d').date()
    #         food_qs = food_qs.filter(submitted_on__date=date)
    #     except ValueError:
    #         pass  # Skip filter if date format is invalid

    # if event_type:
    #     food_qs = food_qs.filter(event_type__iexact=event_type)

    # Step 3: Accepted history
    accepted_food = AcceptedFood.objects.filter(ngo=ngo).select_related('surplus_food')

    # Step 4: Handle accept action
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        food = get_object_or_404(SurplusFood, pk=food_id)
        AcceptedFood.objects.create(ngo=ngo, surplus_food=food)
        return redirect('ngo_dashboard')

    total_accepted = accepted_food.count()
    available_food_count = food_qs.count()
    total_kg_accepted = sum(item.surplus_food.prepared_quantity for item in accepted_food)

    return render(request, 'ngo/dashboard.html', {
        'ngo': ngo,
        'food_list': food_qs,
        'accepted_list': accepted_food,
        'total_accepted': total_accepted,
        'available_food_count': available_food_count,
        'total_kg_accepted': total_kg_accepted,
    })

def ngo_analytics(request):
    ngo_id = request.session.get('ngo_id')
    if not ngo_id:
        return redirect('ngo_login')

    ngo = get_object_or_404(NGO, pk=ngo_id)

    accepted_ids = AcceptedFood.objects.values_list('surplus_food_id', flat=True)
    food_qs = SurplusFood.objects.exclude(id__in=accepted_ids)

    restaurant_locations = [
        {
            'lat': food.restaurant.latitude,
            'lng': food.restaurant.longitude,
            'name': food.restaurant.name,
            'event': food.event_type,
            'quantity': food.prepared_quantity
        }
        for food in food_qs if food.restaurant.latitude and food.restaurant.longitude
    ]

    event_type_counts = {}
    for f in food_qs:
        event_type_counts[f.event_type] = event_type_counts.get(f.event_type, 0) + 1
    
    chart_labels = list(event_type_counts.keys())
    chart_data = list(event_type_counts.values())

    return render(request, 'ngo/analytics.html', {
        'ngo': ngo,
        'restaurant_locations': restaurant_locations,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })

def ngo_logistics(request):
    ngo_id = request.session.get('ngo_id')
    if not ngo_id:
        return redirect('ngo_login')

    ngo = get_object_or_404(NGO, pk=ngo_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_volunteer':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            vehicle_type = request.POST.get('vehicle_type')
            Volunteer.objects.create(ngo=ngo, name=name, phone=phone, vehicle_type=vehicle_type)
            messages.success(request, f"Volunteer {name} added successfully.")
            
        elif action == 'assign_volunteer':
            food_id = request.POST.get('food_id')
            volunteer_id = request.POST.get('volunteer_id')
            
            food = get_object_or_404(AcceptedFood, pk=food_id, ngo=ngo)
            volunteer = get_object_or_404(Volunteer, pk=volunteer_id, ngo=ngo)
            
            food.volunteer = volunteer
            food.save()
            messages.success(request, f"Assigned {volunteer.name} to pickup {food.surplus_food.restaurant.name}'s food.")
            
        return redirect('ngo_logistics')

    volunteers = Volunteer.objects.filter(ngo=ngo).order_by('-registered_on')
    deliveries = AcceptedFood.objects.filter(ngo=ngo).select_related('surplus_food', 'volunteer').order_by('-accepted_on')

    return render(request, 'ngo/logistics.html', {
        'ngo': ngo,
        'volunteers': volunteers,
        'deliveries': deliveries,
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