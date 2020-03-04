#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from django.forms import ModelForm
from .models import UploadedFile


class UploadFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['uploaded_file', 'password', 'limit_time']
