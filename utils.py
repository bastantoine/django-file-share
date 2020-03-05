#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

from functools import wraps

from django.shortcuts import redirect
from django.utils.http import urlencode


def requires_auth(view_func):
    @wraps(view_func)
    def decorated(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            _redirect = redirect('file_share:login')
            next_page = urlencode({'next': request.path})
            _redirect['Location'] += '?%s' % next_page
            return _redirect
        return view_func(request, *args, **kwargs)
    return decorated