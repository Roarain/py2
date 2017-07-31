# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.


def index(request):
    html_content = '<h1> This is Blog Index Page ...'
    return HttpResponse(html_content)

def base(request):
    return render(request,'base.html')

def base_ref(request):
    return render(request,'base_ref.html')