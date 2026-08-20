# coding=utf-8
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model inherited from default Django AUTH User model"""
    # Custom Permission
    class PermissionChoice(models.TextChoices):
        USERS = 'users', 'Users'
        AUTHENTICATORS = 'authenticators', 'Authenticators'
        SUPERADMIN = 'superadmin', 'SuperAdmin'

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
    role = models.CharField(
        max_length=20,
        choices=PermissionChoice.choices,
        default=PermissionChoice.USERS,
        verbose_name="ROLE"
    )

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"

    def is_superadmin(self):
        """Super Admin has full access"""
        return self.is_superuser or self.role == self.PermissionChoice.SUPERADMIN

    def is_authenticator(self):
        """Authenticator can review/verify voice recording status"""
        return self.is_superadmin() or self.role == self.PermissionChoice.AUTHENTICATORS

    def is_normal_user(self):
        """Normal user can only record and listen"""
        return not self.is_superadmin() and not self.is_authenticator()

    def save(self, *args, **kwargs):
        if self.role == self.PermissionChoice.SUPERADMIN:
            self.is_superuser = True

        self.is_staff = self.is_superuser

        super().save(*args, **kwargs)
