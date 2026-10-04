from django.db import connection
from gift_resellers.models import SaleAllocation

table = SaleAllocation._meta.db_table

with connection.cursor() as cursor:
    constraints = connection.introspection.get_constraints(
        cursor,
        table,
    )

name = "uniq_sale_allocation_type"

print("TABLE =", table)
print("TOTAL_ALLOCATIONS =", SaleAllocation.objects.count())

if name not in constraints:
    raise RuntimeError("CONTRAINTE_DB_ABSENTE")

constraint = constraints[name]

print("CONTRAINTE =", name)
print("UNIQUE =", constraint["unique"])
print("COLUMNS =", constraint["columns"])

if not constraint["unique"]:
    raise RuntimeError("CONTRAINTE_NON_UNIQUE")

expected = ["sale_id", "allocation_type"]

if constraint["columns"] != expected:
    raise RuntimeError(
        f"COLONNES_INCORRECTES: {constraint['columns']}"
    )

print("PROTECTION_DB_DOUBLE_ALLOCATION=OK")