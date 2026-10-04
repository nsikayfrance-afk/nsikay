from decimal import Decimal


def calculate_bank_share(amount, percentage):

    amount = Decimal(amount)

    percentage = Decimal(percentage)

    return amount * percentage / Decimal("100")



def route_commission(
        amount,
        country,
        currency
):

    return {

        "country": country,

        "currency": currency,

        "amount": Decimal(amount)

    }
