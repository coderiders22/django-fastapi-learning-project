from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    """
    App configuration for calculator module.
    Django uses this for app initialization.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculator'
