from django.shortcuts import render
from .models import User

def forms(request):
    users = User.objects.order_by('-date')[:5]
    context = {
        'users': users,
    }
    return render(request, 'forms.html', context)

def index(request):
    users = User.objects.order_by('-date')[:5]
    context = {
        'users': users,
    }
    return render(request, 'index.html', context)

def error_404(request, exception):
    data = {}
    return render(request,'404.html', data)