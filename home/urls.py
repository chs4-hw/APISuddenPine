from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.views import User
from . import api
from home.views import HomeProfileView, HomeWeekView, HomeMonthView, HomeYearView, SearchResultsView, InfoView, CompareListView
from home.views import WeekBatteryChart, WeekConsumptionChart, WeekSavedChart, WeekSolarChart
from home.views import MonthBatteryChart, MonthConsumptionChart, MonthSavedChart, MonthSolarChart
from home.views import YearBatteryChart, YearConsumptionChart, YearSavedChart, YearSolarChart
from home.views import CompareMonthChart, CompareMonthConsumptionChart


router = routers.DefaultRouter()

router.register('api/homestats', api.HomeStatsAPI)
router.register('api/userstats', api.UserStatsAPI)
router.register('api/daylogs', api.DayLogsAPI)
router.register('api/devices', api.DevicesAPI)
router.register('api/roomcontrol', api.RoomControlAPI)

# Imported HomeView class as the new view 

urlpatterns = [
    path('', include(router.urls)),
    url('^admin$', HomeProfileView.as_view(), name='home_page'),
    url('admin/siteinfo', InfoView.as_view(), name='info'),

    url('admin/compare_homes', CompareListView.as_view(), name='compare'),
    
    url('admin/compare/month', CompareMonthChart.as_view(), name='compare_month'),
    #url('admin/compare/month', CompareMonthConsumptionChart.as_view(), name='compare_month'),

    path('admin/', SearchResultsView.as_view(), name='search'),
    
    url('admin/homeinfo/week', HomeWeekView.as_view(), name='info_week'),
    url('admin/homeinfo/month', HomeMonthView.as_view(), name='info_month'),
    url('admin/homeinfo/year', HomeYearView.as_view(), name='info_year'),
    path('admin/battery/weekdata', WeekBatteryChart.as_view(), name='weekbattery'),
    path('admin/consumption/weekdata', WeekConsumptionChart.as_view(), name='weekconsumption'),
    path('admin/saved/weekdata', WeekSavedChart.as_view(), name='weeksaved'),
    path('admin/solar/weekdata', WeekSolarChart.as_view(), name='weeksolar'),
    path('admin/battery/monthdata', MonthBatteryChart.as_view(), name='monthbattery'),
    path('admin/consumption/monthdata', MonthConsumptionChart.as_view(), name='monthconsumption'),
    path('admin/saved/monthdata', MonthSavedChart.as_view(), name='monthsaved'),
    path('admin/solar/monthdata', MonthSolarChart.as_view(), name='monthsolar'),
    path('admin/battery/yeardata', YearBatteryChart.as_view(), name='yearbattery'),
    path('admin/consumption/yeardata', YearConsumptionChart.as_view(), name='yearconsumption'),
    path('admin/saved/yeardata', YearSavedChart.as_view(), name='yearsaved'),
    path('admin/solar/yeardata', YearSolarChart.as_view(), name='yearsolar')
    ]