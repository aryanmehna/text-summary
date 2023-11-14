from django import forms 
from .models import UploadedPDF


class UploadedPDFForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['pdf_file']