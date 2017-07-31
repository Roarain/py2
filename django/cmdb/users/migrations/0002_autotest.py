# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoTest',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='users.Base')),
                ('auto_id', models.AutoField(primary_key=True, serialize=False, verbose_name='\u6d4b\u8bd5ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u7528\u6237\u540d')),
                ('age', models.IntegerField(verbose_name='\u5e74\u9f84')),
            ],
            bases=('users.base',),
        ),
    ]
