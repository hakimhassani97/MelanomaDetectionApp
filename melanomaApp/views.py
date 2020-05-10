from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as doLogin
from .models import Doctor, Caracteristic as Car, Image, Patient
from .forms import UploadImageForm, LoginForm, RegisterForm, UserRegisterForm, AddPatientForm
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
# auth views


def login(request):
    '''
        Doctor login view
    '''
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                doLogin(request, user)
                return redirect("/")
            else:
                msg = 'Email ou mot de passe incorrectes'
        else:
            msg = 'Erreur lors de validation du formulaire'
    return render(request, "auth/login.html", {"form": form, "msg": msg})


def register(request):
    '''
        Doctor registration view
    '''
    msg = None
    success = False
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        userform = UserRegisterForm(request.POST)
        if form.is_valid() and userform.is_valid():
            # save the User, and the Doctor
            user = userform.save(commit=False)
            user.is_active = False
            user.save()
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            username = userform.cleaned_data.get("username")
            raw_password = userform.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'Compte Cree avec succes, veuillez attendre notre validation'
            success = True
            # return redirect("/login/")
        else:
            msg = 'Verifiez les champs'
    else:
        form = RegisterForm()
        userform = UserRegisterForm()
    return render(request, "auth/register.html", {"form": form, "userform": userform, "msg": msg, "success": success})


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
                i = Image(name=form.cleaned_data['name'], image=f)
                i.save()
                if 'compute' in request.POST:
                    car = Caracteristics.extractCaracteristics(i.image.path)
                    car = Car(**car)
                    car.save()
            # one Image
            # f = form.save()
            # car = Caracteristics.extractCaracteristics(f.image.path)
            # car = Car(**car)
            # car.save()
            form = UploadImageForm()
            return render(request, 'uploadImg.html', {'form': form, 'success': True})
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


def addPatient(request):
    '''
        Add Patient
    '''
    msg = None
    success = False
    if request.method == "POST":
        form = AddPatientForm(request.POST, request.FILES)
        if form.is_valid():
            Patient = form.save(commit=False)
            Patient.save()
            msg = 'Le Patient est enregistrée avec succes'
            success = True
            # return redirect("/login/")
            return render(request, 'addPatient.html', {"form": form, "msg": msg, "success": success})
        else:
            msg = 'Verifiez les champs'
            return render(request, 'addPatient.html', {"form": form, "msg": msg, "success": success})
    else:
        form = AddPatientForm()
        return render(request, 'addPatient.html', {'form': form})


def patientsList(request):
    '''
        returns a list of all Patients
    '''
    patients = Patient.objects.all()
    context = {
        'patients': patients,
    }
    return render(request, 'patientsList.html', context)


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)
