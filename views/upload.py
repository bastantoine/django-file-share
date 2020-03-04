#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from django.shortcuts import render

from ..forms import UploadFileForm
from .base import BaseView


class UploadFileView(BaseView):

    def get(self, request):
        context = {
            'form': UploadFileForm()
        }
        return render(request, 'file_explorer/upload.html', context=context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.filename = request.FILES['uploaded_file'].name
            uploaded_file.save()
            context = {
                'uuid': uploaded_file.uuid
            }
            return render(request, 'file_explorer/upload_successful.html', context=context)
        else:
            return render(request, 'file_explorer/upload_error.html')
