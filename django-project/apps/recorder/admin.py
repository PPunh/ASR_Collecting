# coding=utf-8
from django.contrib import admin
from .models import VoiceRecordingModel, VoiceCategoryModel

@admin.register(VoiceCategoryModel)
class VoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(VoiceRecordingModel)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("category", "title","audio_file")
