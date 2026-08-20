from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .backends import MultiAuthBackend

from . import models
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ("email", "phone_number", "role", "is_superuser")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'class': 'w3-input',
                    'placeholder': f"Enter {field.label}..."
                }
            )