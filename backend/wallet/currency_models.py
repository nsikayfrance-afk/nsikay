from django.db import models
from wallet.models import Wallet


class WalletCurrencyBalance(models.Model):

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="currency_balances"
    )

    currency = models.CharField(
        max_length=10
    )


    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        unique_together = (
            "wallet",
            "currency"
        )


    def __str__(self):
        return f"{self.wallet} - {self.currency}"

