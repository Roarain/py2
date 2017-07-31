"""mysite URL Configuration

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
from app01 import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'index',views.index),
    url(r'articles/([1-2][0-9]{3})',views.articles_year),
    url(r'article_find/(?P<year>[1-2][0-9]{3})/(?P<month>[0-9]{1}|1[0-2]{1})',views.article_find),
    url(r'host',views.host),
    # url(r'test',views.test),
    url(r'register',views.register),
    url(r'add_book',views.add_book),
    url(r'book_form',views.book_form),
    url(r'book_model_form',views.book_model_form),
    url(r'filter/(\w+)',views.filter),
    url(r'mem/(\w+)',views.mem),
    # url(r'^$|.*?',views.index),
]
