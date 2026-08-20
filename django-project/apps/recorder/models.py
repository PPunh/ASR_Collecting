# coding=utf-8
from django.db import models
from apps.common.models import AuditModel
from django.conf import settings

# Category of Voice Recording
class VoiceCategoryModel(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = "Category",
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name = "Description"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return f"Category Name: {self.name}"

class VoiceTaskModel(AuditModel, models.Model):
    """ A recording task inside a category. Contains the title & script that
    normal users must read and record. """
    category = models.ForeignKey(
        VoiceCategoryModel,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Category"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Task Title"
    )
    script = models.TextField(
        verbose_name="Script"
    )

    class Meta:
        verbose_name = "Voice Task"
        verbose_name_plural = "Voice Tasks"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}"

class VoiceRecordingModel(AuditModel, models.Model):
    # Verify Status
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    category = models.ForeignKey(
        VoiceCategoryModel,
        on_delete = models.CASCADE,
        verbose_name = "Category",
        blank=True, null=True,
        related_name = "category"
    )
    task = models.ForeignKey(
        VoiceTaskModel,
        on_delete = models.SET_NULL,
        verbose_name = "Task",
        blank=True, null=True,
        related_name = "recordings"
    )
    audio_file = models.FileField(
        upload_to="recording/%Y/%m/%d/",
        verbose_name="Audio File"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Title"
    )
    script = models.TextField(
        blank=True, null=True,
        verbose_name = "Script"
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

    class Meta:
        verbose_name = "Voice Recording"
        verbose_name_plural = "Voice Recordings"
        permissions = [
            ("can_review_recording", "Can review and verify voice recording status (approve/reject)"),
        ]
