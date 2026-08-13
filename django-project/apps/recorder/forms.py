# coding=utf-8
from django import forms
from django.forms import ModelForm
from .models import VoiceCategoryModel

class VoiceCategoryForm(forms.ModelForm):
    class Meta:
        model = VoiceCategoryModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            placeholder_text = field.label or field_name.replace("_", " ").title()
            field.widget.attrs.update(
                {
                    "class": "w3-input",
                    "placeholder": f"Enter {placeholder_text}"
                }
            )
