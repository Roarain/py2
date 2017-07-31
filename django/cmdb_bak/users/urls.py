"""cmdb URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'^login/',views.login),
    url(r'^register/',views.register),
    url(r'^autojump/',views.autojump),
    url(r'^check_regist_duplicate_user/',views.check_regist_duplicate_user),
    url(r'^server_register/',views.server_register),
    url(r'^server_list/', views.server_list),
    url(r'^server_list_page/(\d*)/', views.server_list_page),
    # url(r'^server_search/(?P<ip>(.*))/(?P<port>(\d*))/', views.server_search),
    url(r'^server_search/', views.server_search),
    # url(r'^server_search_result/', views.server_search_result),
    # url(r'^sqltest/', views.sqltest),
    url(r'^server_detail/(.*)/', views.server_detail),
    url(r'^server_delete/(.*)/', views.server_delete),
    # url(r'server_monitor/(.*)',views.server_monitor),
    url(r'^server_monitor/',views.server_monitor),
    url(r'^password_forget/',views.password_forget),
    url(r'^password_forget_sendmail/',views.password_forget_sendmail),
    url(r'^sendemail/',views.sendemail),
    url(r'^password_emailcode_verify/',views.password_emailcode_verify),
    url(r'^password_update/',views.password_update),
    url(r'^jqtest/',views.jqtest),
    url(r'^logout/',views.logout),
    url(r'^captcha/',views.captcha),
    # url(r'^&|.*?',views.index),

]
