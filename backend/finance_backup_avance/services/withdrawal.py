from decimal import Decimal
from django.db import transaction

from finance.models import WalletTransaction


class WithdrawalError(Exception):
    pass


@transaction.atomic
def final_withdraw(wallet, amount, reference):
    amount = Decimal(amount)

    if amount <= 0:
        raise WithdrawalError("Montant invalide")

    fee = amount * Decimal("0.012")

    total = amount + fee

    if wallet.balance < total:
        raise WithdrawalError("Solde insuffisant")

    wallet.balance -= total
    wallet.save(update_fields=["balance"])

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="withdraw",
        amount=amount,
        reference=reference,
        status="completed",
    )
