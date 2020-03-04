#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    HomeView,
    GetFileView,
    AdminView,
    DeleteFileView,
    UploadFileView,
)

app_name = 'file_explorer'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin', AdminView.as_view(), name='admin'),
    path('upload', UploadFileView.as_view(), name='upload'),
    path('l/<uuid:uuid>', GetFileView.as_view(), name='get'),
    path('delete/<uuid:uuid>', DeleteFileView.as_view(), name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
