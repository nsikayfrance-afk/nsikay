import os
from decimal import Decimal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

print("=" * 70)
print(" NSIKAY - STAGE 4D.4 - MOBILE MONEY / CARTE")
print("=" * 70)

payment = Decimal("100.00")

rate = Decimal("0.85") / Decimal("100")

fee = payment * rate
received = payment - fee

print("\nCALCUL MOBILE MONEY / CARTE")
print(" - Paiement =", payment)
print(" - Frais NSIKAY =", fee)
print(" - Montant final =", received)

assert fee == Decimal("0.85")
assert received == Decimal("99.15")

print("\nCONTROLE MOBILE MONEY 0.85% = OK")

print("=" * 70)
