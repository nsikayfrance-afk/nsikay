from decimal import Decimal

print("=" * 70)
print("DIAGNOSTIC DECIMAL COMMISSION NSIKAY")
print("=" * 70)

from gift_resellers.services import calculate_reseller_sale_split

split = calculate_reseller_sale_split(
    retail_amount=Decimal("600.00"),
    official_value_eur=Decimal("0.10"),
    member_percentage=Decimal("60.00"),
    principal_reseller_percentage=Decimal("30.00"),
    nsikay_percentage=Decimal("5.000"),
    other_percentage=Decimal("5.00"),
    currency="EUR",
)

expected = (
    Decimal("0.10") * Decimal("0.05")
).quantize(Decimal("0.01"))

actual = split["nsikay_amount_eur"]

print("official_value_eur :", repr(Decimal("0.10")))
print("5 % brut          :", repr(Decimal("0.10") * Decimal("0.05")))
print("expected          :", repr(expected))
print("actual            :", repr(actual))
print("type expected     :", type(expected))
print("type actual       :", type(actual))
print("expected == actual:", expected == actual)
print("expected str      :", str(expected))
print("actual str        :", str(actual))
print("expected tuple    :", expected.as_tuple())
print("actual tuple      :", actual.as_tuple())

print("")
print("SPLIT COMPLET :")
for key, value in split.items():
    print(f"{key}: {value!r} | type={type(value)}")

if actual != expected:
    raise AssertionError(
        f"DIAGNOSTIC ECHEC : expected={expected!r}, actual={actual!r}"
    )

print("")
print("DIAGNOSTIC_COMMISSION = OK")