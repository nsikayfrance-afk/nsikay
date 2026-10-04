from decimal import Decimal
from django.db import transaction

from banking.models import (
    BankTransaction,
    BankBalance
)



def create_transaction(
    account,
    transaction_type,
    amount,
    currency,
    reference
):

    operation = BankTransaction.objects.create(

        account=account,

        transaction_type=transaction_type,

        amount=Decimal(amount),

        currency=currency,

        reference=reference,

        status="completed"

    )


    update_balance(
        account,
        currency,
        transaction_type,
        Decimal(amount)
    )


    return operation




def update_balance(
    account,
    currency,
    transaction_type,
    amount
):

    balance, created = BankBalance.objects.get_or_create(

        account=account,

        currency=currency

    )


    if transaction_type == "deposit":

        balance.balance += amount


    elif transaction_type == "withdrawal":

        balance.balance -= amount


    balance.save()



def transfer_money(
    sender,
    receiver,
    amount,
    currency,
    reference
):

    with transaction.atomic():

        sender_balance = BankBalance.objects.get(

            account=sender,

            currency=currency

        )


        if sender_balance.balance < Decimal(amount):

            raise Exception(
                "Solde insuffisant"
            )


        create_transaction(

            sender,

            "transfer",

            amount,

            currency,

            reference + "-OUT"

        )


        create_transaction(

            receiver,

            "deposit",

            amount,

            currency,

            reference + "-IN"

        )


    return True

from banking.models import (
    AccountOpeningRequest,
    BankAccount
)


def activate_bank_account(request_id):

    opening = AccountOpeningRequest.objects.get(
        id=request_id
    )


    if opening.status != "approved":
        return None


    account = BankAccount.objects.create(

        user=opening.user,

        bank=opening.bank,

        currency=opening.currency,

        account_number=(
            "NSK"
            + str(opening.id).zfill(10)
        ),

    )


    opening.status = "activated"

    opening.save()


    return account


