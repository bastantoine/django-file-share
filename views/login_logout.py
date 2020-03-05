#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*
from django.utils.http import urlencode
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages

from .base import BaseView


class LoginView(BaseView):

    def get(self, request):
        context = {}
        if request.GET.get('next'):
            context['next'] = urlencode({
                'next': request.GET.get('next'),
            })
        return render(request, 'file_explorer/login.html', context=context)

    def post(self, request):
        if not request.POST:
            return self.get(request)
        username = request.POST['username']
        password = request.POST['password']
        user = self.authenticate(request, username, password)
        if not user:
            return render(request, 'file_explorer/login.html')
        auth.login(request, user)
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('file_explorer:home')


class LogoutView(BaseView):

    def get(self, request):
        auth.logout(request)
        return redirect('file_explorer:home')
