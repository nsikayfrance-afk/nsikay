from decimal import Decimal
from django.db import transaction

from finance.models import BankRoutingOperation


@transaction.atomic
def route_bank_operation(
    bank_account,
    amount,
    operation_type,
    country,
    currency,
    reference
):

    amount = Decimal(amount)

    bank_account.balance += amount

    bank_account.save(
        update_fields=["balance"]
    )


    return BankRoutingOperation.objects.create(

        bank_account=bank_account,

        operation_type=operation_type,

        amount=amount,

        country=country,

        currency=currency,

        reference=reference

    )
