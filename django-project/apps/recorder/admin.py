# coding=utf-8
from django.contrib import admin
from .models import VoiceRecordingModel, VoiceCategoryModel, VoiceTaskModel

@admin.register(VoiceCategoryModel)
class VoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(VoiceTaskModel)
class VoiceTaskAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "script")

@admin.register(VoiceRecordingModel)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("category", "task", "title","audio_file")
