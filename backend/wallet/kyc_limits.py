from decimal import Decimal


def check_wallet_limit(
    profile,
    operation,
    amount
):

    amount = Decimal(amount)


    if operation == "deposit":

        return amount <= profile.daily_deposit_limit


    if operation == "withdraw":

        return amount <= profile.daily_withdraw_limit


    if operation == "transfer":

        return amount <= profile.daily_transfer_limit


    return False


