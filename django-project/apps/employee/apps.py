from django.apps import AppConfig


# make sure to update AppClassName and App name
class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.employee'
    verbose_name = 'Employee'
    label = 'employee'
