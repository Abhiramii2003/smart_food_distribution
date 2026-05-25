from django.shortcuts import render
from ngo.models import NGO, AcceptedFood
from restaurant.models import Restaurant, SurplusFood
from django.db.models import Sum

def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    total_ngos = NGO.objects.count()
    total_restaurants = Restaurant.objects.count()
    total_surplus_events = SurplusFood.objects.count()
    
    # Calculate total kg of food donated globally
    total_food_kg = SurplusFood.objects.aggregate(Sum('prepared_quantity'))['prepared_quantity__sum'] or 0

    # Map Data: Combine restaurants and NGOs (that have locations, but only Restaurants have lat/lng currently)
    locations = []
    restaurants = Restaurant.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    for r in restaurants:
        locations.append({
            'lat': r.latitude,
            'lng': r.longitude,
            'name': r.name,
            'type': 'Restaurant',
            'info': f"District: {r.district}"
        })

    # Activity Feed: All accepted foods
    global_activity = AcceptedFood.objects.select_related('ngo', 'surplus_food__restaurant').order_by('-accepted_on')

    # Chart Data: Surplus Submissions over time (by event type for simplicity)
    event_type_counts = {}
    for f in SurplusFood.objects.all():
        event_type_counts[f.event_type] = event_type_counts.get(f.event_type, 0) + 1
    
    chart_labels = list(event_type_counts.keys())
    chart_data = list(event_type_counts.values())

    return render(request, 'admin_dashboard.html', {
        'total_ngos': total_ngos,
        'total_restaurants': total_restaurants,
        'total_surplus_events': total_surplus_events,
        'total_food_kg': total_food_kg,
        'locations': locations,
        'global_activity': global_activity,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })
