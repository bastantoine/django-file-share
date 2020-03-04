#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from django.shortcuts import render

from .base import BaseView


class HomeView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/home.html')
