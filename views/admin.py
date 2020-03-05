#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

import os

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.utils.decorators import method_decorator

from .base import BaseView
from ..models import UploadedFile
from ..utils import requires_auth


class ProtectedView(BaseView):
    
    @method_decorator(requires_auth)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AdminView(ProtectedView):

    def get(self, request):
        context = {
            'all_files': UploadedFile.objects.filter(available__exact=True)
        }
        return render(request, 'file_explorer/admin.html', context=context)

class DeleteFileView(ProtectedView):

    def get(self, request, uuid):
        uploaded_file = get_object_or_404(UploadedFile, uuid__exact=uuid)
        # We should uploaded_file.name, and not uploaded_file.file.name, as the
        # late one will need to open the file to get the name, which will cause
        # trouble in case the file itself was removed from the disk and the DB
        # not properly cleaned. The first one is not an absolute path to the file,
        # but we can build it using settings.UPLOAD_ROOT
        splitted = uploaded_file.uploaded_file.name.split('/')
        year, month, day, filename = splitted[-4:]
        root_folder = os.path.join(settings.UPLOAD_ROOT, *splitted[:-4])
        try:
            os.remove(os.path.join(root_folder, year, month, day, filename))
        except FileNotFoundError:
            # Perhaps the file itself is already removed and the DB not properly
            # cleaned. Anyway, this shouldn't bother us.
            pass
        folders = [year, month, day]
        for i in range(len(folders)):
            # This way we start by the further folder,
            # and go higher one folder at a time
            path = os.path.join(root_folder, *folders[i:], '')
            if len(os.listdir(path)) > 0:
                # The current folder is not empty, so no need to
                # delete it and we don't need to go any higher
                break
            os.rmdir(path)
        uploaded_file.delete()
        return redirect('file_explorer:admin')
