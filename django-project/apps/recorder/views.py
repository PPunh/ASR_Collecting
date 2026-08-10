# coding=utf-8
from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.common.mixins import SearchFilterMixin
from .models import VoiceRecordingModel

class RecordPageView(TemplateView):
	""" Recording Page """
	template_name = "recorder/record.html"



class RecordingListView(SearchFilterMixin, ListView):
	model = VoiceRecordingModel
	template_name = "recorder/home.html"
	context_object_name = "items"
	list_display = ["audio_file", "title", "created_at", "created_by"]
	paginate_by = 20
	ordering = ["-created_at"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "Sound List"
		context["topic"] = "Voice Recorded List"
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