# coding=utf-8
from django.contrib import admin
from .models import VoiceRecordingModel

@admin.register(VoiceRecordingModel)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("title","audio_file")