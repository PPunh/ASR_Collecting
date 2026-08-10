# coding=utf-8
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, View, TemplateView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from apps.common.mixins import SearchFilterMixin
from .models import VoiceRecordingModel

class RecordPageView(CreateView):
    """ Recording Page """
    model = VoiceRecordingModel
    template_name = "recorder/record.html"
    fields = ['title', 'audio_file']
    success_url = reverse_lazy('recorder:recording_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	context["title"] = "Recording your voice"
    	return context



class RecordingListView(SearchFilterMixin, ListView):
	model = VoiceRecordingModel
	template_name = "recorder/home.html"
	context_object_name = "items"
	list_display = ["audio_file", "title", "created_by", "status", "reviewed_by"]
	search_fields = ["title"]
	paginate_by = 20
	ordering = ["-created_at"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Sound List"
		context["topic"] = "Voice Recorded List"
		context["details_url_name"] = "recorder:details"
		return context


class UploadAuditoView(View):
	""" Get audio from JS and save into DB """
	def post(self, request, *args, **kwargs):
		audio = request.FILES.get('audio')
		if not audio:
			return JsonResponse(
				{
					'status':'error',
					'messages': "Not found",
				}, status = 400
			)

		title = request.POST.get('title', '')
		rec = VoiceRecordingModel.objects.create(audio_file = audio, title=title)

		return JsonResponse({
			'status':'ok',
			'id':rec.id,
			'url':rec.audio_file.url,
		})


class ReviewVoiceDetailView(DetailView):
	model = VoiceRecordingModel
	template_name = "recorder/detail.html"
	context_object_name = "object"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Detail"
		context["topic"] = "Detail of Voice Recorded"
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

		action = request.POST.get('action')
		comment = request.POST.get('comment', '').strip()

		# Check action from form
		if action in ['approved', 'rejected']:
			self.object.status = action
			self.object.comment = comment
			self.object.reviewed_by = request.user
			self.object.reviewed_at = timezone.now()
			self.object.save()
		return redirect('recorder:details', pk=self.object.pk)