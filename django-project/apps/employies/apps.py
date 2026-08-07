from django.apps import AppConfig


# make sure to update AppClassName and App name
class EmployiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.employies'
    verbose_name = 'Employies'
    label = 'employies'
