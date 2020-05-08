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
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)