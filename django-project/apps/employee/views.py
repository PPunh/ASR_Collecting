# coding=utf-8
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from apps.common.mixins import SearchFilterMixin, MultipleInlineFormsetMixin
from .models import EmployeeModel
from .forms import EmployeeForm
from apps.users.models import User
from apps.users.forms import CustomUserCreationForm

class EmployeeListView(SearchFilterMixin, ListView):
	model = EmployeeModel
	template_name = "employee/list.html"
	context_object_name = "items"
	list_display = ["code", "name", "sur_name", "province", "district", "village"]
	base_urlname = "employee"
	search_fields = ["code", "name", "sur_name"]

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = "Employee"
		context['topic'] = "All Employees"
		context["details_url_name"] = "employee:details"
		return context

class EmployeeCreateView(MultipleInlineFormsetMixin, CreateView):
	model = User
	form_class = CustomUserCreationForm
	template_name = "employee/add.html"
	inline_formsets = [
		{
			'model': EmployeeModel,
            'form': EmployeeForm,
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
			"employee:list"
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Add new user"
		return context


class EmployeeDetailView(DetailView):
	model = EmployeeModel
	template_name = "employee/details.html"
	context_object_name = "items"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Employee Details"
		context['topic'] = "Employee Details"
		return context