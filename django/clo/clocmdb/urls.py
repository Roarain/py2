"""clo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^test',views.test),
    url(r'^register/',views.register),
    url(r'^check_regist_duplicate_user/', views.check_regist_duplicate_user),
    url(r'^login/', views.login),
    url(r'^captcha/',views.captcha),
    # url(r'^index/', views.index),
    url(r'^server_register/',views.server_register),
    url(r'^server_list/', views.server_list),
    url(r'^server_detail/(\d+)/', views.server_detail),
    url(r'^service_list/(\d+)/', views.service_list),
    url(r'^service_control/(\d+)/(\w+)/(\w+)/', views.service_control),
    url(r'^password_forget_sendmail/',views.password_forget_sendmail),
    url(r'^findpassword/',views.findpassword),
    url(r'^password_emailcode_verify/',views.password_emailcode_verify),
    url(r'^password_update/',views.password_update),
    url(r'^server_monitor/(\d+)/',views.server_monitor),
    url(r'^monitor_zabbix/(\d+)/',views.monitor_zabbix),
    url(r'^zabbix_monitor/(\d+)/(\d+)/',views.zabbix_monitor),
]
