from django.urls import path, include

# auth_views
from django.contrib.auth import views as auth_views

# 3rd party libs
from rest_framework.routers import DefaultRouter

# from . import views
from . import views


app_name = 'users' # Namespace for URLs in this users app
router = DefaultRouter()
# router.register('', views.ViewSet, name='')

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
]

# when user go to path /app_name/ it will show api root page (API endpoints list)
urlpatterns += router.urls
