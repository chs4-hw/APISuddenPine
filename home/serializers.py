from rest_framework import serializers
from .models import HomeStat, DayLog, Device, RoomControl

# Serializers

class HomeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStat
        fields = ('__all__')
   
class DayLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayLog
        fields = ('__all__')

class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('__all__')

class RoomControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomControl
        fields = ('__all__')

#class LeagueSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = League
#        fields = '__all__'                      