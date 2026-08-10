# coding=utf-8
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model inherited from default Django AUTH User model"""

    phone_regex = RegexValidator(
        regex=r"^\d{8}$",
        message="Phone number must be 8 digits.",
    )

    phone_number = models.CharField(
        max_length=8,
        unique=True,
        validators=[phone_regex],
        error_messages={"unique": "A user with that phone number already exists."}
    )

    email = models.EmailField(
        max_length=60,
        unique=True,
        error_messages={"unique": "A user with that email address already exists."}
    )

    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_users'
    )

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} ({self.phone_number or 'N/A'})"

    def save(self, *args, **kwargs):
        self.is_staff = self.is_superuser
        super().save(*args, **kwargs)