from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from finance.models import WalletTransaction


class WenzePaymentError(Exception):
    pass


@transaction.atomic
def pay_order_with_wallet(order, wallet):
    """
    Paiement WENZE par portefeuille NSIKAY.

    Sécurité :
    - Vérification commande
    - Vérification solde
    - Débit wallet atomique
    - Création transaction financière
    - Validation commande
    """

    if str(order.status).upper() == "PAID":
        raise WenzePaymentError("Commande déjà payée")

    amount = Decimal(order.total_amount)

    if wallet.balance < amount:
        raise WenzePaymentError("Solde insuffisant")

    wallet.balance -= amount
    wallet.save()

    transaction_wallet = WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="purchase",
        amount=amount,
        reference=order.reference,
        status="completed",
    )

    order.status = "PAID"
    order.payment_method = "wallet"
    order.payment_reference = str(transaction_wallet.id)
    order.payment_fee = Decimal("0.00")
    order.paid_at = timezone.now()
    order.save()

    return transaction_wallet
