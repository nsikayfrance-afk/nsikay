import os
from decimal import Decimal

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

print("=" * 70)
print(" NSIKAY - STAGE 4D.3 - TEST RETRAIT")
print("=" * 70)

withdrawal = Decimal("100.00")

rate = Decimal("1.20") / Decimal("100")

fee = withdrawal * rate
received = withdrawal - fee

print("\nCALCUL RETRAIT")
print(" - Demande retrait =", withdrawal)
print(" - Frais NSIKAY =", fee)
print(" - Montant utilisateur =", received)

assert fee == Decimal("1.20")
assert received == Decimal("98.80")

print("\nCONTROLE RETRAIT 1.20% = OK")

print("=" * 70)
