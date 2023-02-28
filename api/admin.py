from django.contrib import admin
from .models import User, Video, Hospital, VisitRequest, Content, Notification

admin.site.register(User)
admin.site.register(Video)
admin.site.register(Hospital)
admin.site.register(VisitRequest)
admin.site.register(Content)
admin.site.register(Notification)