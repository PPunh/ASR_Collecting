# coding=utf-8
from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator
from smart_selects.db_fields import ChainedForeignKey
from crum import get_current_user

class ProvinceModel(models.Model):
    name = models.CharField(
        max_length = 20,
        unique = True,
        verbose_name = "Province"
    )

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.name

class DistrictModel(models.Model):
    province = models.ForeignKey(
        ProvinceModel,
        on_delete = models.CASCADE,
        related_name = "districts",
        verbose_name = "Province"
    )
    name = models.CharField(
        max_length = 30,
        verbose_name = "District",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"

    def __str__(self):
        return self.name


class PersonalInfoModel(models.Model):
    name = models.CharField(
        max_length = 60,
        verbose_name = "Name"
    )
    sur_name = models.CharField(
        max_length = 60,
        blank=True, null=True,
        verbose_name = "Sur Name",
    )
    province = models.ForeignKey(
        ProvinceModel,
        on_delete = models.CASCADE,
        blank=True, null=True,
        verbose_name = "Province"
    )
    district = models.ForeignKey(
        DistrictModel,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="District"
    )
    village = models.CharField(
        max_length = 30,
        verbose_name = "Village"
    )

    class Meta:
        abstract = True



# Abstract audit table
class AuditModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        blank=True, null=True,
        related_name = "%(class)s_created_by",
        verbose_name = "Created By"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name = "Created At"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        blank=True, null=True,
        related_name = "%(class)s_modified_by",
        verbose_name = "Modified By"
    )
    modified_at = models.DateTimeField(
        auto_now = True,
        verbose_name = "Modified At"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ Enhance save method with autometically created_by and modified_by """
        user = kwargs.pop('user', None)

        if not user:
            user = get_current_user()

        # Set created_by
        if not self.pk and user and user.is_authenticated:
            self.created_by = user

        # Aways update modified_by when user is available
        if user and user.is_authenticated:
            self.modified_by = user

        super().save(*args, **kwargs)


class CodeGenerationModel(models.Model):
    """
    Auto Generate a uqinue code for each model
    """
    code = models.CharField(
        max_length = 20,
        unique = True,
        blank = True, null=True,
        verbose_name = "Code"
    )

    class Meta:
        abstract = True

    def generate_code(self, prefix=None, start_code = 1):
        if not self.code:
            if not prefix:
                # Default prefix from class name if not provided
                prefix = self.__class__.__name__.upper()[:3]

            with transaction.atomic():
                # Lock the table to prevent race conditions
                last_obj = self.__class__.objects.select_for_update().order_by('code').first()
                if last_obj and last_obj.code:
                    try:
                        # Assumes code format is PRE-NUMBER
                        content = last_obj.code.split("-")[-1]
                        last_code = int(content)
                        new_code = last_code + 1
                    except (ValueError, IndexError):
                        new_code = start_code

                else:
                    new_code = start_code
                self.code = f"{prefix} - {new_code}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        super().save(*args, **kwargs)