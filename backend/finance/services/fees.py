from decimal import Decimal, ROUND_DOWN


NSIKAY_FEES = {
    "transfer": Decimal("0.005"),
    "mobile_money": Decimal("0.0085"),
    "withdraw": Decimal("0.012"),
    "wenze": Decimal("0.000"),
}


def calculate_fee(amount, operation):
    amount = Decimal(amount)

    rate = NSIKAY_FEES.get(
        operation,
        Decimal("0")
    )

    fee = (
        amount * rate
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_DOWN
    )

    return fee


def get_fee_rate(operation):
    return NSIKAY_FEES.get(
        operation,
        Decimal("0")
    )
