# coding=utf-8
from django.contrib import admin
from . import models


@admin.register(models.ProvinceModel)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", )

