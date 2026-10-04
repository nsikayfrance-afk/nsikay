from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from api_nsikay.models import VirtualGift

from gift_resellers.models import (
    Reseller,
    NetworkMember,
    SaleAllocation,
    GiftResellerAuditLog,
)

from gift_resellers.services import (
    create_gift_inventory_unit,
    distribute_gift_unit,
    create_distribution_agreement,
    accept_distribution_agreement,
    lock_distribution_agreement,
    calculate_reseller_sale_split,
    create_reseller_sale,
    settle_reseller_sale,
)

print("")
print("=" * 70)
print(" NSIKAY - TEST FONCTIONNEL GIFT RESELLERS STAGE 3 V2")
print("=" * 70)
print("")

User = get_user_model()

reseller_user = User.objects.get(
    username="banque_test_nsikay"
)

member_user = User.objects.get(
    username="validation_test_nsikay"
)

customer = User.objects.get(
    username="admin_test_nsikay"
)

reseller = Reseller.objects.get(
    user=reseller_user
)

membership = (
    NetworkMember.objects
    .filter(
        user=member_user,
        network__principal_reseller=reseller,
        active=True,
    )
    .order_by("-id")
    .first()
)

if membership is None:
    raise AssertionError(
        "Aucun membre actif trouve pour le revendeur."
    )

gift = VirtualGift.objects.get(
    slug="quartz"
)

print("REVENDEUR :", reseller_user.username)
print("MEMBRE    :", member_user.username)
print("CLIENT    :", customer.username)
print("")
print("CADEAU :", gift.name)
print("VALEUR OFFICIELLE :", gift.reference_value_eur, "EUR")

# ============================================================
# UNITE
# ============================================================

unit = create_gift_inventory_unit(
    gift=gift,
    source="RESELLER",
    reseller=reseller,
    actor=reseller_user,
)

print("")
print("UNITÉ :", unit.unit_id)
print("STATUT :", unit.status)

if unit.status != "AVAILABLE":
    raise AssertionError(
        "Unite non AVAILABLE."
    )

print("CREATION_UNITE = OK")

# ============================================================
# DISTRIBUTION
# ============================================================

unit = distribute_gift_unit(
    unit=unit,
    reseller=reseller,
    member=membership,
    actor=reseller_user,
)

if unit.status != "DISTRIBUTED":
    raise AssertionError(
        "Unite non DISTRIBUTED."
    )

print("DISTRIBUTION = OK")

# ============================================================
# ACCORD
# ============================================================

agreement = create_distribution_agreement(
    principal_reseller=reseller,
    network_member=membership,
    gift=gift,
    quantity=1,
    member_percentage=Decimal("60.000"),
    principal_reseller_percentage=Decimal("30.000"),
    other_percentage=Decimal("5.000"),
    actor=reseller_user,
)

agreement = accept_distribution_agreement(
    agreement=agreement,
    actor=reseller_user,
)

agreement = lock_distribution_agreement(
    agreement=agreement,
    actor=reseller_user,
)

if agreement.status != "LOCKED":
    raise AssertionError(
        "Accord non LOCKED."
    )

print("ACCORD_LOCKED = OK")

# ============================================================
# CALCUL
# ============================================================

split = calculate_reseller_sale_split(
    retail_amount=Decimal("600.00"),
    retail_currency="EUR",
    official_value_eur=agreement.official_value_eur,
    member_percentage=agreement.member_percentage,
    principal_reseller_percentage=agreement.principal_reseller_percentage,
    other_percentage=agreement.other_percentage,
    nsikay_percentage=agreement.nsikay_percentage,
)

print("")
print("PRIX RETAIL :", split["retail_amount"], "EUR")
print("BASE NSIKAY :", split["nsikay_base_eur"], "EUR")
print("NSIKAY      :", split["nsikay_amount_eur"], "EUR")
print("MEMBRE      :", split["member_amount"], "EUR")
print("REVENDEUR   :", split["principal_reseller_amount"], "EUR")
print("AUTRE       :", split["other_amount"], "EUR")
print("NON AFFECTE :", split["unallocated_amount"], "EUR")

expected_nsikay = (
    agreement.official_value_eur * Decimal("0.05")
).quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)

if split["nsikay_amount_eur"] != expected_nsikay:
    raise AssertionError(
        "Commission NSIKAY incorrecte."
    )

print("CALCUL_5_POURCENT = OK")

# ============================================================
# CREATION VENTE
# ============================================================

