from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import transaction, models
from django.forms import inlineformset_factory
from django.db.models import Q
from django.apps import apps
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# Multipel Inline Formset Mixin
class MultipleInlineFormsetMixin:
    """
    Enhanced mixin for CreateView and UpdateView to handle multiple inline formsets.

    Usage:
    inline_formsets = [
        {
            'model': ChildModel,
            'form': ChildModelForm,
            'extra': 1,
            'can_delete': True,
            'formset_name': 'child_formset',
            'fk_name': 'parent',  # Optional: specify if auto-detection fails
        }
    ]
    """
    inline_formsets = []

    def get_model_class(self, model_config):
        """Convert string 'app.Model' to actual model class"""
        if isinstance(model_config, str):
            try:
                app_label, model_name = model_config.split('.')
                return apps.get_model(app_label, model_name)
            except ValueError:
                raise ValueError(
                    _("Model string '{model_config}' must be in format 'app_name.ModelName'").format(model_config=model_config)
                )
        return model_config

    def get_foreign_key_field(self, formset_config):
        """Find foreign key field that points from child model to parent model"""

        if 'fk_name' in formset_config:
            return formset_config['fk_name']

        model = self.get_model_class(formset_config['model'])
        parent_model = self.model
        priority_fields = ['user']
        fields = model._meta.get_fields()

        # 1. Find the OneToOneField that points to the parent first.
        for field in fields:
            if (isinstance(field, models.OneToOneField) and
                    field.related_model == parent_model and
                    hasattr(field, 'name')):
                return field.name

        # 2. Find from the field name that is defined in priority
        for name in priority_fields:
            for field in fields:
                if (hasattr(field, 'related_model') and
                        field.related_model == parent_model and
                        field.name == name):
                    return field.name

        # 3. Find another field that points to the parent, except for audit fields.
        audit_fields = ['created_by', 'updated_by', 'deleted_by']
        for field in fields:
            if (hasattr(field, 'related_model') and
                    field.related_model == parent_model and
                    hasattr(field, 'name') and
                    field.name not in audit_fields):
                return field.name

        # 4. Absolute fallback
        for field in fields:
            if (hasattr(field, 'related_model') and
                    field.related_model == parent_model and
                    hasattr(field, 'name')):
                return field.name

        raise ValueError(
            f"Could not find foreign key field in {model.__name__} "
            f"that points to {parent_model.__name__}. "
            f"Please specify 'fk_name' in your formset configuration."
        )

    def create_formset_class(self, formset_config):
        """Create formset class from config"""

        model = self.get_model_class(formset_config['model'])
        fk_name = self.get_foreign_key_field({**formset_config, 'model': model})

        factory_kwargs = dict(
            parent_model=self.model,
            model=model,
            form=formset_config.get('form'),
            extra=formset_config.get('extra', 1),
            can_delete=formset_config.get('can_delete', True),
            can_order=formset_config.get('can_order', False),
            max_num=formset_config.get('max_num', None),
            min_num=formset_config.get('min_num', None),
            validate_max=formset_config.get('validate_max', False),
            validate_min=formset_config.get('validate_min', False),
            fk_name=fk_name,
        )

        if formset_config.get('exclude'):
            factory_kwargs['exclude'] = formset_config['exclude']
        else:
            factory_kwargs['fields'] = formset_config.get('fields', '__all__')

        return inlineformset_factory(**factory_kwargs)

    def get_formset_instances(self):
        """
        Cache formset instances in self._formset_instances
        to prevent creating formset multiple times between get_context_data and form_valid
        which may cause validation state mismatch
        """
        if not hasattr(self, '_formset_instances'):
            self._formset_instances = {}
            for formset_config in self.inline_formsets:
                formset_name = formset_config.get('formset_name')
                if not formset_name:
                    raise ValueError("Each formset configuration must have a 'formset_name'")

                FormsetClass = self.create_formset_class(formset_config)

                if self.request.method == 'POST':
                    formset = FormsetClass(
                        self.request.POST,
                        self.request.FILES,
                        instance=getattr(self, 'object', None),
                    )
                else:
                    formset = FormsetClass(
                        instance=getattr(self, 'object', None),
                    )

                self._formset_instances[formset_name] = formset

        return self._formset_instances

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not self.inline_formsets:
            return data

        for formset_name, formset in self.get_formset_instances().items():
            data[formset_name] = formset

        return data

    def form_valid(self, form):
        with transaction.atomic():
            # Save main form first to get instance for formsets
            self.object = form.save()

            # Reset _formset_instances after save main form
            # Because instance changes (has pk for CreateView)
            if hasattr(self, '_formset_instances'):
                del self._formset_instances

            # Validate all formsets
            formset_instances = self.get_formset_instances()
            all_valid = all(fs.is_valid() for fs in formset_instances.values())

            if not all_valid:
                # Use render_to_response + get_context_data instead of self.form_invalid(form)
                # To ensure formset with errors are sent back to template correctly
                transaction.set_rollback(True)
                return self.render_to_response(self.get_context_data(form=form))

            # Save all formsets
            for formset in formset_instances.values():
                formset.save()

        return HttpResponseRedirect(self.get_success_url())



# Search Filter Mixins
class SearchFilterMixin:
    """
        Generic search filter mixin:
        View set:
            - model
            - search_fields:
            - status_field
            - status_choices
    """
    status_field = 'status'
    search_param = 'search'
    search_fields = []
    status_choices = []
    default_status = None
    list_display = [] # Set the fields to display in the list view

    def get_verbose_name(self, model, field_path):
        # Get verbose name from model field (Supports nested fields like 'field__subfield)
        try:
            parts = field_path.split('__')
            field = model._meta.get_field(parts[0])

            if len(parts) > 1 and field.is_relation:
                return self.get_verbose_name(field.related_model, '__'.join(parts[1:]))
            return field.verbose_name
        except Exception:
            # Return field name if not found
            return field_path.replace('__', ' ').replace('_', ' ').capitalize()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Status Filter
        status = self.request.GET.get(self.status_field) or self.default_status
        if status:
            queryset = queryset.filter(**{self.status_field: status})

        # Search Filter
        search_query = self.request.GET.get(self.search_param)
        if search_query and self.search_fields:
            q_obj = Q()
            for field in self.search_fields:
                q_obj |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_obj)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # status dropdown
        context['status_choices'] = self.status_choices
        context['current_status'] = self.request.GET.get(self.status_field) or self.default_status
        context['status_field'] = self.status_field

        # Search Filter
        context['search_param'] = self.search_param
        context['search_query'] = self.request.GET.get(self.search_param, '')

        # Create Headers for list view autometically
        if self.list_display:
            context["headers"] = [
                {
                    'field':field,
                    'label':self.get_verbose_name(self.model, field)
                }
                for field in self.list_display
            ]
        return context
