# coding=utf-8
from django.db import models
from django.conf import settings
from apps.common.models import PersonalInfoModel, AuditModel, CodeGenerationModel

class EmployiesModel(PersonalInfoModel, AuditModel, CodeGenerationModel):
    code = models.CharField(
        max_length=20,
        unique=True, blank=True, null=True,
        verbose_name = "Code",
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        blank=True, null=True,
        verbose_name = "User",
        related_name = "Personal_info"
    )

    class Meta:
        verbose_name = "Employies Information"
        verbose_name_plural = "Employies Informations"

    def __str__(self):
        return f"{self.name} - {self.sur_name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code(prefix="EMP", start_code="100001")
        super().save(*args, **kwargs)