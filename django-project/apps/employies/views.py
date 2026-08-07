# coding=utf-8
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from apps.common.mixins import SearchFilterMixin, MultipleInlineFormsetMixin
from .models import EmployiesModel
from .forms import EmployiesForm
from apps.users.models import User
from apps.users.forms import CustomUserCreationForm

class EmployiesListView(SearchFilterMixin, ListView):
	model = EmployiesModel
	template_name = "employies/list.html"
	context_object_name = "items"
	list_display = ["code", "name", "sur_name", "province", "district", "village"]
	base_urlname = "employies"
	search_fields = ["code", "name", "sur_name"]

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = "Employies"
		context['topic'] = "All Employies"
		return context

class EmployiesCreateView(MultipleInlineFormsetMixin, CreateView):
	model = User
	form_class = CustomUserCreationForm
	template_name = "employies/add.html"
	inline_formsets = [
		{
			'model': EmployiesModel,
            'form': EmployiesForm,
            'extra': 1,
            'can_delete': False,
            'formset_name': 'employee_formset',
		}
	]

	def get_success_url(self):
		messages.success(
			self.request,
			"Create new user successfully"
		)
		return reverse(
			"employies:list"
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Add new user"
		return context