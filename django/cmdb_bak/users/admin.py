# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Group)
admin.site.register(models.Permission)
admin.site.register(models.UserGroup)
admin.site.register(models.UserPermission)
admin.site.register(models.PermissionGroup)
admin.site.register(models.Server)
admin.site.register(models.ServerDetail)
admin.site.register(models.UserServer)
# admin.site.register(models.AutoTest)
admin.site.register(models.Test1)