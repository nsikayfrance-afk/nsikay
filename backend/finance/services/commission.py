from decimal import Decimal


NSIKAY_FEES = {
    "transfer": Decimal("0.005"),
    "mobile_money": Decimal("0.0085"),
    "withdraw": Decimal("0.012"),
    "wenze": Decimal("0"),
}


def calculate_commission(amount, operation):
    amount = Decimal(amount)

    rate = NSIKAY_FEES.get(
        operation,
        Decimal("0")
    )

    return amount * rate
