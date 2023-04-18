from django.contrib import admin
from .models import User, Video, Hospital, Appointment, Content, Notification, Category

admin.site.register(User)
admin.site.register(Video)
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(Content)
admin.site.register(Notification)
admin.site.register(Category)