sale = create_reseller_sale(
    unit=unit,
    agreement=agreement,
    customer=customer,
    retail_amount=Decimal("600.00"),
    retail_currency="EUR",
    actor=member_user,
)

print("")
print("VENTE :", sale.reference)
print("STATUT :", sale.status)

if sale.status != "PENDING":
    raise AssertionError(
        "La vente doit etre PENDING."
    )

print("CREATION_VENTE = OK")

# ============================================================
# REGLEMENT
# ============================================================

sale = settle_reseller_sale(
    sale=sale,
    payment_reference="TEST-PAYMENT-STAGE3-V2-001",
    actor=member_user,
)

sale.refresh_from_db()
unit.refresh_from_db()

print("")
print("STATUT VENTE :", sale.status)
print("STATUT UNITE :", unit.status)

if sale.status != "SETTLED":
    raise AssertionError(
        "Vente non SETTLED."
    )

if unit.status != "SOLD":
    raise AssertionError(
        "Unite non SOLD."
    )

print("REGLEMENT = OK")

# ============================================================
# ALLOCATIONS
# ============================================================

allocations = list(
    SaleAllocation.objects
    .filter(sale=sale)
    .order_by("id")
)

print("")
print("ALLOCATIONS :", len(allocations))

for row in allocations:
    print(
        row.allocation_type,
        "|",
        row.amount,
        row.currency,
        "| BASE",
        row.base_amount,
    )

types = {
    row.allocation_type
    for row in allocations
}

for required in (
    "MEMBER",
    "PRINCIPAL_RESELLER",
    "NSIKAY",
    "OTHER",
):
    if required not in types:
        raise AssertionError(
            f"Allocation absente : {required}"
        )

print("ALLOCATIONS_AUTOMATIQUES = OK")

# ============================================================
# MONTANTS
# ============================================================

member = next(
    row for row in allocations
    if row.allocation_type == "MEMBER"
)

principal = next(
    row for row in allocations
    if row.allocation_type == "PRINCIPAL_RESELLER"
)

nsikay = next(
    row for row in allocations
    if row.allocation_type == "NSIKAY"
)

other = next(
    row for row in allocations
    if row.allocation_type == "OTHER"
)

if member.amount != Decimal("360.00"):
    raise AssertionError(
        "Part membre incorrecte."
    )

if principal.amount != Decimal("180.00"):
    raise AssertionError(
        "Part revendeur incorrecte."
    )

if nsikay.amount != Decimal("0.01"):
    raise AssertionError(
        "Part NSIKAY incorrecte."
    )

if other.amount != Decimal("30.00"):
    raise AssertionError(
        "Part OTHER incorrecte."
    )

print("MONTANTS = OK")

# ============================================================
# DOUBLE REGLEMENT
# ============================================================

try:
    settle_reseller_sale(
        sale=sale,
        payment_reference="DOUBLE-TEST",
        actor=member_user,
    )
except ValidationError:
    print("ANTI_DOUBLE_REGLEMENT = OK")
else:
    raise AssertionError(
        "Double reglement accepte."
    )

# ============================================================
# DOUBLE VENTE
# ============================================================

try:
    create_reseller_sale(
        unit=unit,
        agreement=agreement,
        customer=customer,
        retail_amount=Decimal("600.00"),
        retail_currency="EUR",
        actor=member_user,
    )
except ValidationError:
    print("ANTI_DOUBLE_VENTE = OK")
else:
    raise AssertionError(
        "Deuxieme vente acceptee."
    )

# ============================================================
# TRACE
# ============================================================

audit_unit = GiftResellerAuditLog.objects.filter(
    reference=unit.unit_id
).count()

audit_sale = GiftResellerAuditLog.objects.filter(
    reference=sale.reference
).count()

allocation_count = SaleAllocation.objects.filter(
    sale=sale
).count()

print("")
print("AUDIT UNITE :", audit_unit)
print("AUDIT VENTE :", audit_sale)
print("ALLOCATIONS :", allocation_count)

if audit_unit < 2:
    raise AssertionError(
        "Audit unite insuffisant."
    )

if audit_sale < 2:
    raise AssertionError(
        "Audit vente insuffisant."
    )

if allocation_count < 4:
    raise AssertionError(
        "Allocations insuffisantes."
    )

print("TRAÇABILITE = OK")

print("")
print("=" * 70)
print(" TEST_STAGE3_COMPLET = OK")
print("=" * 70)