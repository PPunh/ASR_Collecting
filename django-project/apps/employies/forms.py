# coding=utf-8
from django import forms
from django.forms import ModelForm
from django_select2.forms import ModelSelect2Widget
from smart_selects.form_fields import ChainedModelChoiceField
from .models import EmployiesModel

class DistrictWidget(ModelSelect2Widget):
    search_fields = ['name__icontains']
    dependent_fields = {'province': 'province'}

class EmployiesForm(forms.ModelForm):
    class Meta:
        model = EmployiesModel
        exclude = ["created_at", "created_by", "modified_at", "modified_by", "code"]
        widgets = {
            'district': DistrictWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # if ChainedSelect skip modify widget.attrs
            if isinstance(field, ChainedModelChoiceField):
                continue

            placeholder_text = field.label or field_name.replace("_", " ").title()
            
            field.widget.attrs.update(
                {
                    "class": "w3-input",
                    "placeholder": f"Enter {placeholder_text}"
                }
            )