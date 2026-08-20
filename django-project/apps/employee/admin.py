# coding=utf-8
from django.contrib import admin
from .models import EmployeeModel

@admin.register(EmployeeModel)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "sur_name"]
    search_fields = ["code", "name", "sur_name"]
    readonly_fields = ["code", "created_by", "created_at", "modified_by", "modified_at"]