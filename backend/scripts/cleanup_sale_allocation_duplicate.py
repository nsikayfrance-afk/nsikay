from django.db import transaction
from gift_resellers.models import SaleAllocation

SALE_ID = 9
ALLOCATION_TYPE = "MEMBER"
KEEP_ID = 20
DELETE_ID = 23

with transaction.atomic():
    rows = list(
        SaleAllocation.objects
        .select_for_update()
        .filter(
            sale_id=SALE_ID,
            allocation_type=ALLOCATION_TYPE,
        )
        .order_by("id")
    )

    print("AVANT_NETTOYAGE =", len(rows))

    for row in rows:
        print(
            f" - id={row.id} "
            f"| reference={row.reference} "
            f"| amount={row.amount}"
        )

    target = SaleAllocation.objects.filter(
        pk=DELETE_ID,
        sale_id=SALE_ID,
        allocation_type=ALLOCATION_TYPE,
    ).first()

    if target is None:
        raise RuntimeError(
            "Le doublon attendu id=23 n'existe plus. "
            "Nettoyage interrompu."
        )

    keeper = SaleAllocation.objects.filter(
        pk=KEEP_ID,
        sale_id=SALE_ID,
        allocation_type=ALLOCATION_TYPE,
    ).first()

    if keeper is None:
        raise RuntimeError(
            "L'allocation originale id=20 est introuvable. "
            "Nettoyage interrompu."
        )

    target.delete()

    print()
    print("SUPPRESSION_CIBLE = OK")
    print("SUPPRIME_ID =", DELETE_ID)
    print("CONSERVE_ID =", KEEP_ID)

remaining = list(
    SaleAllocation.objects
    .filter(
        sale_id=SALE_ID,
        allocation_type=ALLOCATION_TYPE,
    )
    .values("id", "reference", "amount")
)

print()
print("APRES_NETTOYAGE =", len(remaining))

for row in remaining:
    print(
        f" - id={row['id']} "
        f"| reference={row['reference']} "
        f"| amount={row['amount']}"
    )

if len(remaining) != 1 or remaining[0]["id"] != KEEP_ID:
    raise RuntimeError("VERIFICATION_NETTOYAGE_FAILED")

print("NETTOYAGE=OK")