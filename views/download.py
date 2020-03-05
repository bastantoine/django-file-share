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

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from ..models import UploadedFile
from .base import BaseView


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
        if datetime.date.today() > file.limit_time:
            return None
        return file

    def get(self, request, uuid):
        file = self.get_file(uuid)
        if not file:
            return render(request, 'file_share/file_out_of_date.html')
        if file.password:
            return render(request, 'file_share/file_login.html')
        return self.get_response_from_file(file)

    def post(self, request, uuid):
        file = self.get_file(uuid)
        if not file:
            return render(request, 'file_share/file_out_of_date.html')
        if file.password:
            if (not request.POST or not request.POST.get('password') or
                not file.password == request.POST.get('password')):
                return render(request, 'file_share/file_login.html')
        return self.get_response_from_file(file)
