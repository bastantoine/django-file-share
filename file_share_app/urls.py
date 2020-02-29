from django.urls import path

from .views import (
    HomeView,
    GetFileView,
    AdminView,
    UploadFileView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin', AdminView.as_view(), name='admin'),
    path('get', GetFileView.as_view(), name='get'),
    path('upload', UploadFileView.as_view(), name='upload'),
]
