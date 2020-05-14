from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

class Doctor(models.Model):
    '''
        the Doctor model
    '''
    phone = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='avatars', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name = 'Doctor'
    def __str__(self):
        if self.user:
            return self.user.email
        else:
            return 'h'

class Patient(models.Model):
    '''
        the Patient model
    '''
    firstName = models.CharField(max_length=30, null=False, blank=False)
    lastName = models.CharField(max_length=30, null=False, blank=False)
    birthDate = models.DateTimeField(null=True, blank=True)     
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254,null=True, blank=True)
    sexe = models.CharField(max_length=30, null=False, blank=False, default="male")
    
    def __str__(self):
        return self.firstName+' '+self.lastName+' ('+self.phone+')'
    


class Note(models.Model):
    '''
        Note model
    '''
    title = models.CharField(max_length=254, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date = models.DateTimeField('Note date', auto_now_add=True)
    
    def __str__(self):
        return self.title +' '+self.content
    


class Image(models.Model):
    '''
        the Image model
    '''
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images', default=None)
    date = models.DateTimeField('upload date', auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    def classification(self):
        thresholdsPH2 = np.array([2.65, 92.87, 6.39, 13.2, 17.2, 15.44, 55.73, 1560, 0.02, 0.56, 1.81, 1.35, 219, 1, 5, 2, 5, 9.51, 63.69, 560, 572.24, 4.54])
        thresholdsISIC = np.array([4.23, 93.61, 7.31, 12.28, 16.17, 10.18, 73.42, 900, 0.02, 0.71, 1.37, 1.2, 145, 1.6, 3, 2, 3, 10.25, 66.93, 342, 323.27, 3.63])
        opsPH2 = np.array([0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0])
        opsISIC = np.array([0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0])
        return False
    def __str__(self):
        return self.name+' '+str(self.date)+' '+self.image.url

class Details(models.Model):
    '''
        the image Details model
    '''
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True, blank=True)
    
    ###### preparation 
    preprocess = models.ImageField(upload_to='images', null=True, blank=True)    
    segmentation = models.ImageField(upload_to='images', null=True, blank=True)   
    posttraitement = models.ImageField(upload_to='images', null=True, blank=True)
    
    ######## diametre 
    enclosingCircle = models.ImageField(upload_to='images', null=True, blank=True)    
    openCircle = models.ImageField(upload_to='images', null=True, blank=True)   
    lengtheningIndex = models.ImageField(upload_to='images', null=True, blank=True)
    

    extract = models.ImageField(upload_to='images', null=True, blank=True)
    contour = models.ImageField(upload_to='images', null=True, blank=True)
    circle = models.ImageField(upload_to='images', null=True, blank=True)
    rect = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return str(self.image)

class Caracteristic(models.Model):
    '''
        Image Caracteristic model
    '''
    car0 = models.FloatField('asymmetryByBestFitEllipse', default=0)
    car1 = models.FloatField('asymmetryByDistanceByCircle', default=0)
    car2 = models.FloatField('asymmetryIndex', default=0)
    car3 = models.FloatField('asymmetryBySubRegion', default=0)
    car4 = models.FloatField('asymmetryBySubRegionCentered', default=0)
    car5 = models.FloatField('asymmetryBySubRegionCentered2', default=0)
    car6 = models.FloatField('borderRoundness', default=0)
    car7 = models.FloatField('borderLength', default=0)
    car8 = models.FloatField('borderRegularityIndex', default=0)
    car9 = models.FloatField('borderRegularityIndexRatio', default=0)
    car10 = models.FloatField('borderCompactIndex', default=0)
    car11 = models.FloatField('borderHeywoodCircularityIndex', default=0)
    car12 = models.FloatField('borderHarrisCorner', default=0)
    car13 = models.FloatField('borderFractalDimension', default=0)
    car14 = models.FloatField('colorHSVIntervals', default=0)
    car15 = models.FloatField('colorYUVIntervals', default=0)
    car16 = models.FloatField('colorYCbCrIntervals', default=0)
    car17 = models.FloatField('colorSDG', default=0)
    car18 = models.FloatField('colorKurtosis', default=0)
    car19 = models.FloatField('diameterMinEnclosingCircle', default=0)
    car20 = models.FloatField('diameterOpenCircle', default=0)
    car21 = models.FloatField('diameterLengtheningIndex', default=0)
    date = models.DateTimeField('computing date', auto_now_add=True)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str([self.car0,self.car1,self.car2,self.car3,self.car4,self.car5,self.car6,self.car7,self.car8,self.car9,self.car10,
        self.car11,self.car12,self.car13,self.car14,self.car15,self.car16,self.car17,self.car18,self.car19,self.car20,self.car21])