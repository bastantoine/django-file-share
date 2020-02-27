from django.forms import ModelForm
from .models import UploadedFile


class UploadFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['uploaded_file', 'password', 'limit_time']
