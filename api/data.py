from django.conf import settings

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import City, Discrict, Hospital 


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

            item = Discrict.objects.create(name=name, slug=slug, city=city)
            item.save()

        return JsonResponse({'status': 200, 'message': 'ok'})
    
    def store_hospitals(self, city):
        response_data = self.get('hospital', {'city': city.slug})
        
        if response_data['rowCount'] <= 0:
            return JsonResponse({'status': 404, 'message': 'No data available'})
        
        data_list = response_data['data']
        for data in data_list:
            name = data['Ad']
            address = data['Adres']
            phone = data['Tel']
            email = data['Email']
            website = data['Website']
            discrict = Discrict.objects.filter(name=data['ilce'])
            
            district = None
            if len(discrict) > 0:
                district = discrict[0]
            
            longitude = data['longitude'] if data['longitude'] else 0.00
            latitude = data['latitude'] if data['latitude'] else 0.00
            
            item = Hospital.objects.create(
                name=name,
                address=address,
                longitude=longitude,
                latitude=latitude,
                city=city,
                discrict=district,
                phone=phone,
                email=email,
                website=website
            )
            item.save()

        return JsonResponse({'status': 200, 'message': 'ok'})
