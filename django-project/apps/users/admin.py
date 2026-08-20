# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

from . import models
from . import forms


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    model = models.User

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Personal Info", {"fields": ("phone_number",)}),
        ("ROLE", {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Personal Info", {"fields": ("phone_number",)}),
        ("ROLE", {"fields": ("role",)}),
    )

    def display_modified(self, obj): # display modified in local time
        if obj.date_modified:
            return timezone.localtime(obj.date_modified).strftime('%Y-%m-%d %H:%M')
        return "-"

    display_modified.short_description = "Modified"

    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'display_modified','modified_by')
