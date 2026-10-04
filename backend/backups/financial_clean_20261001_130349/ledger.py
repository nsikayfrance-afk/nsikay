from decimal import Decimal



WITHDRAW_FEE_RATE = Decimal("0.005")

TRANSFER_FEE_RATE = Decimal("0.0025")




def calculate_withdraw_fee(amount):

    return (
        Decimal(amount)
        *
        WITHDRAW_FEE_RATE
    )




def calculate_transfer_fee(amount):

    return (
        Decimal(amount)
        *
        TRANSFER_FEE_RATE
    )




def create_ledger_entry(
        wallet,
        operation,
        amount,
        currency,
        reference
):

    from finance.models import FinancialLedger


    return FinancialLedger.objects.create(

        wallet=wallet,

        transaction_type=operation,

        amount=amount,

        currency=currency,

        reference=reference

    )


