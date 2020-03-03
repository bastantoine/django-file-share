from os.path import join

from django.core.files.storage import FileSystemStorage
from django.conf import settings


# Do not forget to set UPLOAD_ROOT and UPLOAD_URL inside you settings file
upload_storage = FileSystemStorage(
    location=settings.UPLOAD_ROOT,
    base_url=join('file_explorer', settings.UPLOAD_URL)
)
