from decimal import Decimal
from django.db import transaction

from finance.models import WalletTransaction


class MobileMoneyError(Exception):
    pass


@transaction.atomic
def mobile_money_payment(wallet, amount, reference):
    amount = Decimal(amount)

    if amount <= 0:
        raise MobileMoneyError("Montant invalide")

    if wallet.balance < amount:
        raise MobileMoneyError("Solde insuffisant")

    fee = amount * Decimal("0.0085")

    total = amount + fee

    if wallet.balance < total:
        raise MobileMoneyError("Solde insuffisant avec frais")

    wallet.balance -= total
    wallet.save(update_fields=["balance"])

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="withdraw",
        amount=amount,
        reference=reference,
        status="completed",
    )
