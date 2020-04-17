#from django.conf import url
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile, User
from home.models import HomeStat, DayLog
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin  # Replaces the login Decorator
from django.db.models import Sum, Avg

import django_filters

# Create your views here.

class HomeProfileView(LoginRequiredMixin, TemplateView):

    def get(self, request): 
        template_name = 'home/home_page.html'
        data = UserProfile.objects.all()
        return render(request, template_name, {'entries' : data})

class CompareListView(LoginRequiredMixin, TemplateView):

    def get(self, request): 
        template_name = 'home/compare_homes.html'
        data = UserProfile.objects.all()
        return render(request, template_name, {'entries' : data})


class InfoView(LoginRequiredMixin, TemplateView):

    def get(self, request): 
        template_name = 'home/info.html'
        return render(request, template_name, {})

class SearchResultsView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        query = self.request.GET.get('q')
        data = UserProfile.objects.filter(address__exact=query)
        if data:  
           template_name = 'home/home_page.html' 
           return render(request, template_name, {'entries' : data})

        data = UserProfile.objects.filter(city__exact=query)
        if data:  
           template_name = 'home/home_page.html' 
           return render(request, template_name, {'entries' : data})

        data = UserProfile.objects.filter(country__exact=query)
        if data:  
           template_name = 'home/home_page.html' 
           return render(request, template_name, {'entries' : data})

        data = UserProfile.objects.filter(zip__exact=query)
        if data:
            template_name = 'home/home_page.html'
            return render(request, template_name, {'entries' : data})
        else:
            template_name = 'home/home_page.html'
            return render(request, template_name, {'entries' : data})

class HomeWeekView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        query = self.request.GET.get('q')
        template_name = 'home/weeklogs.html'
        daydata = HomeStat.objects.filter(home_id=query)
        return render(request, template_name, {'entries' : daydata})

class HomeMonthView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        query = self.request.GET.get('q')
        template_name = 'home/monthlogs.html'
        daydata = HomeStat.objects.filter(home_id=query)

        return render(request, template_name, {'entries' : daydata})

class HomeYearView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        query = self.request.GET.get('q')
        template_name = 'home/yearlogs.html'
        daydata = HomeStat.objects.filter(home_id=query)

        return render(request, template_name, {'entries' : daydata})

class CompareMonthChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        queryA = self.request.GET.get('a')
        queryB = self.request.GET.get('b')
        queryAver = DayLog.objects.all()

        querysetA = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryA)
        querysetB = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryB)

        daylabels = [0] * 31
        valuesBatteryA = ["0"] * 31
        valuesBatteryB = ["0"] * 31
        dayAverBattery = ["0"] * 31

        valuesConsumptionA = ["0"] * 31
        valuesConsumptionB = ["0"] * 31
        dayAverConsumption = ["0"] * 31

        valuesSolarA = ["0"] * 31
        valuesSolarB = ["0"] * 31
        dayAverSolar = ["0"] * 31

        valuesSavedA = ["0"] * 31
        valuesSavedB = ["0"] * 31
        dayAverSaved = ["0"] * 31

        valuesBatteryAver = []
        valuesConsumptionAver = []
        valuesSolarAver = []
        valuesSavedAver = []
        

        # Battery

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                valuesBatteryA[entry.date.day-1] = entry.dailyBattery

            
            dayAverBattery[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailyBattery'))
            
            valuesBatteryAver.append(list(dayAverBattery[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                valuesBatteryB[entry.date.day-1] = entry.dailyBattery

        
        # Consumption

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                valuesConsumptionA[entry.date.day-1] = entry.dailyConS

            
            dayAverConsumption[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailyConS'))
            
            valuesConsumptionAver.append(list(dayAverConsumption[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                valuesConsumptionB[entry.date.day-1] = entry.dailyConS

        # Solar

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                valuesSolarA[entry.date.day-1] = entry.dailySolar

            
            dayAverSolar[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailySolar'))
            
            valuesSolarAver.append(list(dayAverSolar[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                valuesSolarB[entry.date.day-1] = entry.dailySolar

        # Money Saved

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                valuesSavedA[entry.date.day-1] = entry.dailySave

            
            dayAverSaved[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailySave'))
            
            valuesSavedAver.append(list(dayAverSaved[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                valuesSavedB[entry.date.day-1] = entry.dailySave

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'valuesBatteryA': valuesBatteryA,
            'valuesBatteryB': valuesBatteryB,
            'valuesBatteryAver': valuesBatteryAver,
            'valuesConsumptionA': valuesConsumptionA,
            'valuesConsumptionB': valuesConsumptionB,
            'valuesConsumptionAver': valuesConsumptionAver,
            'valuesSolarA': valuesSolarA,
            'valuesSolarB': valuesSolarB,
            'valuesSolarAver': valuesSolarAver,
            'valuesSavedA': valuesSavedA,
            'valuesSavedB': valuesSavedB,
            'valuesSavedAver': valuesSavedAver,
        }

        return JsonResponse(data)

class CompareMonthBatteryChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        queryA = self.request.GET.get('a')
        queryB = self.request.GET.get('b')
        queryAver = DayLog.objects.all()

        querysetA = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryA)
        querysetB = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryB)

        daylabels = [0] * 31
        valuesA = ["0"] * 31
        valuesB = ["0"] * 31
        dayAver = ["0"] * 31

        valuesAver = []
        valuesAv = []

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                valuesA[entry.date.day-1] = entry.dailyBattery

            
            dayAver[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailyBattery'))
            
            valuesAver.append(list(dayAver[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                valuesB[entry.date.day-1] = entry.dailyBattery

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'valuesA': valuesA,
            'valuesB': valuesB,
            'valuesAver': valuesAver,
        }

        return JsonResponse(data, safe=False)

class CompareMonthConsumptionChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        queryA = self.request.GET.get('a')
        queryB = self.request.GET.get('b')
        queryAver = DayLog.objects.all()

        querysetA = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryA)
        querysetB = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryB)

        daylabels = [0] * 31
        valuesA = ["0"] * 31
        valuesB = ["0"] * 31
        dayAver = ["0"] * 31

        valuesAver = []
        valuesAv = []

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                valuesA[entry.date.day-1] = entry.dailyConS

            
            dayAver[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailyConS'))
            
            valuesAver.append(list(dayAver[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                valuesB[entry.date.day-1] = entry.dailyConS

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'valuesA': valuesA,
            'valuesB': valuesB,
            'valuesAver': valuesAver,
        }

        return JsonResponse(data, safe=False)

class CompareMonthSolarChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        queryA = self.request.GET.get('a')
        queryB = self.request.GET.get('b')
        queryAver = DayLog.objects.all()

        querysetA = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryA)
        querysetB = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryB)

        daylabels = [0] * 31
        valuesA = ["0"] * 31
        valuesB = ["0"] * 31
        dayAver = ["0"] * 31

        valuesAver = []
        valuesAv = []

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                valuesA[entry.date.day-1] = entry.dailySolar

            
            dayAver[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailySolar'))
            
            valuesAver.append(list(dayAver[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                valuesB[entry.date.day-1] = entry.dailySolar

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'valuesA': valuesA,
            'valuesB': valuesB,
            'valuesAver': valuesAver,
        }

        return JsonResponse(data)

class CompareMonthSavedChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        queryA = self.request.GET.get('a')
        queryB = self.request.GET.get('b')
        queryAver = DayLog.objects.all()

        querysetA = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryA)
        querysetB = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, home_id=queryB)

        daylabels = [0] * 31
        valuesA = ["0"] * 31
        valuesB = ["0"] * 31
        dayAver = ["0"] * 31

        valuesAver = []
        valuesAv = []

        for entry in querysetA:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                valuesA[entry.date.day-1] = entry.dailySave

            
            dayAver[entry.date.day-1] = DayLog.objects.filter(date__year=current_year, date__month=current_month-1, date__day=entry.date.day).aggregate(Avg('dailySave'))
            
            valuesAver.append(list(dayAver[entry.date.day-1].values()))

        for entry in querysetB:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                valuesB[entry.date.day-1] = entry.dailySave

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'valuesA': valuesA,
            'valuesB': valuesB,
            'valuesAver': valuesAver,
        }

        return JsonResponse(data)



class WeekBatteryChart(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        current_day = datetime.datetime.now().day
        year = DayLog.objects.filter(date__year=current_day)

        labels = []
        values = []
        query = self.request.GET.get('q')      
        queryset = reversed(DayLog.objects.filter(home_id=query).order_by('-date')[:7])

        for entry in queryset:
            labels.append(entry.date)
            values.append(entry.dailyBattery)

        data = {
            'labels': labels,
            'values': values,
        }

        return JsonResponse(data)

class WeekConsumptionChart(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        values = []
        query = self.request.GET.get('q')      
        queryset = reversed(DayLog.objects.filter(home_id=query).order_by('-date')[:7])

        for entry in queryset:
            labels.append(entry.date)
            values.append(entry.dailyConS)

        data = {
            'labels': labels,
            'values': values,
        }

        return JsonResponse(data)

class WeekSavedChart(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        values = []
        query = self.request.GET.get('q')      
        queryset = reversed(DayLog.objects.filter(home_id=query).order_by('-date')[:7])

        for entry in queryset:
            labels.append(entry.date)
            values.append(entry.dailySave)

        data = {
            'labels': labels,
            'values': values,
        }

        return JsonResponse(data)

class WeekSolarChart(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        values = []
        query = self.request.GET.get('q')      
        queryset = reversed(DayLog.objects.filter(home_id=query).order_by('-date')[:7])

        for entry in queryset:
            labels.append(entry.date)
            values.append(entry.dailySolar)

        data = {
            'labels': labels,
            'values': values,
        }

        return JsonResponse(data)

class MonthBatteryChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        janSet = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query)
        febSet = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query)
        marSet = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query)
        aprSet = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query)
        maySet = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query)
        junSet = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query)
        julSet = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query)
        augSet = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query)
        sepSet = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query)
        octSet = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query)
        novSet = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query)
        desSet = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query)

        daylabels = [0] * 31
        jan = ["0"] * 31
        feb = ["0"] * 31
        mar = ["0"] * 31
        apr = ["0"] * 31
        may = ["0"] * 31
        jun = ["0"] * 31
        jul = ["0"] * 31
        aug = ["0"] * 31
        sep = ["0"] * 31
        okt = ["0"] * 31
        nov = ["0"] * 31
        des = ["0"] * 31

        for entry in janSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                jan[entry.date.day-1] = entry.dailyBattery

        for entry in febSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                feb[entry.date.day-1] = entry.dailyBattery

        for entry in marSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                mar[entry.date.day-1] = entry.dailyBattery

        for entry in aprSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                apr[entry.date.day-1] = entry.dailyBattery

        for entry in maySet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                may[entry.date.day-1] = entry.dailyBattery

        for entry in junSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                jun[entry.date.day-1] = entry.dailyBattery

        for entry in julSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                jul[entry.date.day-1] = entry.dailyBattery

        for entry in augSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                aug[entry.date.day-1] = entry.dailyBattery

        for entry in sepSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                sep[entry.date.day-1] = entry.dailyBattery

        for entry in octSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                okt[entry.date.day-1] = entry.dailyBattery

        for entry in novSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                nov[entry.date.day-1] = entry.dailyBattery

        for entry in desSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyBattery > 0:                
                des[entry.date.day-1] = entry.dailyBattery

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'jan': jan,
            'feb': feb,
            'mar': mar,
            'apr': apr,
            'may': may,
            'jun': jun,
            'jul': jul,
            'aug': aug,
            'sep': sep,
            'oct': okt,
            'nov': nov,
            'des': des,
        }

        return JsonResponse(data)

class MonthConsumptionChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        janSet = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query)
        febSet = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query)
        marSet = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query)
        aprSet = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query)
        maySet = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query)
        junSet = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query)
        julSet = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query)
        augSet = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query)
        sepSet = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query)
        octSet = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query)
        novSet = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query)
        desSet = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query)

        daylabels = [0] * 31
        jan = ["0"] * 31
        feb = ["0"] * 31
        mar = ["0"] * 31
        apr = ["0"] * 31
        may = ["0"] * 31
        jun = ["0"] * 31
        jul = ["0"] * 31
        aug = ["0"] * 31
        sep = ["0"] * 31
        okt = ["0"] * 31
        nov = ["0"] * 31
        des = ["0"] * 31

        for entry in janSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                jan[entry.date.day-1] = entry.dailyConS

        for entry in febSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                feb[entry.date.day-1] = entry.dailyConS

        for entry in marSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                mar[entry.date.day-1] = entry.dailyConS

        for entry in aprSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                apr[entry.date.day-1] = entry.dailyConS

        for entry in maySet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                may[entry.date.day-1] = entry.dailyConS

        for entry in junSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                jun[entry.date.day-1] = entry.dailyConS

        for entry in julSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                jul[entry.date.day-1] = entry.dailyConS

        for entry in augSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                aug[entry.date.day-1] = entry.dailyConS

        for entry in sepSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                sep[entry.date.day-1] = entry.dailyConS

        for entry in octSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                okt[entry.date.day-1] = entry.dailyConS

        for entry in novSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                nov[entry.date.day-1] = entry.dailyConS

        for entry in desSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailyConS > 0:                
                des[entry.date.day-1] = entry.dailyConS

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'jan': jan,
            'feb': feb,
            'mar': mar,
            'apr': apr,
            'may': may,
            'jun': jun,
            'jul': jul,
            'aug': aug,
            'sep': sep,
            'oct': okt,
            'nov': nov,
            'des': des,
        }

        return JsonResponse(data)

class MonthSavedChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        janSet = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query)
        febSet = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query)
        marSet = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query)
        aprSet = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query)
        maySet = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query)
        junSet = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query)
        julSet = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query)
        augSet = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query)
        sepSet = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query)
        octSet = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query)
        novSet = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query)
        desSet = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query)

        daylabels = [0] * 31
        jan = ["0"] * 31
        feb = ["0"] * 31
        mar = ["0"] * 31
        apr = ["0"] * 31
        may = ["0"] * 31
        jun = ["0"] * 31
        jul = ["0"] * 31
        aug = ["0"] * 31
        sep = ["0"] * 31
        okt = ["0"] * 31
        nov = ["0"] * 31
        des = ["0"] * 31

        for entry in janSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                jan[entry.date.day-1] = entry.dailySave

        for entry in febSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                feb[entry.date.day-1] = entry.dailySave

        for entry in marSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                mar[entry.date.day-1] = entry.dailySave

        for entry in aprSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                apr[entry.date.day-1] = entry.dailySave

        for entry in maySet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                may[entry.date.day-1] = entry.dailySave

        for entry in junSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                jun[entry.date.day-1] = entry.dailySave

        for entry in julSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                jul[entry.date.day-1] = entry.dailySave

        for entry in augSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                aug[entry.date.day-1] = entry.dailySave

        for entry in sepSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                sep[entry.date.day-1] = entry.dailySave

        for entry in octSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                okt[entry.date.day-1] = entry.dailySave

        for entry in novSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                nov[entry.date.day-1] = entry.dailySave

        for entry in desSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySave > 0:                
                des[entry.date.day-1] = entry.dailySave

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'jan': jan,
            'feb': feb,
            'mar': mar,
            'apr': apr,
            'may': may,
            'jun': jun,
            'jul': jul,
            'aug': aug,
            'sep': sep,
            'oct': okt,
            'nov': nov,
            'des': des,
        }

        return JsonResponse(data)

class MonthSolarChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        janSet = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query)
        febSet = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query)
        marSet = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query)
        aprSet = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query)
        maySet = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query)
        junSet = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query)
        julSet = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query)
        augSet = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query)
        sepSet = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query)
        octSet = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query)
        novSet = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query)
        desSet = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query)

        daylabels = [0] * 31
        jan = ["0"] * 31
        feb = ["0"] * 31
        mar = ["0"] * 31
        apr = ["0"] * 31
        may = ["0"] * 31
        jun = ["0"] * 31
        jul = ["0"] * 31
        aug = ["0"] * 31
        sep = ["0"] * 31
        okt = ["0"] * 31
        nov = ["0"] * 31
        des = ["0"] * 31

        for entry in janSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                jan[entry.date.day-1] = entry.dailySolar

        for entry in febSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                feb[entry.date.day-1] = entry.dailySolar

        for entry in marSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                mar[entry.date.day-1] = entry.dailySolar

        for entry in aprSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                apr[entry.date.day-1] = entry.dailySolar

        for entry in maySet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                may[entry.date.day-1] = entry.dailySolar

        for entry in junSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                jun[entry.date.day-1] = entry.dailySolar

        for entry in julSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                jul[entry.date.day-1] = entry.dailySolar

        for entry in augSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                aug[entry.date.day-1] = entry.dailySolar

        for entry in sepSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                sep[entry.date.day-1] = entry.dailySolar

        for entry in octSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                okt[entry.date.day-1] = entry.dailySolar

        for entry in novSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                nov[entry.date.day-1] = entry.dailySolar

        for entry in desSet:
            daylabels[entry.date.day] = entry.date.day-1
            if entry.dailySolar > 0:                
                des[entry.date.day-1] = entry.dailySolar

        for i in range(len(daylabels)):
            daylabels[i] = i + 1

        data = {
            'daylabels': daylabels,
            'jan': jan,
            'feb': feb,
            'mar': mar,
            'apr': apr,
            'may': may,
            'jun': jun,
            'jul': jul,
            'aug': aug,
            'sep': sep,
            'oct': okt,
            'nov': nov,
            'des': des,
        }

        return JsonResponse(data)

class YearBatteryChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        jan0 = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query).aggregate(Sum('dailyBattery'))
        jan1 = DayLog.objects.filter(date__year=current_year-1, date__month=1, home_id=query).aggregate(Sum('dailyBattery'))
        jan2 = DayLog.objects.filter(date__year=current_year-2, date__month=1, home_id=query).aggregate(Sum('dailyBattery'))
        jan3 = DayLog.objects.filter(date__year=current_year-3, date__month=1, home_id=query).aggregate(Sum('dailyBattery'))
        jan4 = DayLog.objects.filter(date__year=current_year-4, date__month=1, home_id=query).aggregate(Sum('dailyBattery'))

        feb0 = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query).aggregate(Sum('dailyBattery'))
        feb1 = DayLog.objects.filter(date__year=current_year-1, date__month=2,home_id=query).aggregate(Sum('dailyBattery'))
        feb2 = DayLog.objects.filter(date__year=current_year-2, date__month=2,home_id=query).aggregate(Sum('dailyBattery'))
        feb3 = DayLog.objects.filter(date__year=current_year-3, date__month=2,home_id=query).aggregate(Sum('dailyBattery'))
        feb4 = DayLog.objects.filter(date__year=current_year-4, date__month=2,home_id=query).aggregate(Sum('dailyBattery'))

        mar0 = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query).aggregate(Sum('dailyBattery'))
        mar1 = DayLog.objects.filter(date__year=current_year-1, date__month=3,home_id=query).aggregate(Sum('dailyBattery'))
        mar2 = DayLog.objects.filter(date__year=current_year-2, date__month=3,home_id=query).aggregate(Sum('dailyBattery'))
        mar3 = DayLog.objects.filter(date__year=current_year-3, date__month=3,home_id=query).aggregate(Sum('dailyBattery'))
        mar4 = DayLog.objects.filter(date__year=current_year-4, date__month=3,home_id=query).aggregate(Sum('dailyBattery'))

        apr0 = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query).aggregate(Sum('dailyBattery'))
        apr1 = DayLog.objects.filter(date__year=current_year-1, date__month=4, home_id=query).aggregate(Sum('dailyBattery'))
        apr2 = DayLog.objects.filter(date__year=current_year-2, date__month=4, home_id=query).aggregate(Sum('dailyBattery'))
        apr3 = DayLog.objects.filter(date__year=current_year-3, date__month=4, home_id=query).aggregate(Sum('dailyBattery'))
        apr4 = DayLog.objects.filter(date__year=current_year-4, date__month=4, home_id=query).aggregate(Sum('dailyBattery'))

        may0 = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query).aggregate(Sum('dailyBattery'))
        may1 = DayLog.objects.filter(date__year=current_year-1, date__month=5,home_id=query).aggregate(Sum('dailyBattery'))
        may2 = DayLog.objects.filter(date__year=current_year-2, date__month=5,home_id=query).aggregate(Sum('dailyBattery'))
        may3 = DayLog.objects.filter(date__year=current_year-3, date__month=5,home_id=query).aggregate(Sum('dailyBattery'))
        may4 = DayLog.objects.filter(date__year=current_year-4, date__month=5,home_id=query).aggregate(Sum('dailyBattery'))

        jun0 = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query).aggregate(Sum('dailyBattery'))
        jun1 = DayLog.objects.filter(date__year=current_year-1, date__month=6,home_id=query).aggregate(Sum('dailyBattery'))
        jun2 = DayLog.objects.filter(date__year=current_year-2, date__month=6,home_id=query).aggregate(Sum('dailyBattery'))
        jun3 = DayLog.objects.filter(date__year=current_year-3, date__month=6,home_id=query).aggregate(Sum('dailyBattery'))
        jun4 = DayLog.objects.filter(date__year=current_year-4, date__month=6,home_id=query).aggregate(Sum('dailyBattery'))

        jul0 = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query).aggregate(Sum('dailyBattery'))
        jul1 = DayLog.objects.filter(date__year=current_year-1, date__month=7, home_id=query).aggregate(Sum('dailyBattery'))
        jul2 = DayLog.objects.filter(date__year=current_year-2, date__month=7, home_id=query).aggregate(Sum('dailyBattery'))
        jul3 = DayLog.objects.filter(date__year=current_year-3, date__month=7, home_id=query).aggregate(Sum('dailyBattery'))
        jul4 = DayLog.objects.filter(date__year=current_year-4, date__month=7, home_id=query).aggregate(Sum('dailyBattery'))

        aug0 = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query).aggregate(Sum('dailyBattery'))
        aug1 = DayLog.objects.filter(date__year=current_year-1, date__month=8,home_id=query).aggregate(Sum('dailyBattery'))
        aug2 = DayLog.objects.filter(date__year=current_year-2, date__month=8,home_id=query).aggregate(Sum('dailyBattery'))
        aug3 = DayLog.objects.filter(date__year=current_year-3, date__month=8,home_id=query).aggregate(Sum('dailyBattery'))
        aug4 = DayLog.objects.filter(date__year=current_year-4, date__month=8,home_id=query).aggregate(Sum('dailyBattery'))

        sep0 = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query).aggregate(Sum('dailyBattery'))
        sep1 = DayLog.objects.filter(date__year=current_year-1, date__month=9,home_id=query).aggregate(Sum('dailyBattery'))
        sep2 = DayLog.objects.filter(date__year=current_year-2, date__month=9,home_id=query).aggregate(Sum('dailyBattery'))
        sep3 = DayLog.objects.filter(date__year=current_year-3, date__month=9,home_id=query).aggregate(Sum('dailyBattery'))
        sep4 = DayLog.objects.filter(date__year=current_year-4, date__month=9,home_id=query).aggregate(Sum('dailyBattery'))

        oct0 = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query).aggregate(Sum('dailyBattery'))
        oct1 = DayLog.objects.filter(date__year=current_year-1, date__month=10, home_id=query).aggregate(Sum('dailyBattery'))
        oct2 = DayLog.objects.filter(date__year=current_year-2, date__month=10, home_id=query).aggregate(Sum('dailyBattery'))
        oct3 = DayLog.objects.filter(date__year=current_year-3, date__month=10, home_id=query).aggregate(Sum('dailyBattery'))
        oct4 = DayLog.objects.filter(date__year=current_year-4, date__month=10, home_id=query).aggregate(Sum('dailyBattery'))

        nov0 = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query).aggregate(Sum('dailyBattery'))
        nov1 = DayLog.objects.filter(date__year=current_year-1, date__month=11,home_id=query).aggregate(Sum('dailyBattery'))
        nov2 = DayLog.objects.filter(date__year=current_year-2, date__month=11,home_id=query).aggregate(Sum('dailyBattery'))
        nov3 = DayLog.objects.filter(date__year=current_year-3, date__month=11,home_id=query).aggregate(Sum('dailyBattery'))
        nov4 = DayLog.objects.filter(date__year=current_year-4, date__month=11,home_id=query).aggregate(Sum('dailyBattery'))

        des0 = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query).aggregate(Sum('dailyBattery'))
        des1 = DayLog.objects.filter(date__year=current_year-1, date__month=12,home_id=query).aggregate(Sum('dailyBattery'))
        des2 = DayLog.objects.filter(date__year=current_year-2, date__month=12,home_id=query).aggregate(Sum('dailyBattery'))
        des3 = DayLog.objects.filter(date__year=current_year-3, date__month=12,home_id=query).aggregate(Sum('dailyBattery'))
        des4 = DayLog.objects.filter(date__year=current_year-4, date__month=12,home_id=query).aggregate(Sum('dailyBattery'))

        labels = []

        label0 = [current_year]
        label1 = [current_year-1]
        label2 = [current_year-2]
        label3 = [current_year-3]
        label4 = [current_year-4]

        values0 = [
            (list(jan0.values())),
            (list(feb0.values())),
            (list(mar0.values())),
            (list(apr0.values())),
            (list(may0.values())),
            (list(jun0.values())),
            (list(jul0.values())),
            (list(aug0.values())),
            (list(sep0.values())),
            (list(oct0.values())),
            (list(nov0.values())),
            (list(des0.values()))
            ]
        
        values1 = [
            (list(jan1.values())),
            (list(feb1.values())),
            (list(mar1.values())),
            (list(apr1.values())),
            (list(may1.values())),
            (list(jun1.values())),
            (list(jul1.values())),
            (list(aug1.values())),
            (list(sep1.values())),
            (list(oct1.values())),
            (list(nov1.values())),
            (list(des1.values()))
            ]

        values2 = [
            (list(jan2.values())),
            (list(feb2.values())),
            (list(mar2.values())),
            (list(apr2.values())),
            (list(may2.values())),
            (list(jun2.values())),
            (list(jul2.values())),
            (list(aug2.values())),
            (list(sep2.values())),
            (list(oct2.values())),
            (list(nov2.values())),
            (list(des2.values()))
            ]

        values3 = [
            (list(jan3.values())),
            (list(feb3.values())),
            (list(mar3.values())),
            (list(apr3.values())),
            (list(may3.values())),
            (list(jun3.values())),
            (list(jul3.values())),
            (list(aug3.values())),
            (list(sep3.values())),
            (list(oct3.values())),
            (list(nov3.values())),
            (list(des3.values()))
            ]

        values4 = [
            (list(jan4.values())),
            (list(feb4.values())),
            (list(mar4.values())),
            (list(apr4.values())),
            (list(may4.values())),
            (list(jun4.values())),
            (list(jul4.values())),
            (list(aug4.values())),
            (list(sep4.values())),
            (list(oct4.values())),
            (list(nov4.values())),
            (list(des4.values()))
            ]

        data = {
            'labels': ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Des"],
            'label0': label0,
            'label1': label1,
            'label2': label2,
            'label3': label3,
            'label4': label4,
            'values0': values0,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4
        }

        return JsonResponse(data)

class YearConsumptionChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        jan0 = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query).aggregate(Sum('dailyConS'))
        jan1 = DayLog.objects.filter(date__year=current_year-1, date__month=1, home_id=query).aggregate(Sum('dailyConS'))
        jan2 = DayLog.objects.filter(date__year=current_year-2, date__month=1, home_id=query).aggregate(Sum('dailyConS'))
        jan3 = DayLog.objects.filter(date__year=current_year-3, date__month=1, home_id=query).aggregate(Sum('dailyConS'))
        jan4 = DayLog.objects.filter(date__year=current_year-4, date__month=1, home_id=query).aggregate(Sum('dailyConS'))

        feb0 = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query).aggregate(Sum('dailyConS'))
        feb1 = DayLog.objects.filter(date__year=current_year-1, date__month=2,home_id=query).aggregate(Sum('dailyConS'))
        feb2 = DayLog.objects.filter(date__year=current_year-2, date__month=2,home_id=query).aggregate(Sum('dailyConS'))
        feb3 = DayLog.objects.filter(date__year=current_year-3, date__month=2,home_id=query).aggregate(Sum('dailyConS'))
        feb4 = DayLog.objects.filter(date__year=current_year-4, date__month=2,home_id=query).aggregate(Sum('dailyConS'))

        mar0 = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query).aggregate(Sum('dailyConS'))
        mar1 = DayLog.objects.filter(date__year=current_year-1, date__month=3,home_id=query).aggregate(Sum('dailyConS'))
        mar2 = DayLog.objects.filter(date__year=current_year-2, date__month=3,home_id=query).aggregate(Sum('dailyConS'))
        mar3 = DayLog.objects.filter(date__year=current_year-3, date__month=3,home_id=query).aggregate(Sum('dailyConS'))
        mar4 = DayLog.objects.filter(date__year=current_year-4, date__month=3,home_id=query).aggregate(Sum('dailyConS'))

        apr0 = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query).aggregate(Sum('dailyConS'))
        apr1 = DayLog.objects.filter(date__year=current_year-1, date__month=4, home_id=query).aggregate(Sum('dailyConS'))
        apr2 = DayLog.objects.filter(date__year=current_year-2, date__month=4, home_id=query).aggregate(Sum('dailyConS'))
        apr3 = DayLog.objects.filter(date__year=current_year-3, date__month=4, home_id=query).aggregate(Sum('dailyConS'))
        apr4 = DayLog.objects.filter(date__year=current_year-4, date__month=4, home_id=query).aggregate(Sum('dailyConS'))

        may0 = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query).aggregate(Sum('dailyConS'))
        may1 = DayLog.objects.filter(date__year=current_year-1, date__month=5,home_id=query).aggregate(Sum('dailyConS'))
        may2 = DayLog.objects.filter(date__year=current_year-2, date__month=5,home_id=query).aggregate(Sum('dailyConS'))
        may3 = DayLog.objects.filter(date__year=current_year-3, date__month=5,home_id=query).aggregate(Sum('dailyConS'))
        may4 = DayLog.objects.filter(date__year=current_year-4, date__month=5,home_id=query).aggregate(Sum('dailyConS'))

        jun0 = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query).aggregate(Sum('dailyConS'))
        jun1 = DayLog.objects.filter(date__year=current_year-1, date__month=6,home_id=query).aggregate(Sum('dailyConS'))
        jun2 = DayLog.objects.filter(date__year=current_year-2, date__month=6,home_id=query).aggregate(Sum('dailyConS'))
        jun3 = DayLog.objects.filter(date__year=current_year-3, date__month=6,home_id=query).aggregate(Sum('dailyConS'))
        jun4 = DayLog.objects.filter(date__year=current_year-4, date__month=6,home_id=query).aggregate(Sum('dailyConS'))

        jul0 = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query).aggregate(Sum('dailyConS'))
        jul1 = DayLog.objects.filter(date__year=current_year-1, date__month=7, home_id=query).aggregate(Sum('dailyConS'))
        jul2 = DayLog.objects.filter(date__year=current_year-2, date__month=7, home_id=query).aggregate(Sum('dailyConS'))
        jul3 = DayLog.objects.filter(date__year=current_year-3, date__month=7, home_id=query).aggregate(Sum('dailyConS'))
        jul4 = DayLog.objects.filter(date__year=current_year-4, date__month=7, home_id=query).aggregate(Sum('dailyConS'))

        aug0 = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query).aggregate(Sum('dailyConS'))
        aug1 = DayLog.objects.filter(date__year=current_year-1, date__month=8,home_id=query).aggregate(Sum('dailyConS'))
        aug2 = DayLog.objects.filter(date__year=current_year-2, date__month=8,home_id=query).aggregate(Sum('dailyConS'))
        aug3 = DayLog.objects.filter(date__year=current_year-3, date__month=8,home_id=query).aggregate(Sum('dailyConS'))
        aug4 = DayLog.objects.filter(date__year=current_year-4, date__month=8,home_id=query).aggregate(Sum('dailyConS'))

        sep0 = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query).aggregate(Sum('dailyConS'))
        sep1 = DayLog.objects.filter(date__year=current_year-1, date__month=9,home_id=query).aggregate(Sum('dailyConS'))
        sep2 = DayLog.objects.filter(date__year=current_year-2, date__month=9,home_id=query).aggregate(Sum('dailyConS'))
        sep3 = DayLog.objects.filter(date__year=current_year-3, date__month=9,home_id=query).aggregate(Sum('dailyConS'))
        sep4 = DayLog.objects.filter(date__year=current_year-4, date__month=9,home_id=query).aggregate(Sum('dailyConS'))

        oct0 = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query).aggregate(Sum('dailyConS'))
        oct1 = DayLog.objects.filter(date__year=current_year-1, date__month=10, home_id=query).aggregate(Sum('dailyConS'))
        oct2 = DayLog.objects.filter(date__year=current_year-2, date__month=10, home_id=query).aggregate(Sum('dailyConS'))
        oct3 = DayLog.objects.filter(date__year=current_year-3, date__month=10, home_id=query).aggregate(Sum('dailyConS'))
        oct4 = DayLog.objects.filter(date__year=current_year-4, date__month=10, home_id=query).aggregate(Sum('dailyConS'))

        nov0 = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query).aggregate(Sum('dailyConS'))
        nov1 = DayLog.objects.filter(date__year=current_year-1, date__month=11,home_id=query).aggregate(Sum('dailyConS'))
        nov2 = DayLog.objects.filter(date__year=current_year-2, date__month=11,home_id=query).aggregate(Sum('dailyConS'))
        nov3 = DayLog.objects.filter(date__year=current_year-3, date__month=11,home_id=query).aggregate(Sum('dailyConS'))
        nov4 = DayLog.objects.filter(date__year=current_year-4, date__month=11,home_id=query).aggregate(Sum('dailyConS'))

        des0 = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query).aggregate(Sum('dailyConS'))
        des1 = DayLog.objects.filter(date__year=current_year-1, date__month=12,home_id=query).aggregate(Sum('dailyConS'))
        des2 = DayLog.objects.filter(date__year=current_year-2, date__month=12,home_id=query).aggregate(Sum('dailyConS'))
        des3 = DayLog.objects.filter(date__year=current_year-3, date__month=12,home_id=query).aggregate(Sum('dailyConS'))
        des4 = DayLog.objects.filter(date__year=current_year-4, date__month=12,home_id=query).aggregate(Sum('dailyConS'))

        labels = []

        label0 = [current_year]
        label1 = [current_year-1]
        label2 = [current_year-2]
        label3 = [current_year-3]
        label4 = [current_year-4]

        values0 = [
            (list(jan0.values())),
            (list(feb0.values())),
            (list(mar0.values())),
            (list(apr0.values())),
            (list(may0.values())),
            (list(jun0.values())),
            (list(jul0.values())),
            (list(aug0.values())),
            (list(sep0.values())),
            (list(oct0.values())),
            (list(nov0.values())),
            (list(des0.values()))
            ]
        
        values1 = [
            (list(jan1.values())),
            (list(feb1.values())),
            (list(mar1.values())),
            (list(apr1.values())),
            (list(may1.values())),
            (list(jun1.values())),
            (list(jul1.values())),
            (list(aug1.values())),
            (list(sep1.values())),
            (list(oct1.values())),
            (list(nov1.values())),
            (list(des1.values()))
            ]

        values2 = [
            (list(jan2.values())),
            (list(feb2.values())),
            (list(mar2.values())),
            (list(apr2.values())),
            (list(may2.values())),
            (list(jun2.values())),
            (list(jul2.values())),
            (list(aug2.values())),
            (list(sep2.values())),
            (list(oct2.values())),
            (list(nov2.values())),
            (list(des2.values()))
            ]

        values3 = [
            (list(jan3.values())),
            (list(feb3.values())),
            (list(mar3.values())),
            (list(apr3.values())),
            (list(may3.values())),
            (list(jun3.values())),
            (list(jul3.values())),
            (list(aug3.values())),
            (list(sep3.values())),
            (list(oct3.values())),
            (list(nov3.values())),
            (list(des3.values()))
            ]

        values4 = [
            (list(jan4.values())),
            (list(feb4.values())),
            (list(mar4.values())),
            (list(apr4.values())),
            (list(may4.values())),
            (list(jun4.values())),
            (list(jul4.values())),
            (list(aug4.values())),
            (list(sep4.values())),
            (list(oct4.values())),
            (list(nov4.values())),
            (list(des4.values()))
            ]

        data = {
            'labels': ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Des"],
            'label0': label0,
            'label1': label1,
            'label2': label2,
            'label3': label3,
            'label4': label4,
            'values0': values0,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4
        }

        return JsonResponse(data)

class YearSavedChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        jan0 = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query).aggregate(Sum('dailySave'))
        jan1 = DayLog.objects.filter(date__year=current_year-1, date__month=1, home_id=query).aggregate(Sum('dailySave'))
        jan2 = DayLog.objects.filter(date__year=current_year-2, date__month=1, home_id=query).aggregate(Sum('dailySave'))
        jan3 = DayLog.objects.filter(date__year=current_year-3, date__month=1, home_id=query).aggregate(Sum('dailySave'))
        jan4 = DayLog.objects.filter(date__year=current_year-4, date__month=1, home_id=query).aggregate(Sum('dailySave'))

        feb0 = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query).aggregate(Sum('dailySave'))
        feb1 = DayLog.objects.filter(date__year=current_year-1, date__month=2,home_id=query).aggregate(Sum('dailySave'))
        feb2 = DayLog.objects.filter(date__year=current_year-2, date__month=2,home_id=query).aggregate(Sum('dailySave'))
        feb3 = DayLog.objects.filter(date__year=current_year-3, date__month=2,home_id=query).aggregate(Sum('dailySave'))
        feb4 = DayLog.objects.filter(date__year=current_year-4, date__month=2,home_id=query).aggregate(Sum('dailySave'))

        mar0 = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query).aggregate(Sum('dailySave'))
        mar1 = DayLog.objects.filter(date__year=current_year-1, date__month=3,home_id=query).aggregate(Sum('dailySave'))
        mar2 = DayLog.objects.filter(date__year=current_year-2, date__month=3,home_id=query).aggregate(Sum('dailySave'))
        mar3 = DayLog.objects.filter(date__year=current_year-3, date__month=3,home_id=query).aggregate(Sum('dailySave'))
        mar4 = DayLog.objects.filter(date__year=current_year-4, date__month=3,home_id=query).aggregate(Sum('dailySave'))

        apr0 = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query).aggregate(Sum('dailySave'))
        apr1 = DayLog.objects.filter(date__year=current_year-1, date__month=4, home_id=query).aggregate(Sum('dailySave'))
        apr2 = DayLog.objects.filter(date__year=current_year-2, date__month=4, home_id=query).aggregate(Sum('dailySave'))
        apr3 = DayLog.objects.filter(date__year=current_year-3, date__month=4, home_id=query).aggregate(Sum('dailySave'))
        apr4 = DayLog.objects.filter(date__year=current_year-4, date__month=4, home_id=query).aggregate(Sum('dailySave'))

        may0 = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query).aggregate(Sum('dailySave'))
        may1 = DayLog.objects.filter(date__year=current_year-1, date__month=5,home_id=query).aggregate(Sum('dailySave'))
        may2 = DayLog.objects.filter(date__year=current_year-2, date__month=5,home_id=query).aggregate(Sum('dailySave'))
        may3 = DayLog.objects.filter(date__year=current_year-3, date__month=5,home_id=query).aggregate(Sum('dailySave'))
        may4 = DayLog.objects.filter(date__year=current_year-4, date__month=5,home_id=query).aggregate(Sum('dailySave'))

        jun0 = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query).aggregate(Sum('dailySave'))
        jun1 = DayLog.objects.filter(date__year=current_year-1, date__month=6,home_id=query).aggregate(Sum('dailySave'))
        jun2 = DayLog.objects.filter(date__year=current_year-2, date__month=6,home_id=query).aggregate(Sum('dailySave'))
        jun3 = DayLog.objects.filter(date__year=current_year-3, date__month=6,home_id=query).aggregate(Sum('dailySave'))
        jun4 = DayLog.objects.filter(date__year=current_year-4, date__month=6,home_id=query).aggregate(Sum('dailySave'))

        jul0 = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query).aggregate(Sum('dailySave'))
        jul1 = DayLog.objects.filter(date__year=current_year-1, date__month=7, home_id=query).aggregate(Sum('dailySave'))
        jul2 = DayLog.objects.filter(date__year=current_year-2, date__month=7, home_id=query).aggregate(Sum('dailySave'))
        jul3 = DayLog.objects.filter(date__year=current_year-3, date__month=7, home_id=query).aggregate(Sum('dailySave'))
        jul4 = DayLog.objects.filter(date__year=current_year-4, date__month=7, home_id=query).aggregate(Sum('dailySave'))

        aug0 = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query).aggregate(Sum('dailySave'))
        aug1 = DayLog.objects.filter(date__year=current_year-1, date__month=8,home_id=query).aggregate(Sum('dailySave'))
        aug2 = DayLog.objects.filter(date__year=current_year-2, date__month=8,home_id=query).aggregate(Sum('dailySave'))
        aug3 = DayLog.objects.filter(date__year=current_year-3, date__month=8,home_id=query).aggregate(Sum('dailySave'))
        aug4 = DayLog.objects.filter(date__year=current_year-4, date__month=8,home_id=query).aggregate(Sum('dailySave'))

        sep0 = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query).aggregate(Sum('dailySave'))
        sep1 = DayLog.objects.filter(date__year=current_year-1, date__month=9,home_id=query).aggregate(Sum('dailySave'))
        sep2 = DayLog.objects.filter(date__year=current_year-2, date__month=9,home_id=query).aggregate(Sum('dailySave'))
        sep3 = DayLog.objects.filter(date__year=current_year-3, date__month=9,home_id=query).aggregate(Sum('dailySave'))
        sep4 = DayLog.objects.filter(date__year=current_year-4, date__month=9,home_id=query).aggregate(Sum('dailySave'))

        oct0 = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query).aggregate(Sum('dailySave'))
        oct1 = DayLog.objects.filter(date__year=current_year-1, date__month=10, home_id=query).aggregate(Sum('dailySave'))
        oct2 = DayLog.objects.filter(date__year=current_year-2, date__month=10, home_id=query).aggregate(Sum('dailySave'))
        oct3 = DayLog.objects.filter(date__year=current_year-3, date__month=10, home_id=query).aggregate(Sum('dailySave'))
        oct4 = DayLog.objects.filter(date__year=current_year-4, date__month=10, home_id=query).aggregate(Sum('dailySave'))

        nov0 = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query).aggregate(Sum('dailySave'))
        nov1 = DayLog.objects.filter(date__year=current_year-1, date__month=11,home_id=query).aggregate(Sum('dailySave'))
        nov2 = DayLog.objects.filter(date__year=current_year-2, date__month=11,home_id=query).aggregate(Sum('dailySave'))
        nov3 = DayLog.objects.filter(date__year=current_year-3, date__month=11,home_id=query).aggregate(Sum('dailySave'))
        nov4 = DayLog.objects.filter(date__year=current_year-4, date__month=11,home_id=query).aggregate(Sum('dailySave'))

        des0 = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query).aggregate(Sum('dailySave'))
        des1 = DayLog.objects.filter(date__year=current_year-1, date__month=12,home_id=query).aggregate(Sum('dailySave'))
        des2 = DayLog.objects.filter(date__year=current_year-2, date__month=12,home_id=query).aggregate(Sum('dailySave'))
        des3 = DayLog.objects.filter(date__year=current_year-3, date__month=12,home_id=query).aggregate(Sum('dailySave'))
        des4 = DayLog.objects.filter(date__year=current_year-4, date__month=12,home_id=query).aggregate(Sum('dailySave'))

        labels = []

        label0 = [current_year]
        label1 = [current_year-1]
        label2 = [current_year-2]
        label3 = [current_year-3]
        label4 = [current_year-4]

        values0 = [
            (list(jan0.values())),
            (list(feb0.values())),
            (list(mar0.values())),
            (list(apr0.values())),
            (list(may0.values())),
            (list(jun0.values())),
            (list(jul0.values())),
            (list(aug0.values())),
            (list(sep0.values())),
            (list(oct0.values())),
            (list(nov0.values())),
            (list(des0.values()))
            ]
        
        values1 = [
            (list(jan1.values())),
            (list(feb1.values())),
            (list(mar1.values())),
            (list(apr1.values())),
            (list(may1.values())),
            (list(jun1.values())),
            (list(jul1.values())),
            (list(aug1.values())),
            (list(sep1.values())),
            (list(oct1.values())),
            (list(nov1.values())),
            (list(des1.values()))
            ]

        values2 = [
            (list(jan2.values())),
            (list(feb2.values())),
            (list(mar2.values())),
            (list(apr2.values())),
            (list(may2.values())),
            (list(jun2.values())),
            (list(jul2.values())),
            (list(aug2.values())),
            (list(sep2.values())),
            (list(oct2.values())),
            (list(nov2.values())),
            (list(des2.values()))
            ]

        values3 = [
            (list(jan3.values())),
            (list(feb3.values())),
            (list(mar3.values())),
            (list(apr3.values())),
            (list(may3.values())),
            (list(jun3.values())),
            (list(jul3.values())),
            (list(aug3.values())),
            (list(sep3.values())),
            (list(oct3.values())),
            (list(nov3.values())),
            (list(des3.values()))
            ]

        values4 = [
            (list(jan4.values())),
            (list(feb4.values())),
            (list(mar4.values())),
            (list(apr4.values())),
            (list(may4.values())),
            (list(jun4.values())),
            (list(jul4.values())),
            (list(aug4.values())),
            (list(sep4.values())),
            (list(oct4.values())),
            (list(nov4.values())),
            (list(des4.values()))
            ]

        data = {
            'labels': ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Des"],
            'label0': label0,
            'label1': label1,
            'label2': label2,
            'label3': label3,
            'label4': label4,
            'values0': values0,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4
        }

        return JsonResponse(data)

