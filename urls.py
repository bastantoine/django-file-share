from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    HomeView,
    GetFileView,
    AdminView,
    UploadFileView
)

app_name = 'file_explorer'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin', AdminView.as_view(), name='admin'),
    path('upload', UploadFileView.as_view(), name='upload'),
    path('l/<uuid:uuid>', GetFileView.as_view(), name='get'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
