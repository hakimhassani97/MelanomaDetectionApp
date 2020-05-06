from django.urls import path
from django.conf.urls.static import static
from application import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadImg', views.uploadImg, name='uploadImg'),
    path('images', views.images, name='images'),
    path('forms.html', views.forms, name='forms'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)