# coding=utf-8
import os
import re
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View, TemplateView, DetailView
from django.http import JsonResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.db.models import Count
from apps.common.mixins import SearchFilterMixin, SuperAdminRequiredMixin
from .models import VoiceRecordingModel, VoiceCategoryModel
from .forms import VoiceCategoryForm

class VoiceCategoryListView(LoginRequiredMixin, SearchFilterMixin, ListView):
    model = VoiceCategoryModel
    template_name = "recorder/voice_category.html"
    context_object_name = "items"
    paginate_by = 20
    search_fields = [
        "name"
    ]

    def get_queryset(self):
        return super().get_queryset().annotate(total_items=Count('category'))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Category"
        context['topic'] = "All Categories"
        return context


class VoiceCategoryCreateView(SuperAdminRequiredMixin, CreateView):
    model = VoiceCategoryModel
    template_name = "recorder/create_category.html"
    form_class = VoiceCategoryForm
    success_url = reverse_lazy("recorder:category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Category"
        context["topic"] = "New Category"
        return context


class RecordingListView(LoginRequiredMixin, SearchFilterMixin, ListView):
    model = VoiceRecordingModel
    template_name = "recorder/voices_list.html"
    context_object_name = "items"
    list_display = ["audio_file", "title", "created_by", "status", "reviewed_by"]
    search_fields = ["title", "created_by__username", "reviewed_by__username"]
    status_field = "status"
    status_choices = VoiceRecordingModel.StatusChoices.choices
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        category_pk = self.kwargs.get('pk')
        if category_pk:
            self.category = get_object_or_404(VoiceCategoryModel, pk=category_pk)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        if self.category:
            context["title"] = f"Category: {self.category.name}"
            context["topic"] = f"{self.category.name}"
        else:
            context["title"] = "All Recordings"
            context["topic"] = "Voices Recorded List"
        context["details_url_name"] = "recorder:details"
        context["download_url_name"] = "recorder:download_audio"
        return context



class RecordPageView(LoginRequiredMixin, CreateView):
    """ Recording Page """
    model = VoiceRecordingModel
    template_name = "recorder/record_page.html"
    fields = ['title', 'audio_file']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # category_id = self.kwargs.get('category_id') or request.GET.get('category')
        # self.category = get_object_or_404(VoiceCategoryModel, pk=category_id) if category_id else None
        category_id = self.kwargs.get('pk') or self.kwargs.get('category_id') or request.GET.get('category')
        self.category = get_object_or_404(VoiceCategoryModel, pk=category_id) if category_id else None

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if self.category:
            form.instance.category = self.category
        return super().form_valid(form)

    def get_success_url(self):
        if self.category:
            return reverse('recorder:recording_list', kwargs={'pk': self.category.pk})
        return reverse('recorder:category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["title"] = f"Recording voice for {self.category.name}" if self.category else "Recording your voice"
        return context


class UploadAudioView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        audio = request.FILES.get('audio')
        if not audio:
            return JsonResponse({'status': 'error', 'message': 'No audio file provided'}, status=400)

        title = request.POST.get('title', '').strip() or 'Untitled Recording'
        script=request.POST.get('script', '')

        # 1. Get category From FormData has send via JavaScript
        category_id = request.POST.get('category')

        # 2. find Instance
        category_obj = None
        if category_id and category_id.isdigit():
            category_obj = VoiceCategoryModel.objects.filter(pk=int(category_id)).first()

        if not category_obj:
            return JsonResponse({'status': 'error', 'message': 'Category is required'}, status=400)

        rec = VoiceRecordingModel.objects.create(
            audio_file=audio,
            title=title,
            script = script,
            category=category_obj,
            created_by=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({
            'status': 'ok',
            'id': rec.id,
            'url': rec.audio_file.url,
        })

class ReviewVoiceDetailView(LoginRequiredMixin, DetailView):
    model = VoiceRecordingModel
    template_name = "recorder/review.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail"
        context["topic"] = "Detail of Voice Recorded"
        context["pending_status"] = self.object.status == "pending"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticator():
            return self.handle_no_permission()

        action = request.POST.get('action')
        comment = request.POST.get('comment', '').strip()

        # Check action from form
        if action in ['approved', 'rejected']:
            self.object.status = action
            self.object.comment = comment
            self.object.reviewed_by = request.user
            self.object.reviewed_at = timezone.now()
            self.object.save()

            if self.object.category:
                return redirect('recorder:recording_list', pk=self.object.category.pk)
            return redirect('recorder:category')

        return redirect('recorder:details', pk=self.object.pk)


class DownloadAudioView(LoginRequiredMixin, View):
    """ Stream the recording as an attachment named after its title """

    def get(self, request, *args, **kwargs):
        rec = get_object_or_404(VoiceRecordingModel, pk=kwargs.get('pk'))

        if rec.status != VoiceRecordingModel.StatusChoices.APPROVED:
            return JsonResponse({'status': 'error', 'message': 'Not available until approved'}, status=403)

        if not rec.audio_file:
            return JsonResponse({'status': 'error', 'message': 'No audio file attached'}, status=404)

        # Keep the real extension of the stored file (webm / mpeg / wav ...)
        _, ext = os.path.splitext(rec.audio_file.name)
        if not ext:
            ext = ".webm"

        # Build a safe filename from the title
        title = rec.title.strip() or f"recording-{rec.pk}"
        safe_title = re.sub(r'[\\/:*?"<>|]+', '_', title)
        safe_title = re.sub(r'\s+', ' ', safe_title).strip(' ._')
        safe_title = safe_title[:50]

        response = FileResponse(
            rec.audio_file.open('rb'),
            as_attachment=True,
            filename=f"{safe_title}{ext}",
        )
        return response
