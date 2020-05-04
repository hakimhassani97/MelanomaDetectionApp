from django.shortcuts import render
from .models import User

def index(request):
    users = User.objects.order_by('-date')[:5]
    context = {
        'users': users,
    }
    return render(request, 'index.html', context)