#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from os.path import join
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Do not forget to set UPLOAD_ROOT and UPLOAD_URL inside you settings file
upload_storage = FileSystemStorage(
    location=settings.UPLOAD_ROOT,
    base_url=join('file_share', settings.UPLOAD_URL)
)
