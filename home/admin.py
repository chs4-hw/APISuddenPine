from django.contrib import admin
from .models import HomeStat, DayLog, Device, RoomControl

# Register your models here.

admin.site.register(HomeStat)
admin.site.register(DayLog)
admin.site.register(Device)
admin.site.register(RoomControl)

