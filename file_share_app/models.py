from django.db import models


class UploadedFile(models.Model):

    uploaded_file = models.FileField(upload_to=None, max_length=100)
    password = models.CharField(max_length=20)
    limit_time = models.DateField()
    uuid = models.UUIDField()
    available = models.BooleanField()
