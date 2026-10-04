from gift_resellers.models import (
    NetworkMember,
    ResellerNetwork,
    Reseller,
    GiftInventoryUnit,
)
from django.contrib.auth.models import User

reseller_user = User.objects.get(username="banque_test_nsikay")
member_user = User.objects.get(username="validation_test_nsikay")

print("")
print("============================================================")
print(" INSPECTION IDS MEMBRE / RESEAU / UNITE - SAFE")
print("============================================================")
print("")

print("USER REVENDEUR :", reseller_user.id, reseller_user.username)
print("USER MEMBRE    :", member_user.id, member_user.username)

def show_fields(obj, label):
    print("")
    print(label, "ID =", obj.id)
    for field in obj._meta.fields:
        name = field.name
        try:
            value = getattr(obj, name)
        except Exception:
            value = "<ERREUR>"
        if name != "id":
            print("  ", name, "=", value)

print("")
print("REVENDEURS DU USER :")

resellers = Reseller.objects.filter(user=reseller_user)

for reseller in resellers:
    show_fields(reseller, "RESELLER")

    networks = ResellerNetwork.objects.filter(reseller=reseller)

    print("  RESEAUX :", networks.count())

    for network in networks:
        show_fields(network, "  NETWORK")

        members = NetworkMember.objects.filter(
            network=network,
            user=member_user
        )

        print("    MEMBRES TROUVES :", members.count())

        for m in members:
            show_fields(m, "    MEMBER")

print("")
print("TOUS LES NETWORKMEMBER DU USER :")

all_members = NetworkMember.objects.filter(user=member_user)

print("TOTAL =", all_members.count())

for m in all_members:
    show_fields(m, "MEMBER")

print("")
print("UNITES DISTRIBUEES AU USER :")

units = (
    GiftInventoryUnit.objects
    .filter(current_member__user=member_user)
    .select_related(
        "current_member",
        "current_member__network",
        "current_reseller"
    )
    .order_by("-id")[:10]
)

print("TOTAL =", units.count())

for unit in units:
    print("")
    print("UNIT ID :", unit.id)
    print("UNIT CODE :", unit.unit_id)
    print("STATUS :", unit.status)
    print("CURRENT_RESELLER_ID :", unit.current_reseller_id)
    print("CURRENT_MEMBER_ID :", unit.current_member_id)

    if unit.current_member:
        print("MEMBER.USER_ID :", unit.current_member.user_id)
        print("MEMBER.NETWORK_ID :", unit.current_member.network_id)

    if unit.current_member and unit.current_member.network:
        print("MEMBER.NETWORK OBJECT :", unit.current_member.network)

print("")
print("============================================================")
print(" FIN INSPECTION SAFE")
print("============================================================")