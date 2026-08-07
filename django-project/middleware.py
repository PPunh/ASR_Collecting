from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django_ratelimit.core import is_ratelimited
from django.conf import settings

# Global Rate Limit Milddleware
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