from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.core.exceptions import PermissionDenied
from django_ratelimit.core import is_ratelimited
from django.conf import settings

# # Global Permission Required
# class AutoPermissionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # skip checking when users was'nt login or users is Admin/SuperAdmin
#         if not request.user.is_authenticated or request.user.is_superuser:
#             return self.get_response(request)
#
#         # Extrack the URL to find the app name and the action/view Name
#         resolver_match = resolve(request.path_info)
#         app_name = resolver_match.app_name
#         url_name = resolver_match.url_name
#
#         # Automatically map URLs to permissions.
#         # Example: If a user clicks on the create/edit page URL, check the add/change permissions.
#         if url_name:
#             if 'create' in url_name or 'add' in url_name:
#                 perm_needed = f"{app_name}.add_{resolver_match.func.view_class.model._meta.model_name}"
#             elif 'edit' in url_name or 'update' in url_name:
#                 perm_needed = f"{app_name}.change_{resolver_match.func.view_class.model._meta.model_name}"
#             elif 'delete' in url_name:
#                 perm_needed = f"{app_name}.delete_{resolver_match.func.view_class.model._meta.model_name}"
#             else:
#                 perm_needed = None
#
#             # Check Group/User if not have permission, Return HTTP 405 Forbidden
#             if perm_needed and not request.user.has_perm(perm_needed):
#                 raise PermissionDenied("You don't have PERMISSION to access this page")
#
#         return self.get_response(request)


# Set RateLimit middleware at settings.py are enought
class GlobalRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        static_url = getattr(settings, 'STATIC_URL', '/static/')
        media_url = getattr(settings, 'MEDIA_URL', '/media/')

        if path.startswith(static_url) or (media_url and path.startswith(media_url)):
            return self.get_response(request)

        rate_settings = getattr(settings, 'RATE_LIMIT', '100/m')

        ratelimited = is_ratelimited(
            request,
            key="ip",
            rate=rate_settings,
            group="global",
            increment=True
        )

        if ratelimited:
            return HttpResponse(
                "Too many requests. Please try again later.",
                status=429
            )

        return self.get_response(request)


# Global Login Request Middleware
class GlobalLoginRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse('users:login'),
            # reverse('users:initial_superuser'),
        ]

        path = request.path

        static_url = getattr(settings, 'STATIC_URL', '/static/')
        media_url = getattr(settings, 'MEDIA_URL', '/media/')

        if (
            request.user.is_authenticated or
            path in exempt_urls or
            path.startswith('/backend-site-admin12321') or
            path.startswith(static_url) or
            (media_url and path.startswith(media_url))
        ):
            return self.get_response(request)

        messages.error(
            request,
            "You must be logged in to access this page."
        )
        return redirect('users:login')
