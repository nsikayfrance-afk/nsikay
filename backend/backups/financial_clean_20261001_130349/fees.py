from decimal import Decimal


TRANSFER_COMMISSION = Decimal("0.0025")

WITHDRAW_FEE = Decimal("0.005")



def calculate_platform_commission(amount):

    return Decimal(amount) * TRANSFER_COMMISSION



def calculate_withdraw_cost(amount):

    return Decimal(amount) * WITHDRAW_FEE


