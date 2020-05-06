from django import forms
from .models import Image

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['imgName', 'image']
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['imgName'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control-file'