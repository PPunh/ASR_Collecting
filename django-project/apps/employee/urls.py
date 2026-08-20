# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this employee app
app_name = 'employee'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.EmployeeListView.as_view(), name="list"),
    path('add/', views.EmployeeCreateView.as_view(), name="add"),
    path('details/<int:pk>/', views.EmployeeDetailView.as_view(), name="details"),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
