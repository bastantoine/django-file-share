from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Do not forget to set UPLOAD_ROOT and UPLOAD_URL inside you settings file
upload_storage = FileSystemStorage(
    location=settings.UPLOAD_ROOT,
    base_url=settings.UPLOAD_URL
)
