# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('id','name','publisher','publish_date')
    search_fields = ('name','publisher__name','publish_date')
    list_filter = ('name','publisher')
    list_editable = ('name','publisher','publish_date')
    list_per_page = 3
    # filter_horizontal = ('author',)
    filter_vertical = ('author',)
    # raw_id_fields = ('publisher',)
    date_hierarchy = ('publish_date')

class BookAuthor(admin.ModelAdmin):
    list_display = ('name','email')


admin.site.register(models.Author,BookAuthor)
admin.site.register(models.Publisher)
admin.site.register(models.Book,BookAdmin)