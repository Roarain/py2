# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

class ServerInfoAdmin(admin.ModelAdmin):
    # list_display = ('hostname','ip','manager','phone','email')
    list_display = ('hostname','ip')
    list_per_page = 2
    search_fields = ('hostname','ip')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username','email','phone')
    search_fields = ('username','email','phone')

admin.site.register(models.ServerInfo,ServerInfoAdmin)
admin.site.register(models.UserInfo,UserInfoAdmin)
