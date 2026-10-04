from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from wallet.models import Wallet
from wallet.currency_models import WalletCurrencyBalance


User = get_user_model()



@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):

    if created:

        wallet, created_wallet = Wallet.objects.get_or_create(
            user=instance
        )


        currencies = [
            "USD",
            "EUR",
            "CDF"
        ]


        for currency in currencies:

            WalletCurrencyBalance.objects.get_or_create(
                wallet=wallet,
                currency=currency,
                defaults={
                    "balance":0
                }
            )

