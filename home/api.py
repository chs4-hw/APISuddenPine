from django.shortcuts import render
from .models import HomeStat, DayLog, Device, RoomControl
from rest_framework import viewsets, permissions, filters
from .serializers import HomeStatsSerializer, DayLogsSerializer, DevicesSerializer, RoomControlSerializer
# Create your views here.    

class HomeStatsAPI(viewsets.ModelViewSet):
    queryset = HomeStat.objects.all()
    permission_classes = [
        permissions.IsAdminUser
    ]
    serializer_class = HomeStatsSerializer
    filter_backends = [
        filters.SearchFilter
    ]
    
    search_fields = ['user__id']

    def sample_view(request):
        permission_classes=permissions.IsAuthenticated
        current_user = request.user
        query = self.request.GET.get('current_user')

        return JsonResponse(query)


class UserStatsAPI(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HomeStatsSerializer
    queryset = HomeStat.objects.all()

    def sample_view(request):
        current_user = request.user
        

class DayLogsAPI(viewsets.ModelViewSet):
    queryset = DayLog.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DayLogsSerializer

class DevicesAPI(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DevicesSerializer

class RoomControlAPI(viewsets.ModelViewSet):
    queryset = RoomControl.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RoomControlSerializer  
