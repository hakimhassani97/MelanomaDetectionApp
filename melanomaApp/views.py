from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import User, Caracteristic as Car, Image
from .forms import UploadImageForm
from .detector.Caracteristics import Caracteristics

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

def uploadImg(request):
    '''
        process the request img
    '''
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            f = form.save()
            car = Caracteristics.extractCaracteristics(f.image.path)
            car = Car(**car)
            car.save()
            form = UploadImageForm()
            return render(request, 'uploadImg.html', {'form': form, 'success':True})
            # return redirect('uploadImg')
    else:
        form = UploadImageForm()
    return render(request, 'uploadImg.html', {'form': form})

def images(request):
    '''
        returns a list of all the images
    '''
    images = Image.objects.order_by('-date')
    context = {
        'images': images,
    }
    return render(request, 'images.html', context)

def error_404(request, exception):
    data = {}
    return render(request,'404.html', data)