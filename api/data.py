from django.conf import settings

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import City, District, Hospital 


@csrf_exempt
class NosyAPI():
    TOKEN = ''
    BASE = ''
    
    def __init__(self):
        self.TOKEN = settings.NOSY_TOKEN
        self.BASE = settings.NOSY_BASE_URL
        
    def get(self, endpoint, params):
        url = self.BASE + '/' + endpoint
        
        headers = {
            'Authorization': f'Bearer {self.TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        return response.json()
    
    def store_city(self):
        
        response_data = self.get('getTurkeyCity', {'id': '98842'})
        
        data_list = response_data['data']
        for data in data_list:
            city_name = data['cityName']
            city_slug = data['citySlug']

            city_data = City.objects.create(name=city_name, slug=city_slug)
            city_data.save()

        return JsonResponse({'status': 200, 'message': 'ok'})
    
    def store_discrict(self, city):
        response_data = self.get('getTurkeyCity', {'id': '98842', 'city': city.slug})
        
        data_list = response_data['data']
        for data in data_list:
            name = data['cityName']
            slug = data['citySlug']

            item = District.objects.create(name=name, slug=slug, city=city)
            item.save()

        return JsonResponse({'status': 200, 'message': 'ok'})
