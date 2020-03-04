#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from .base import BaseView


class ProtectedView(BaseView):
    pass


class AdminView(ProtectedView):

    def get(self, request):
        context = {
            'all_files': UploadedFile.objects.filter(available__exact=True)
        }
        return render(request, 'file_explorer/admin.html', context=context)
