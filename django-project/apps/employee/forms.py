# coding=utf-8
from django import forms
from django.forms import ModelForm
from .models import EmployeeModel

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        exclude = ["created_at", "created_by", "modified_at", "modified_by", "code"]

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