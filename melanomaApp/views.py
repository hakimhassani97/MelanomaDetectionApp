import cv2
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files import File
from django.contrib.auth import authenticate, login as doLogin
from django.contrib.auth.decorators import user_passes_test
from .models import Doctor, Caracteristic as Car, Image, Patient, Details ,Note
from .forms import UploadImageForm, LoginForm, RegisterForm, UserRegisterForm, AddPatientForm,AddNoteForm
from .detector.Caracteristics import Caracteristics
from .detector.utils.Caracteristics import Caracteristics as Cars
from .detector.utils.Contours import Contours
from .detector.utils.Preprocess import Preprocess
import shutil
import os

def checkDoctorIsLoggedIn(user):
    '''
        checks if the doctor is logged in and active
    '''
    return user.is_authenticated and hasattr(user, 'doctor') and user.doctor!=None

def forms(request):
    users = Doctor.objects.order_by('-date')[:5]
    context = {
        'users': users,
    }
    return render(request, 'forms.html', context)

@user_passes_test(checkDoctorIsLoggedIn, login_url='/login')
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
        if form.is_valid():
            # multiple Images
            files = request.FILES.getlist('image')
            for f in files:
                i = Image(name=form.cleaned_data['name'], image=f, patient=form.cleaned_data['patient'])
                i.save()                
                if 'compute' in request.POST:
                    # image caracteristics
                    car = Caracteristics.extractCaracteristics(i.image.path)
                    car = Car(**car, image=i)
                    car.save()
                    # image details
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    contour = Contours.contours2(img)
                    # extractLesion
                    img = Cars.extractLesion(img, contour)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_extract.')
                    cv2.imwrite(imgPath, img)
                    det = Details(image=i)
                    with open(imgPath, 'rb') as dest:
                        # name = i.image.name.replace('.','_extract.')
                        name = imgPath.replace('media/images/','')
                        det.extract.save(name, File(dest), save=False)
                    # remove temporary files
                    # shutil.rmtree(imgPath, ignore_errors=True)
                    os.remove(imgPath)
                    det.save()
                    
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

def updatePatient(request,patientId):
    '''
        Update Patient
    '''
   
    return render(request, 'updatePatient.html')



def patientsList(request):
    '''
        returns a list of all Patients
    '''
    patients = Patient.objects.all()
    context = {
        'patients': patients,
    }
    return render(request, 'patientsList.html', context)



def preparation(request,imgId):
    '''
        returns preparation
    '''
    
    details=Details.objects.raw('SELECT * FROM melanomaApp_details WHERE image_id  = %s',[imgId])[0]
    
    context = {
        
        'details': details,
    }

    return render(request, 'preparation.html',context)
    

def asymmetry(request):
    '''
        returns asymmetry
    '''
    return render(request, 'asymmetry.html')

def border(request):
    '''
        returns border
    '''
    return render(request, 'border.html')

def color(request):
    '''
        returns color
    '''
    return render(request, 'color.html')


def diameter(request):
    '''
        returns diameter
    '''
    return render(request, 'diameter.html')


def addNote(request):
    '''
        Add Note
    '''
    msg = None
    success = False
    add =False
    if request.method == "POST":
        form = AddNoteForm(request.POST, request.FILES)
        if form.is_valid():
            Note = form.save(commit=False)
            Note.save()
            msg = 'Note est enregistrée avec succes'
            success = True
            add =True  
            return redirect(notesList)
        else:
            msg = 'Verifiez les champs'
            return render(request, 'addNote.html', {"form": form, "msg": msg, "success": success})
    else:
        form = AddNoteForm()
        return render(request, 'addNote.html', {'form': form})




def notesList(request):
    '''
        returns noteList
    '''
    notes = Note.objects.order_by('-date')
    context = {
        'notes': notes,
    }
    return render(request, 'notesList.html', context)


def deleteNote(request,noteId):
    '''
        delete note
    '''
    note = Note.objects.get(id=noteId)
    note.delete()
    return redirect(notesList)




def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)
