import inspect
from gift_resellers.services import create_reseller_sale, settle_reseller_sale

print("=" * 70)
print(" SIGNATURE create_reseller_sale")
print("=" * 70)

print(inspect.signature(create_reseller_sale))

print("\nPARAMETRES")
for name, param in inspect.signature(create_reseller_sale).parameters.items():
    print(
        f" - {name}"
        f" | kind={param.kind}"
        f" | default={param.default!r}"
    )

print("\n" + "=" * 70)
print(" SIGNATURE settle_reseller_sale")
print("=" * 70)

print(inspect.signature(settle_reseller_sale))

print("\nPARAMETRES")
for name, param in inspect.signature(settle_reseller_sale).parameters.items():
    print(
        f" - {name}"
        f" | kind={param.kind}"
        f" | default={param.default!r}"
    )

print("\nINSPECTION_SIGNATURE=OK")