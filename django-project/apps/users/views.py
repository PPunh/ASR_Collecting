import logging
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.utils import timezone
from django.forms import inlineformset_factory
from . import forms
from . import models


logger = logging.getLogger(__name__)


@method_decorator(never_cache, name='dispatch')
@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class Login(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Welcome back, {form.get_user().username}!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Invalid username or password. Please try again."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            'users:home',
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        return context


@never_cache
@require_http_methods(["GET", "POST"])
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You have successfully logged out"
    )
    return redirect("users:login")



# @method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
def home(request):
    context = {
        'title': 'Home',
    }

    template = 'home.html'
    return render(request, template, context)
