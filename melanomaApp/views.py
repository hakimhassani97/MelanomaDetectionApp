from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Doctor, Caracteristic as Car, Image
from .forms import UploadImageForm
from .detector.Caracteristics import Caracteristics

def forms(request):
    users = Doctor.objects.order_by('-date')[:5]
    context = {
        'users': users,
    }
    return render(request, 'forms.html', context)

def index(request):
    users = Doctor.objects.order_by('-date')[:5]
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
            # multiple Images
            files = request.FILES.getlist('image')
            for f in files:
                i = Image(imgName=form.cleaned_data['imgName'], image=f)
                i.save()
                car = Caracteristics.extractCaracteristics(i.image.path)
                car = Car(**car)
                car.save()
            # one Image
            # f = form.save()
            # car = Caracteristics.extractCaracteristics(f.image.path)
            # car = Car(**car)
            # car.save()
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