class YearSolarChart(APIView):

    def get(self, request, format=None):

        current_year = datetime.datetime.now().year

        query = self.request.GET.get('q') 

        jan0 = DayLog.objects.filter(date__year=current_year, date__month=1, home_id=query).aggregate(Sum('dailySolar'))
        jan1 = DayLog.objects.filter(date__year=current_year-1, date__month=1, home_id=query).aggregate(Sum('dailySolar'))
        jan2 = DayLog.objects.filter(date__year=current_year-2, date__month=1, home_id=query).aggregate(Sum('dailySolar'))
        jan3 = DayLog.objects.filter(date__year=current_year-3, date__month=1, home_id=query).aggregate(Sum('dailySolar'))
        jan4 = DayLog.objects.filter(date__year=current_year-4, date__month=1, home_id=query).aggregate(Sum('dailySolar'))

        feb0 = DayLog.objects.filter(date__year=current_year, date__month=2,home_id=query).aggregate(Sum('dailySolar'))
        feb1 = DayLog.objects.filter(date__year=current_year-1, date__month=2,home_id=query).aggregate(Sum('dailySolar'))
        feb2 = DayLog.objects.filter(date__year=current_year-2, date__month=2,home_id=query).aggregate(Sum('dailySolar'))
        feb3 = DayLog.objects.filter(date__year=current_year-3, date__month=2,home_id=query).aggregate(Sum('dailySolar'))
        feb4 = DayLog.objects.filter(date__year=current_year-4, date__month=2,home_id=query).aggregate(Sum('dailySolar'))

        mar0 = DayLog.objects.filter(date__year=current_year, date__month=3,home_id=query).aggregate(Sum('dailySolar'))
        mar1 = DayLog.objects.filter(date__year=current_year-1, date__month=3,home_id=query).aggregate(Sum('dailySolar'))
        mar2 = DayLog.objects.filter(date__year=current_year-2, date__month=3,home_id=query).aggregate(Sum('dailySolar'))
        mar3 = DayLog.objects.filter(date__year=current_year-3, date__month=3,home_id=query).aggregate(Sum('dailySolar'))
        mar4 = DayLog.objects.filter(date__year=current_year-4, date__month=3,home_id=query).aggregate(Sum('dailySolar'))

        apr0 = DayLog.objects.filter(date__year=current_year, date__month=4, home_id=query).aggregate(Sum('dailySolar'))
        apr1 = DayLog.objects.filter(date__year=current_year-1, date__month=4, home_id=query).aggregate(Sum('dailySolar'))
        apr2 = DayLog.objects.filter(date__year=current_year-2, date__month=4, home_id=query).aggregate(Sum('dailySolar'))
        apr3 = DayLog.objects.filter(date__year=current_year-3, date__month=4, home_id=query).aggregate(Sum('dailySolar'))
        apr4 = DayLog.objects.filter(date__year=current_year-4, date__month=4, home_id=query).aggregate(Sum('dailySolar'))

        may0 = DayLog.objects.filter(date__year=current_year, date__month=5,home_id=query).aggregate(Sum('dailySolar'))
        may1 = DayLog.objects.filter(date__year=current_year-1, date__month=5,home_id=query).aggregate(Sum('dailySolar'))
        may2 = DayLog.objects.filter(date__year=current_year-2, date__month=5,home_id=query).aggregate(Sum('dailySolar'))
        may3 = DayLog.objects.filter(date__year=current_year-3, date__month=5,home_id=query).aggregate(Sum('dailySolar'))
        may4 = DayLog.objects.filter(date__year=current_year-4, date__month=5,home_id=query).aggregate(Sum('dailySolar'))

        jun0 = DayLog.objects.filter(date__year=current_year, date__month=6,home_id=query).aggregate(Sum('dailySolar'))
        jun1 = DayLog.objects.filter(date__year=current_year-1, date__month=6,home_id=query).aggregate(Sum('dailySolar'))
        jun2 = DayLog.objects.filter(date__year=current_year-2, date__month=6,home_id=query).aggregate(Sum('dailySolar'))
        jun3 = DayLog.objects.filter(date__year=current_year-3, date__month=6,home_id=query).aggregate(Sum('dailySolar'))
        jun4 = DayLog.objects.filter(date__year=current_year-4, date__month=6,home_id=query).aggregate(Sum('dailySolar'))

        jul0 = DayLog.objects.filter(date__year=current_year, date__month=7, home_id=query).aggregate(Sum('dailySolar'))
        jul1 = DayLog.objects.filter(date__year=current_year-1, date__month=7, home_id=query).aggregate(Sum('dailySolar'))
        jul2 = DayLog.objects.filter(date__year=current_year-2, date__month=7, home_id=query).aggregate(Sum('dailySolar'))
        jul3 = DayLog.objects.filter(date__year=current_year-3, date__month=7, home_id=query).aggregate(Sum('dailySolar'))
        jul4 = DayLog.objects.filter(date__year=current_year-4, date__month=7, home_id=query).aggregate(Sum('dailySolar'))

        aug0 = DayLog.objects.filter(date__year=current_year, date__month=8,home_id=query).aggregate(Sum('dailySolar'))
        aug1 = DayLog.objects.filter(date__year=current_year-1, date__month=8,home_id=query).aggregate(Sum('dailySolar'))
        aug2 = DayLog.objects.filter(date__year=current_year-2, date__month=8,home_id=query).aggregate(Sum('dailySolar'))
        aug3 = DayLog.objects.filter(date__year=current_year-3, date__month=8,home_id=query).aggregate(Sum('dailySolar'))
        aug4 = DayLog.objects.filter(date__year=current_year-4, date__month=8,home_id=query).aggregate(Sum('dailySolar'))

        sep0 = DayLog.objects.filter(date__year=current_year, date__month=9,home_id=query).aggregate(Sum('dailySolar'))
        sep1 = DayLog.objects.filter(date__year=current_year-1, date__month=9,home_id=query).aggregate(Sum('dailySolar'))
        sep2 = DayLog.objects.filter(date__year=current_year-2, date__month=9,home_id=query).aggregate(Sum('dailySolar'))
        sep3 = DayLog.objects.filter(date__year=current_year-3, date__month=9,home_id=query).aggregate(Sum('dailySolar'))
        sep4 = DayLog.objects.filter(date__year=current_year-4, date__month=9,home_id=query).aggregate(Sum('dailySolar'))

        oct0 = DayLog.objects.filter(date__year=current_year, date__month=10, home_id=query).aggregate(Sum('dailySolar'))
        oct1 = DayLog.objects.filter(date__year=current_year-1, date__month=10, home_id=query).aggregate(Sum('dailySolar'))
        oct2 = DayLog.objects.filter(date__year=current_year-2, date__month=10, home_id=query).aggregate(Sum('dailySolar'))
        oct3 = DayLog.objects.filter(date__year=current_year-3, date__month=10, home_id=query).aggregate(Sum('dailySolar'))
        oct4 = DayLog.objects.filter(date__year=current_year-4, date__month=10, home_id=query).aggregate(Sum('dailySolar'))

        nov0 = DayLog.objects.filter(date__year=current_year, date__month=11,home_id=query).aggregate(Sum('dailySolar'))
        nov1 = DayLog.objects.filter(date__year=current_year-1, date__month=11,home_id=query).aggregate(Sum('dailySolar'))
        nov2 = DayLog.objects.filter(date__year=current_year-2, date__month=11,home_id=query).aggregate(Sum('dailySolar'))
        nov3 = DayLog.objects.filter(date__year=current_year-3, date__month=11,home_id=query).aggregate(Sum('dailySolar'))
        nov4 = DayLog.objects.filter(date__year=current_year-4, date__month=11,home_id=query).aggregate(Sum('dailySolar'))

        des0 = DayLog.objects.filter(date__year=current_year, date__month=12,home_id=query).aggregate(Sum('dailySolar'))
        des1 = DayLog.objects.filter(date__year=current_year-1, date__month=12,home_id=query).aggregate(Sum('dailySolar'))
        des2 = DayLog.objects.filter(date__year=current_year-2, date__month=12,home_id=query).aggregate(Sum('dailySolar'))
        des3 = DayLog.objects.filter(date__year=current_year-3, date__month=12,home_id=query).aggregate(Sum('dailySolar'))
        des4 = DayLog.objects.filter(date__year=current_year-4, date__month=12,home_id=query).aggregate(Sum('dailySolar'))

        labels = []

        label0 = [current_year]
        label1 = [current_year-1]
        label2 = [current_year-2]
        label3 = [current_year-3]
        label4 = [current_year-4]

        values0 = [
            (list(jan0.values())),
            (list(feb0.values())),
            (list(mar0.values())),
            (list(apr0.values())),
            (list(may0.values())),
            (list(jun0.values())),
            (list(jul0.values())),
            (list(aug0.values())),
            (list(sep0.values())),
            (list(oct0.values())),
            (list(nov0.values())),
            (list(des0.values()))
            ]
        
        values1 = [
            (list(jan1.values())),
            (list(feb1.values())),
            (list(mar1.values())),
            (list(apr1.values())),
            (list(may1.values())),
            (list(jun1.values())),
            (list(jul1.values())),
            (list(aug1.values())),
            (list(sep1.values())),
            (list(oct1.values())),
            (list(nov1.values())),
            (list(des1.values()))
            ]

        values2 = [
            (list(jan2.values())),
            (list(feb2.values())),
            (list(mar2.values())),
            (list(apr2.values())),
            (list(may2.values())),
            (list(jun2.values())),
            (list(jul2.values())),
            (list(aug2.values())),
            (list(sep2.values())),
            (list(oct2.values())),
            (list(nov2.values())),
            (list(des2.values()))
            ]

        values3 = [
            (list(jan3.values())),
            (list(feb3.values())),
            (list(mar3.values())),
            (list(apr3.values())),
            (list(may3.values())),
            (list(jun3.values())),
            (list(jul3.values())),
            (list(aug3.values())),
            (list(sep3.values())),
            (list(oct3.values())),
            (list(nov3.values())),
            (list(des3.values()))
            ]

        values4 = [
            (list(jan4.values())),
            (list(feb4.values())),
            (list(mar4.values())),
            (list(apr4.values())),
            (list(may4.values())),
            (list(jun4.values())),
            (list(jul4.values())),
            (list(aug4.values())),
            (list(sep4.values())),
            (list(oct4.values())),
            (list(nov4.values())),
            (list(des4.values()))
            ]

        data = {
            'labels': ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Des"],
            'label0': label0,
            'label1': label1,
            'label2': label2,
            'label3': label3,
            'label4': label4,
            'values0': values0,
            'values1': values1,
            'values2': values2,
            'values3': values3,
            'values4': values4
        }

        return JsonResponse(data)

    

