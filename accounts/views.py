from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAdminUser
from django.views.generic import TemplateView

# Create your views here.

@login_required
def home(request):
    args = {'user': request.user}
    if User.is_superuser:
        return render(request, 'home/home_page.html', args)

    else:
        return HttpResponse('Not admin user')

    
