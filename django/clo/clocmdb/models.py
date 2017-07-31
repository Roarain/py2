# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True,editable=False,verbose_name='用户ID')
    username = models.CharField(unique=True,max_length=128,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=20,verbose_name='电话')
    isdelete = models.CharField(max_length=4,default='N',verbose_name='是否删除')
    current_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.username

class Server(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='服务器ID')
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=128,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    protocal_choice = (
        ('SSH','SSH'),
        ('RDP','RDP'),
    )
    protocal = models.CharField(max_length=10,choices=protocal_choice,verbose_name='远程连接类型')
    # active_choice = (
    #     ('Y','激活'),
    #     ('N','未激活'),
    # )
    # isActive = models.CharField(max_length=2,choices=active_choice,verbose_name='是否激活')
    isdelete = models.CharField(max_length=4, default='N', verbose_name='是否删除')
    current_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ip

class ServerDetail(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='信息编号ID')
    server_id = models.IntegerField(verbose_name='服务器ID')
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.IntegerField(verbose_name='端口')
    os_info = models.CharField(max_length=128,verbose_name='操作系统信息')
    cpu_info = models.CharField(max_length=128,verbose_name='CPU信息')
    cpu_count = models.IntegerField(verbose_name='CPU个数')
    mem_info = models.CharField(max_length=20, verbose_name='内存大小')
    disk_info = models.CharField(max_length=20,verbose_name='硬盘大小')
    isdelete = models.CharField(max_length=4, default='N', verbose_name='是否删除')
    current_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ip


class UserServer(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='信息编号ID')
    user_id = models.IntegerField(verbose_name='用户ID')
    username = models.CharField(max_length=128, verbose_name='用户名')
    server_id = models.IntegerField(verbose_name='服务器ID')
    server_ip = models.GenericIPAddressField(verbose_name='IP地址')
    isdelete = models.CharField(max_length=4, default='N', verbose_name='是否删除')
    current_time = models.DateTimeField(auto_now=True)


class SendCodes(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    username = models.CharField(max_length=128, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    emailcode = models.CharField(max_length=20, verbose_name='邮箱验证码')
    isdelete = models.CharField(max_length=4, default='N', verbose_name='是否删除')
    current_time = models.DateTimeField(auto_now=True)