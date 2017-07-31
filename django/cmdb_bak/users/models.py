# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Base(models.Model):
    delete_flag = models.CharField(max_length=10, verbose_name='是否被删除')

class User(Base):
    username = models.CharField(max_length=128,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.IntegerField(verbose_name='电话')

    def __unicode__(self):
        return self.username

class Group(Base):
    groupname = models.CharField(max_length=128,verbose_name='组名称')
    description = models.TextField(verbose_name='组描述')

    def __unicode__(self):
        return self.groupname


class Permission(Base):
    groupname = models.CharField(max_length=128,verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述')

    def __unicode__(self):
        return self.groupname

class UserGroup(Base):
    user_id = models.IntegerField(verbose_name='用户ID')
    group_id = models.IntegerField(verbose_name='组ID')

    def __unicode__(self):
        return self.user_id

class UserPermission(Base):
    user_id = models.IntegerField(verbose_name='用户ID')
    permission_id = models.IntegerField(verbose_name='权限ID')

    def __unicode__(self):
        return self.user_id

class PermissionGroup(Base):
    group_id = models.IntegerField(verbose_name='组ID')
    permission_id = models.IntegerField(verbose_name='权限ID')

    def __unicode__(self):
        return self.group_id

class Server(Base):
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=128,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    protocal_choice = (
        ('SSH','SSH'),
        ('RDP','RDP'),
    )
    protocal = models.CharField(max_length=10,choices=protocal_choice,verbose_name='远程连接类型')
    active_choice = (
        ('Y','激活'),
        ('N','未激活'),
    )
    isActive = models.CharField(max_length=2,choices=active_choice,verbose_name='是否激活')

    def __unicode__(self):
        return self.ip

class ServerDetail(Base):
    server_id = models.IntegerField(verbose_name='服务器ID')
    os_info = models.CharField(max_length=128,verbose_name='操作系统信息')
    cpu_info = models.CharField(max_length=128,verbose_name='CPU信息')
    cpu_count = models.IntegerField(verbose_name='CPU个数')
    mem_info = models.CharField(max_length=20, verbose_name='内存大小')
    disk_info = models.CharField(max_length=20,verbose_name='硬盘大小')


class UserServer(Base):
    user_id = models.IntegerField(verbose_name='用户ID')
    server_id = models.IntegerField(verbose_name='服务器ID')

class AutoTest(Base):
    auto_id = models.AutoField(primary_key=True,verbose_name='测试ID')
    name = models.CharField(max_length=128,verbose_name='用户名')
    age = models.IntegerField(verbose_name='年龄')

    def __unicode__(self):
        return self.name

class Test1(models.Model):
    user_id = models.AutoField(primary_key=True,verbose_name='测试ID')
    name = models.CharField(max_length=128,verbose_name='用户名')
    def __unicode__(self):
        return self.name

class CPUstat(Base):
    cpu_percent = models.CharField(max_length=10,verbose_name='CPU使用率')
    curr_time = models.CharField(max_length=128,verbose_name='当前时间')

class CPUstat2(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    cpu_percent = models.CharField(max_length=10,verbose_name='CPU使用率')
    curr_time = models.CharField(max_length=128,verbose_name='当前时间')

class SendCode(models.Model):
    username = models.CharField(max_length=128, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    emailcode = models.CharField(max_length=20, verbose_name='邮箱验证码')
    current_time = models.DateTimeField(auto_now=True)

class SendCodes(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    username = models.CharField(max_length=128, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    emailcode = models.CharField(max_length=20, verbose_name='邮箱验证码')
    current_time = models.DateTimeField(auto_now=True)

