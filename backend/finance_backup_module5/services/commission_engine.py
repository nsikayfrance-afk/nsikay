from decimal import Decimal


FEES = {
    "transfer": Decimal("0.005"),
    "mobile_money": Decimal("0.0085"),
    "withdraw": Decimal("0.012"),
    "wenze": Decimal("0"),
}


def generate_fee(amount, operation):

    amount = Decimal(amount)

    rate = FEES.get(
        operation,
        Decimal("0")
    )

    return amount * rate
