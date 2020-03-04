#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

import mimetypes
import os
import datetime

import magic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.conf import settings

from .models import UploadedFile
from .forms import UploadFileForm


class BaseView(View):
    pass


class ProtectedView(BaseView):
    pass


class HomeView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/home.html')


class AdminView(ProtectedView):

    def get(self, request):
        context = {
            'all_files': UploadedFile.objects.filter(available__exact=True)
        }
        return render(request, 'file_explorer/admin.html', context=context)


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

class GetFileView(BaseView):

    def guess_mime_type_encoding(self, file_path):
        dummy, encoding = mimetypes.guess_type(file_path)
        # From https://medium.com/@ajrbyers/file-mime-types-in-django-ee9531f3035b
        mime = magic.from_file(file_path, mime=True)
        return (mime, encoding)

    def get_response_from_file(self, file):
        mimetype, encoding = self.guess_mime_type_encoding(
            os.path.join(settings.UPLOAD_ROOT, file.uploaded_file.name)
        )
        if not mimetype:
            mimetype = 'application/octet-stream'
        response = HttpResponse(
            file.uploaded_file.read(),
            content_type=mimetype,
        )
        response['Content-Disposition'] = 'attachment; filename="%s"' % file.filename
        return response

    def get_file(self, uuid):
        file = get_object_or_404(UploadedFile, uuid__exact=uuid)
        if file.limit_time != datetime.datetime.now():
            return None
        return file

    def get(self, request, uuid):
        file = self.get_file(uuid)
        if not file:
            return render(request, 'file_explorer/file_out_of_date.html')
        if file.password:
            return render(request, 'file_explorer/file_login.html')
        return self.get_response_from_file(file)

    def post(self, request, uuid):
        file = self.get_file(uuid)
        if not file:
            return render(request, 'file_explorer/file_out_of_date.html')
        if file.password:
            if (not request.POST or not request.POST.get('password') or
                not file.password == request.POST.get('password')):
                return render(request, 'file_explorer/file_login.html')
        return self.get_response_from_file(file)
