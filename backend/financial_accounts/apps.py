
from django.apps import AppConfig


class FinancialAccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "financial_accounts"

    def ready(self):
        from . import gift_signals  # noqa: F401
