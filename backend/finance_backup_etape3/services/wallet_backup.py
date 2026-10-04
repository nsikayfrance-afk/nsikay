from decimal import Decimal

from django.db import transaction

from finance.models import WalletTransaction


class WalletError(Exception):
    pass


@transaction.atomic
def deposit_wallet(wallet, amount, reference):
    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du dépôt doit être positif")

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
def withdraw_wallet(wallet, amount, reference):
    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du retrait doit être positif")

    if wallet.balance < amount:
        raise WalletError("Solde insuffisant")

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
def transfer_wallet(sender_wallet, receiver_wallet, amount, reference):
    amount = Decimal(amount)

    if amount <= 0:
        raise WalletError("Le montant du transfert doit être positif")

    if sender_wallet.balance < amount:
        raise WalletError("Solde insuffisant")

    if sender_wallet.currency != receiver_wallet.currency:
        raise WalletError("Les devises doivent être identiques")

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
        reference=reference,
        status="completed",
    )

    return sender_transaction
