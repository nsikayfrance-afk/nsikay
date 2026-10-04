from django.db.models import Count
from gift_resellers.models import SaleAllocation

duplicates = list(
    SaleAllocation.objects
    .values("sale_id", "allocation_type")
    .annotate(total=Count("id"))
    .filter(total__gt=1)
)

print("TOTAL_ALLOCATIONS =", SaleAllocation.objects.count())
print("GROUPES_DOUBLONS =", len(duplicates))

if duplicates:
    for row in duplicates:
        print(row)
    raise RuntimeError("DOUBLONS_RESTANTS")

print("AUCUN_DOUBLON=OK")