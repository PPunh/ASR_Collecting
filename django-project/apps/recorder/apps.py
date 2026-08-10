from django.apps import AppConfig


# make sure to update AppClassName and App name
class RecorderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.recorder'
    verbose_name = 'Recorder Recording'
    label = 'recorder'
