from decimal import Decimal
from django.db import transaction

from finance.models import WalletTransaction


class WenzePaymentError(Exception):
    pass


@transaction.atomic
def pay_wenze(
    buyer_wallet,
    seller_wallet,
    amount,
    reference=None
):
    amount = Decimal(amount)

    if amount <= 0:
        raise WenzePaymentError(
            "Le montant doit être positif"
        )

    if buyer_wallet.balance < amount:
        raise WenzePaymentError(
            "Solde Libenga insuffisant"
        )

    if buyer_wallet.currency != seller_wallet.currency:
        raise WenzePaymentError(
            "Les devises doivent être identiques"
        )


    buyer_wallet.balance -= amount
    buyer_wallet.save(
        update_fields=["balance"]
    )


    seller_wallet.balance += amount
    seller_wallet.save(
        update_fields=["balance"]
    )


    if reference is None:
        reference = (
            "WENZE-PAY-"
            + str(amount).replace(".", "")
        )


    transaction = WalletTransaction.objects.create(
        wallet=buyer_wallet,
        transaction_type="purchase",
        amount=amount,
        reference=reference,
        status="completed",
    )


    WalletTransaction.objects.create(
        wallet=seller_wallet,
        transaction_type="deposit",
        amount=amount,
        reference=reference+"-SELLER",
        status="completed",
    )


    return transaction
