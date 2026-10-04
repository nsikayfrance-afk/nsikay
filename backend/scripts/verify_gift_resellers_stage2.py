from gift_resellers.models import (
    GiftInventoryUnit,
    DistributionAgreement,
    Reseller,
    ResellerNetwork,
    NetworkMember,
    ResellerSale,
    SaleAllocation,
)

print("GiftInventoryUnit =", GiftInventoryUnit.objects.count())
print("DistributionAgreement =", DistributionAgreement.objects.count())
print("Reseller =", Reseller.objects.count())
print("ResellerNetwork =", ResellerNetwork.objects.count())
print("NetworkMember =", NetworkMember.objects.count())
print("ResellerSale =", ResellerSale.objects.count())
print("SaleAllocation =", SaleAllocation.objects.count())

print("")
print("=== GiftInventoryUnit fields ===")
for f in GiftInventoryUnit._meta.fields:
    print(" -", f.name, "| default =", f.default)

print("")
print("=== DistributionAgreement fields ===")
for f in DistributionAgreement._meta.fields:
    print(" -", f.name)

print("")
print("=== SERVICES DISPONIBLES ===")

import gift_resellers.services as services

required = [
    "create_gift_inventory_unit",
    "distribute_gift_unit",
    "create_distribution_agreement",
    "accept_distribution_agreement",
    "lock_distribution_agreement",
]

for name in required:
    print(name, "=", hasattr(services, name))