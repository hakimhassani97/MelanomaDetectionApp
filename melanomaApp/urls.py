from django.urls import path
from django.conf.urls.static import static
from application import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadImg', views.uploadImg, name='uploadImg'),
    path('images', views.images, name='images'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forms.html', views.forms, name='forms'),
    path('addPatient', views.addPatient, name='addPatient'),
    path('patientsList', views.patientsList, name='patientsList'),
    path('preparation/<int:imgId>', views.preparation, name='preparation'),
    path('asymmetry', views.asymmetry, name='asymmetry'),
    path('border', views.border, name='border'),
    path('color', views.color, name='color'),
    path('diameter', views.diameter, name='diameter'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
