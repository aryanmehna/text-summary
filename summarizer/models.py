from django.db import models

# Create your models here.
class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploads/')