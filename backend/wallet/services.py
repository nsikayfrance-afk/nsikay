
from decimal import Decimal


TRANSFER_FEE = Decimal("0.25")
WITHDRAW_FEE = Decimal("1.20")


def calculate_transfer_fee(amount):

    return (
        amount * TRANSFER_FEE / Decimal("100")
    )



def calculate_withdraw_fee(amount):

    return (
        amount * WITHDRAW_FEE / Decimal("100")
    )



def execute_transfer(sender, receiver, amount):

    fee = calculate_transfer_fee(amount)

    return {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "commission": fee,
        "status": "SUCCESS"
    }



def execute_withdraw(wallet, amount):

    fee = calculate_withdraw_fee(amount)

    return {
        "wallet": wallet,
        "amount": amount,
        "fee": fee,
        "received": amount-fee,
        "status":"SUCCESS"
    }


