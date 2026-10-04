from decimal import Decimal

from financial_routing.services import calculate_fee


def _fee(amount, fee_type):
    result = calculate_fee(Decimal(str(amount)), fee_type)

    if isinstance(result, dict):
        return Decimal(str(result["fee_amount"]))

    if isinstance(result, (tuple, list)):
        if len(result) >= 5:
            return Decimal(str(result[3]))
        if len(result) == 2:
            return Decimal(str(result[0]))

    raise RuntimeError(
        f"Format inattendu retourné par calculate_fee(): {type(result)}"
    )


def calculate_transfer_fee(amount):
    return _fee(amount, "TRANSFER_INTERNAL")


def calculate_withdrawal_fee(amount):
    return _fee(amount, "WITHDRAWAL")


def calculate_mobile_money_fee(amount):
    return _fee(amount, "TRANSFER_MOBILE_MONEY")


def calculate_visa_fee(amount):
    return _fee(amount, "TRANSFER_VISA")


def calculate_wenze_fee(amount):
    return _fee(amount, "WENZE")
