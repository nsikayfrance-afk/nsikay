from django.apps import AppConfig


class ApiNsikayConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "api_nsikay"


    def ready(self):

        import api_nsikay.signals

