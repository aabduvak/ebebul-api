from django.db.models import DecimalField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin
from math import radians, sin, cos, sqrt, atan2

from .models import Hospital

EARTH_RADIUS_KM = 6371.01
MAX_HOSPITALS = 10

def get_nearest_hospitals(user_latitude, user_longitude):

    hospitals = Hospital.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        latitude__gt=0.000,
        longitude__gt=0.000,
    ).annotate(
        distance=ExpressionWrapper(
            ACos(
                Cos(Radians(user_latitude)) *
                Cos(Radians('latitude')) *
                Cos(Radians('longitude') - Radians(user_longitude)) +
                Sin(Radians(user_latitude)) *
                Sin(Radians('latitude'))
            ) * EARTH_RADIUS_KM,
            output_field=DecimalField(max_digits=16, decimal_places=13)
        )
    ).order_by('distance')[:MAX_HOSPITALS]

    return hospitals

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude coordinates to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Calculate the difference between the two latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the great-circle distance using the Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = EARTH_RADIUS_KM * c

    return distance