from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.api import UserViewSet, RegisterView
from .serializers import UserSerializer

router = routers.DefaultRouter()
router.register(r'admin/users', UserViewSet)
router.register(r'register', RegisterView)

urlpatterns = [
    #url(r'^home/$', views.home, name='home'),
    #url('home/', TemplateView.as_view(template_name='home/home_page.html'), name='home_page'),
    #url(r'^login/$', login, {'template_name': 'accounts/login.html'}),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
    path('', include(router.urls)),
    path(r'auth/', include('rest_auth.urls')),
]