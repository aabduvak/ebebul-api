from django.conf import settings

class NosyAPI():
    TOKEN = ''
    BASE = ''
	
    def __init__(self):
        self.TOKEN = settings.NOSY_TOKEN
        self.BASE = settings.NOSY_BASE_URL
    
	
    
	