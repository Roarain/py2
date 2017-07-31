# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=128,verbose_name='作者')
    email = models.EmailField(verbose_name='邮箱')

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=128,verbose_name='出版社名称',unique=True)
    address = models.CharField(max_length=128,verbose_name='出版社地址')
    city = models.CharField(max_length=128, verbose_name='出版社城市')
    country = models.CharField(max_length=128, verbose_name='出版社国家')
    website = models.URLField(max_length=64,verbose_name='出版社网址')

    def __unicode__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=128,verbose_name='书名')
    author = models.ManyToManyField('Author',verbose_name='作者')
    publisher = models.ForeignKey('Publisher',verbose_name='出版社名称')
    publish_date = models.DateField(verbose_name='出版日期')

    def __unicode__(self):
        return self.name
