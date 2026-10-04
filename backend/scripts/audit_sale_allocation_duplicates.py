from django.db.models import Count
from gift_resellers.models import SaleAllocation

duplicates = list(
    SaleAllocation.objects
    .values("sale_id", "allocation_type")
    .annotate(total=Count("id"))
    .filter(total__gt=1)
    .order_by("sale_id", "allocation_type")
)

print()
print("TOTAL_ALLOCATIONS =", SaleAllocation.objects.count())
print("GROUPES_DOUBLONS =", len(duplicates))
print()

if duplicates:
    print("DOUBLONS_DETECTES :")
    for row in duplicates:
        print(
            f" - sale_id={row['sale_id']} "
            f"| allocation_type={row['allocation_type']} "
            f"| total={row['total']}"
        )

        items = list(
            SaleAllocation.objects
            .filter(
                sale_id=row["sale_id"],
                allocation_type=row["allocation_type"],
            )
            .order_by("id")
            .values(
                "id",
                "reference",
                "amount",
                "percentage",
                "created_at",
            )
        )

        for item in items:
            print(
                f"      id={item['id']} "
                f"| ref={item['reference']} "
                f"| amount={item['amount']} "
                f"| pct={item['percentage']} "
                f"| created={item['created_at']}"
            )
else:
    print("AUCUN_DOUBLON_DETECTE")

print()
print("AUDIT=TERMINE")