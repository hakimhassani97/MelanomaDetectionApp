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
from .detector.utils.Game import Game
import shutil
import imutils
import os
import numpy as np

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
                    ######################## extractLesion
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
                    ######################## draw contour
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    img = cv2.drawContours(img, [contour], -1, (255, 255, 255), 2)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_contour.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.contour.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    ######################## draw circle
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    Contours.boundingCircle(img, contour)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_circle.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.circle.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    ######################## draw rect
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    Contours.boundingRectangleRotated(img, contour)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_rect.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.rect.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    ######################## draw homologue
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    img = Preprocess.removeArtifactYUV(img)
                    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                    x, y, w, h = cv2.boundingRect(contour)
                    rect = img[y:y + h, x:x + w]
                    rotated = imutils.rotate_bound(rect, 180)
                    # intersection between rect and rotated (search)
                    intersection = cv2.bitwise_and(rect, rotated)
                    # img = np.zeros(img.shape)
                    # img = np.add(img, 255)
                    # img[y:y + h, x:x + w] = intersection
                    img = intersection
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_homologue.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.homologue.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    ######################## draw preprocess
                    img = cv2.imread(i.image.path, cv2.IMREAD_COLOR)
                    img = Preprocess.removeArtifactYUV(img)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_preprocess.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.preprocess.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    det.save()

                    ######################## draw segmentation
                    img = cv2.drawContours(img, [contour], -1, (255,0, 255), 2)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_segmentation.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.segmentation.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    det.save()
                    
                    ################### draw PostTraitement
                    
                    img = Cars.extractLesion(img, contour)
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_posttraitement.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.posttraitement.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    det.save()

                    ################## draw enclosingCircle
                    tmp =img
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(img, center, radius=1, color=(0, 255, 255), thickness=1)
                    cv2.circle(img, center, radius=radius, color=(0,255, 0), thickness=1)     
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_enclosingCircle.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.enclosingCircle.save(name, File(dest), save=False)
                    # remove temporary files
                    os.remove(imgPath)
                    det.save()
                    
                    ################## draw openCircle
                    img =tmp 
                    perimeter = cv2.arcLength(contour, True)
                    M = cv2.moments(contour)
                    x = int(M["m10"] / M["m00"])
                    y = int(M["m01"] / M["m00"])
                    radius = int(perimeter / (2 * np.pi))
                    cv2.circle(img, (x,y), radius=1, color=(0, 255, 255), thickness=1)
                    cv2.circle(img, (x,y), radius=radius, color=(0,255, 0), thickness=1)     
                    imgPath = 'media/'+i.image.name
                    imgPath = imgPath.replace('.', '_openCircle.')
                    cv2.imwrite(imgPath, img)
                    with open(imgPath, 'rb') as dest:
                        name = imgPath.replace('media/images/','')
                        det.openCircle.save(name, File(dest), save=False)
                    # remove temporary files
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

def results(request, imgId):
    '''
        returns table of caracteristics of the image
    '''
    image = Image.objects.get(id=imgId)
    a = [image.caracteristic.car0, image.caracteristic.car1, image.caracteristic.car2, image.caracteristic.car3,
        image.caracteristic.car4, image.caracteristic.car5]
    b = [image.caracteristic.car6, image.caracteristic.car7, image.caracteristic.car8, image.caracteristic.car9, image.caracteristic.car10,
        image.caracteristic.car11, image.caracteristic.car12, image.caracteristic.car13]
    c = [image.caracteristic.car14, image.caracteristic.car15, image.caracteristic.car16, image.caracteristic.car17, image.caracteristic.car18]
    d = [image.caracteristic.car19, image.caracteristic.car20, image.caracteristic.car21]
    thresholdsPH2 = np.array([[2.65, 92.87, 6.39, 13.2, 17.2, 15.44], [55.73, 1560, 0.02, 0.56, 1.81, 1.35, 219, 1], [5, 2, 5, 9.51, 63.69], [560, 572.24, 4.54]])
    thresholdsISIC = np.array([[4.23, 93.61, 7.31, 12.28, 16.17, 10.18], [73.42, 900, 0.02, 0.71, 1.37, 1.2, 145, 1.6], [3, 2, 3, 10.25, 66.93], [342, 323.27, 3.63]])
    opsPH2 = np.array([[0, 1, 0, 0, 0, 0], [1, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1], [0, 0, 0]])
    opsISIC = np.array([[0, 1, 0, 0, 0, 0], [1, 0, 1, 1, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0]])
    # c[0:3] = np.array(c).astype(int)[0:3]
    # c[0] = str(c[0])+' couleurs'
    # c[1] = str(c[1])+' couleurs'
    # c[2] = str(c[2])+' couleurs'
    cars = [{'vals':a, 'name':'Asymmetry'}, {'vals':b, 'name':'Border'}, {'vals':c, 'name':'Color'}, {'vals':d, 'name':'Diameter'}]
    thead = '<thead><tr><th class="bg-warning">Caracteristique</th>'
    for m in range(1, 9):
        thead += '<th style="background-color:lightgrey">Méthode '+str(m)+'</th>'
    thead += '</tr></thead>'
    tbody = '<tbody>'
    for i in range(len(cars)):
        car = cars[i]
        tbody +='<tr><td style="background-color:rgb(255, 200, 160)">'+car['name']+'</td>'
        for j in range(len(car['vals'])):
            m = car['vals'][j]
            if (opsPH2[i][j]==0 and m<thresholdsPH2[i][j]) or (opsPH2[i][j]==1 and m>=thresholdsPH2[i][j]):
                tbody += '<td class="bg-success">'+str(m)+'</td>'
            else:
                if (opsPH2[i][j]==1 and m<thresholdsPH2[i][j]) or (opsPH2[i][j]==0 and m>=thresholdsPH2[i][j]):
                    tbody += '<td class="bg-danger">'+str(m)+'</td>'
        for j in range(len(car['vals'])+1, 9):
            tbody += '''
            <td><div>
                <div style="width: 40px;height: 47px;border-bottom: 1px solid black;
                -webkit-transform: translateY(-20px) translateX(5px) rotate(27deg);"></div>
            </div></td>
            '''
        tbody += '</tr>'
    tbody += '</tbody>'
    # image sample
    T = np.array(a+b+c+d)
    result = Game.getResult(T)
    context = {
        'image': image,
        'table': thead+tbody,
        'class': 'Melanome' if result==1 else 'Non Melanome'
    }
    return render(request, 'results.html', context)

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
    img = Image.objects.get(id=imgId)
    # details=Details.objects.raw('SELECT * FROM melanomaApp_details WHERE image_id  = %s',[imgId])[0]
    details = img.details
    
    context = {
        'img': img,
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
