# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-12 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clocmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userserver',
            name='username',
            field=models.CharField(max_length=128, verbose_name='\u7528\u6237\u540d'),
        ),
    ]
