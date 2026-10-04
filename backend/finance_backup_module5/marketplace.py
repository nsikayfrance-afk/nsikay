from decimal import Decimal


# WENZE est le module commercial officiel de NSIKAY.
# Aucune commission de vente WENZE n'est appliquée.
MARKETPLACE_COMMISSION = Decimal("0.00")


def calculate_marketplace_fee(amount):
    return Decimal("0.00")


def authorize_wallet_payment(wallet, amount):
    amount = Decimal(str(amount))

    if amount <= Decimal("0.00"):
        return False

    return wallet.balance >= amount
