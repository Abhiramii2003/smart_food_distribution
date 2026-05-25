from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Restaurant, SurplusFood
from .forms import SurplusFoodForm, RestaurantRegistrationForm, RestaurantLoginForm

# Create your views here.

def restaurant_register(request):
    if request.method == 'POST':
        form = RestaurantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('restaurant_login')
    else:
        form = RestaurantRegistrationForm()
    return render(request, 'restaurant/register.html', {'form': form})

def restaurant_login(request):
    if request.method == 'POST':
        form = RestaurantLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                restaurant = Restaurant.objects.get(contact_email=email, password=password)
                request.session['restaurant_id'] = restaurant.id
                return redirect('restaurant_dashboard')
            except Restaurant.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = RestaurantLoginForm()
    return render(request, 'restaurant/login.html', {'form': form})

def restaurant_logout(request):
    request.session.flush()
    return redirect('restaurant_login')

def surplus_food_view(request):
    restaurant_id = request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('restaurant_login')
        
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    
    if request.method == 'POST':
        form = SurplusFoodForm(request.POST)
        if form.is_valid():
            surplus_food = form.save(commit=False)
            surplus_food.restaurant = restaurant
            surplus_food.save()
            
            # Trigger WebSocket Notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'ngo_notifications',
                {
                    'type': 'ngo_notification',
                    'message': f"New Surplus Food Available!",
                    'restaurant_name': restaurant.name,
                    'quantity': float(surplus_food.prepared_quantity)
                }
            )

            return redirect('restaurant_dashboard')
    else:
        form = SurplusFoodForm()
    return render(request, 'restaurant/surplus_form.html', {'form': form, 'restaurant': restaurant})

def restaurant_dashboard(request):
    restaurant_id = request.session.get('restaurant_id')
    if not restaurant_id:
        return redirect('restaurant_login')
    
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    surplus_history = SurplusFood.objects.filter(restaurant=restaurant).order_by('-submitted_on')
    
    total_donations = surplus_history.count()
    total_kg_donated = sum(food.prepared_quantity for food in surplus_history)
    
    # Chart Data: Donations by Menu Type
    menu_type_counts = {}
    for f in surplus_history:
        menu_type_counts[f.menu_type] = menu_type_counts.get(f.menu_type, 0) + 1
    
    chart_labels = list(menu_type_counts.keys())
    chart_data = list(menu_type_counts.values())

    # Map Data: Just the restaurant's location
    locations = []
    if restaurant.latitude and restaurant.longitude:
        locations.append({
            'lat': restaurant.latitude,
            'lng': restaurant.longitude,
            'name': restaurant.name,
            'info': "Your Location"
        })

    # Activity feed: Check if food was accepted by looking at `ngo.models.AcceptedFood`
    from ngo.models import AcceptedFood
    accepted_history = AcceptedFood.objects.filter(surplus_food__restaurant=restaurant).select_related('ngo', 'surplus_food').order_by('-accepted_on')

    return render(request, 'restaurant/dashboard.html', {
        'restaurant': restaurant,
        'surplus_history': surplus_history,
        'total_donations': total_donations,
        'total_kg_donated': total_kg_donated,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'locations': locations,
        'accepted_history': accepted_history,
    })