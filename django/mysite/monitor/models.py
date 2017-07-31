# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ServerInfo(models.Model):
    hostname = models.CharField(max_length=128,verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    manager = models.CharField(max_length=128,verbose_name='联系人')
    phone = models.IntegerField(verbose_name='电话号码')
    email = models.EmailField(verbose_name='邮箱')

    def __unicode__(self):
        return self.hostname

class UserInfo(models.Model):
    username = models.CharField(max_length=128,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.IntegerField(verbose_name='电话')

    def __unicode__(self):
        return self.username