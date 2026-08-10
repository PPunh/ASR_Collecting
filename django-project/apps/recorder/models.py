# coding=utf-8
from django.db import models
from apps.common.models import AuditModel

class VoiceRecordingModel(AuditModel, models.Model):
    audio_file = models.FileField(
        upload_to = "recording/%Y/%m/%d/",
        verbose_name = "Audio File"
    )
    title = models.CharField(
        max_length=255,
        verbose_name = "Title"
    )

    def __str__(self):
        return f"{self.title} Recording {self.id}"