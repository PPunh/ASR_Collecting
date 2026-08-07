# coding=utf-8
from django.contrib import admin
from .models import EmployiesModel

@admin.register(EmployiesModel)
class EmployiesAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "sur_name"]
    search_fields = ["code", "name", "sur_name"]
    readonly_fields = ["code", "created_by", "created_at", "modified_by", "modified_at"]