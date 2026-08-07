# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'employies'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.EmployiesListView.as_view(), name="list"),
    path('add/', views.EmployiesCreateView.as_view(), name="add"),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
