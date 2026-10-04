import gift_resellers.services as services

required = [
    "create_gift_inventory_unit",
    "distribute_gift_unit",
    "create_distribution_agreement",
    "accept_distribution_agreement",
    "lock_distribution_agreement",
]

all_ok = True

for name in required:
    value = hasattr(services, name)
    print(f"{name} = {value}")
    if not value:
        all_ok = False

if not all_ok:
    raise RuntimeError(
        "Au moins un service Stage 2 est absent."
    )

print("")
print("SERVICES_STAGE2 = OK")