from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.conf import settings

from rest_framework import filters

User = settings.AUTH_USER_MODEL

# Create your models here. 

# Stats for/per House (current)

class HomeStat(models.Model):
    dailyBattery = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    dailyConS = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    dailySave = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    dailySolar = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    updated = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    home = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s %s %s'% (self.dailyBattery, self.dailyConS, self.dailySave, self.dailySolar, self.updated, self.home)

# Stats logged as the week progesses
# Daily Energy Consumption (home)

class DayLog(models.Model):
    dailyBattery = models.DecimalField(max_digits=9, decimal_places=3)
    dailyConS = models.DecimalField(max_digits=9, decimal_places=3)
    dailySave = models.DecimalField(max_digits=9, decimal_places=3)
    dailySolar = models.DecimalField(max_digits=9, decimal_places=3)
    date = models.DateField(auto_now_add=False, unique=False)  
    home = models.ForeignKey(User, on_delete=models.CASCADE)

    # Changes made as previous iteration checked for tuples, not strings
    def __str__(self):
        return '%s %s %s %s %s'% (self.dailyBattery, self.dailyConS, self.dailySave, self.dailySolar, self.home)


# Energy Consumption by Devices

class Device(models.Model):
    device = models.CharField(max_length=50)
    deviceconsumption = models.DecimalField(max_digits=5, decimal_places=3)
    home = models.ForeignKey(User, on_delete=models.CASCADE)

# Lighting and heating controls per room

class RoomControl(models.Model):
    roomtype = models.CharField(max_length=50)
    heating = models.DecimalField(max_digits=4, decimal_places=1)
    light = models.BooleanField(default=False)
    safetyalarm = models.BooleanField(default=False)
    home = models.ForeignKey(User, on_delete=models.CASCADE)
