# apps/recorder/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'recorder'

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),

    # 1. Category List
    path('', views.VoiceCategoryListView.as_view(), name="category"),

    # 2. Create Category
    path('add_category/', views.VoiceCategoryCreateView.as_view(), name="add_category"),

    path('recording_list/<int:pk>/', views.RecordingListView.as_view(), name='recording_list'),

    path('category/<int:pk>/record/', views.RecordPageView.as_view(), name='record_voice'),

    path('upload-audio/', views.UploadAudioView.as_view(), name='upload_audio'),

    path('details/<int:pk>/', views.ReviewVoiceDetailView.as_view(), name="details"),

    path('download/<int:pk>/', views.DownloadAudioView.as_view(), name="download_audio"),
]
