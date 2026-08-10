# coding=utf-8
from django.db import models
from apps.common.models import AuditModel
from django.conf import settings

class VoiceRecordingModel(AuditModel, models.Model):
    # Verify Status
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    audio_file = models.FileField(
        upload_to="recording/%Y/%m/%d/",
        verbose_name="Audio File"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Title"
    )
    
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Status"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Note / Comments"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_recordings",
        verbose_name="Reviewed By"
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Reviewed At"
    )

    def __str__(self):
        return f"{self.title} Recording {self.id}"