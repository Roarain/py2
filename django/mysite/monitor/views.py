# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect
from . import models
import hashlib
# Create your views here.


def hash_password(request,password):
    hash_md5 = hashlib.md5()
    hash_md5.update(password)
    password = hash_md5.hexdigest()
    return password


def valid_login(func):
    def inner(request,*arg,**kwargs):
        try:
            request.session['username']
        except Exception as e:
            return redirect('/monitor/login')
        else:
            session_user = request.session['username']
            if models.UserInfo.objects.filter(username=session_user):
                return func(request)
            else:
                return redirect('/monitor/error')
    return inner
@valid_login
def index(request):
    return render(request, 'monitor_index.html')

def base(request):
    return render(request, 'monitor_base.html')
@valid_login
def table(request):

    # hostname_list = models.ServerInfo.objects.all().hostname
    # ip_list = models.ServerInfo.objects.all().ip
    # manager_list = models.ServerInfo.objects.all().manager
    # phone_list = models.ServerInfo.objects.all().phone
    # email_list = models.ServerInfo.objects.all().email
    # return render(request, 'table.html',{'hostname_list':hostname_list,'ip_list':ip_list,'manager_list':manager_list,'phone_list':phone_list,'email_list':email_list})
    serverinfo_list = models.ServerInfo.objects.all()
    return render(request,'table.html',{'serverinfo_list':serverinfo_list})


def login(request):
    print request.POST
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = hash_password(request,request.POST.get('password'))
        print 'Username is: %s Password is: %s' % (username,password)
        if models.UserInfo.objects.filter(username=username,password=password):
            # return HttpResponse('User %s Login Success...' % (username))
            request.session['username'] = username
            return redirect('/monitor/table/')
        else:
            # return HttpResponse('User %s Login Faild...' % (username))
            return redirect('/monitor/error/')
    return render(request,'login.html')

def error(request):
    return render(request,'error.html')

def monitor_register(request):
    if request.method == 'POST' and request.POST:
        print 'Post Data is: %s,Post Type is: %s' % (request.POST,type(request.POST))
        username = request.POST.get('inputUsername')
        password = hash_password(request,request.POST.get('inputPassword'))
        phone = request.POST.get('inputMobileNum')
        email = request.POST.get('inputEmail')

        if models.UserInfo.objects.filter(username=username):
            return HttpResponse('User: %s is alread exist...')
        else:
            models.UserInfo.objects.create(username=username, password=password, phone=phone, email=email)
            return render(request,'monitor_register_post_data.html',{'data':request.POST})
    return render(request,'monitor_register.html')






