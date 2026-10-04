from decimal import Decimal
import uuid

from django.db import transaction

from finance.models import WalletTransaction


class WalletError(Exception):
    pass


def generate_reference(prefix="NSIKAY"):
    return (
        prefix
        + "-"
        + uuid.uuid4().hex[:12].upper()
    )


@transaction.atomic
def deposit_wallet(wallet, amount, reference=None):
    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du dépôt doit être positif")

    if not reference:
        reference = generate_reference("DEPOSIT")

    wallet.balance += amount
    wallet.save(update_fields=["balance"])

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="deposit",
        amount=amount,
        reference=reference,
        status="completed",
    )


@transaction.atomic
def withdraw_wallet(wallet, amount, reference=None):
    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du retrait doit être positif")

    if wallet.balance < amount:
        raise WalletError("Solde insuffisant")

    if not reference:
        reference = generate_reference("WITHDRAW")

    wallet.balance -= amount
    wallet.save(update_fields=["balance"])

    return WalletTransaction.objects.create(
        wallet=wallet,
        transaction_type="withdraw",
        amount=amount,
        reference=reference,
        status="completed",
    )


@transaction.atomic
def transfer_wallet(sender_wallet, receiver_wallet, amount, reference=None):

    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du transfert doit être positif")

    if sender_wallet.balance < amount:
        raise WalletError("Solde insuffisant")

    if sender_wallet.currency != receiver_wallet.currency:
        raise WalletError("Les devises doivent être identiques")

    if not reference:
        reference = generate_reference("TRANSFER")

    sender_wallet.balance -= amount
    sender_wallet.save(update_fields=["balance"])

    receiver_wallet.balance += amount
    receiver_wallet.save(update_fields=["balance"])

    sender_transaction = WalletTransaction.objects.create(
        wallet=sender_wallet,
        transaction_type="transfer",
        amount=amount,
        reference=reference,
        status="completed",
    )

    WalletTransaction.objects.create(
        wallet=receiver_wallet,
        transaction_type="deposit",
        amount=amount,
        reference=reference + "-RECEIVER",
        status="completed",
    )

    return sender_transaction
