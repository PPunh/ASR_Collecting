# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'recorder'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.RecordingListView.as_view(), name='recording_list'),
    path('record/', views.RecordPageView.as_view(), name='record_page'),
    path('upload-audio/', views.UploadAuditoView.as_view(), name='upload_audio'),
    path('details/<int:pk>/', views.ReviewVoiceDetailView.as_view(), name="details"),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
