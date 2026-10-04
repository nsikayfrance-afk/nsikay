from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from api_nsikay.models import VirtualGift
from gift_resellers.models import (
    DistributionAgreement,
    GiftInventoryUnit,
    NetworkMember,
    Reseller,
    ResellerNetwork,
)
from gift_resellers.services import calculate_reseller_sale_split


User = get_user_model()

print("")
print("============================================================")
print(" TEST RESEAU REVENDEURS CADEAUX")
print("============================================================")

gift = VirtualGift.objects.order_by("value_eur").first()

if gift is None:
    raise RuntimeError("Aucun cadeau du catalogue.")

print(f"CADEAU TEST : {gift.name}")
print(f"VALEUR OFFICIELLE : {gift.value_eur} EUR")

split = calculate_reseller_sale_split(
    retail_amount=Decimal("600.00"),
    retail_currency="EUR",
    official_value_eur=Decimal("500.00"),
    member_percentage=Decimal("60.000"),
    principal_reseller_percentage=Decimal("30.000"),
    other_percentage=Decimal("0.000"),
)

print("")
print("TEST EXEMPLE :")
print("Prix retail : 600 EUR")
print("Valeur officielle : 500 EUR")
print("Membre : 60 % du retail =", split["member_amount"])
print("Revendeur principal : 30 % du retail =", split["principal_reseller_amount"])
print("NSIKAY : 5 % de 500 EUR =", split["nsikay_amount_eur"])
print("Non alloue =", split["unallocated_amount"])

assert split["nsikay_amount_eur"] == Decimal("25.00")
assert split["member_amount"] == Decimal("360.00")
assert split["principal_reseller_amount"] == Decimal("180.00")

print("")
print("RESULTAT REGLE 5 % : OK")
print("RESULTAT CALCUL : OK")
print("")
print("Le prix retail n'a pas modifie la base NSIKAY.")
print("La base NSIKAY reste la valeur officielle initiale EUR.")
print("")