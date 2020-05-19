from django import forms
from .models import Image, Doctor,Patient,Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(forms.Form):
    '''
        Doctor login form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Username","class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password","class": "form-control"}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Username","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email","class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password","class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password check","class": "form-control"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RegisterForm(forms.ModelForm):
    '''
        Doctor registration form
    '''
    image = forms.ImageField(widget=forms.FileInput(attrs={"placeholder" : "Image","class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Phone","class": "form-control"}))
    class Meta:
        model = Doctor
        fields = ['phone', 'image']


class ChangeUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Username","class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email","class": "form-control"}))
    class Meta:
        model = User
        fields = ('username', 'email')


class ChangePassword(UserCreationForm) :
    oldpassword =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Old Password","class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password","class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password check","class": "form-control"}))
    class Meta:
        model = User
        fields = ('oldpassword', 'password1', 'password2')






class UploadImageForm(forms.ModelForm):
    '''
        Image lesion upload form
    '''
    name = forms.CharField(max_length=30, required=False)
    patient = forms.ModelChoiceField(Patient.objects.all())
    class Meta:
        model = Image
        fields = ['patient', 'name', 'image']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control-file'
        self.fields['image'].widget.attrs['multiple'] = True
        self.fields['patient'].widget.attrs['class'] = 'form-control'

class AddPatientForm(forms.ModelForm):
    '''
        Add Patient form
    '''
    firstName = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "First Name","class": "form-control","type":"text"}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Last Name","class": "form-control","type":"text"}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email","class": "form-control","email":"email" }))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Phone","class": "form-control"}))
    birthDate = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d', attrs={"placeholder" : "Birth Date","class": "form-control" ,"type" :"Date"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Address","class": "form-control","type":"text"}))
    CHOICES = (('', 'Sexe'),('male', 'Male'),('femelle', 'Femelle'))
    sexe = forms.ChoiceField(choices=CHOICES ,widget=forms.Select(attrs={"placeholder" : "Sexe","class": "form-control"}))
    class Meta:
        model = Patient
        fields = ('firstName', 'lastName','email','phone','birthDate','address', 'sexe')

class AddNoteForm(forms.ModelForm):
    '''
        Add Note form
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Titre","class": "form-control","type":"text"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder" : "Contenu","class": "form-control","rows":5,}))
    class Meta:
        model = Note
        fields = ('title', 'content')
