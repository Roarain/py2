# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.

def index(request):
    html_content = '<h1> This is Forum Index Page...'
    return HttpResponse(html_content)