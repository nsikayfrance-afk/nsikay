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
print(" INSPECTION IDS MEMBRE / RESEAU / UNITE")
print("============================================================")
print("")

print("USER REVENDEUR :", reseller_user.id, reseller_user.username)
print("USER MEMBRE    :", member_user.id, member_user.username)

print("")
print("RESEAUX DU REVENDEUR :")

resellers = Reseller.objects.filter(user=reseller_user)

for reseller in resellers:
    print(
        "RESELLER:",
        reseller.id,
        "CODE:",
        reseller.code,
        "STATUS:",
        reseller.status
    )

    networks = ResellerNetwork.objects.filter(reseller=reseller)

    for network in networks:
        print(
            "  NETWORK:",
            network.id,
            "CODE:",
            network.code
        )

        members = NetworkMember.objects.filter(
            network=network,
            user=member_user
        )

        for m in members:
            print(
                "    MEMBER:",
                m.id,
                "USER:",
                m.user_id,
                "ACTIVE:",
                m.active
            )

print("")
print("TOUS LES NETWORKMEMBER DU USER :")

all_members = NetworkMember.objects.filter(user=member_user)

for m in all_members:
    print(
        "MEMBER:",
        m.id,
        "NETWORK:",
        m.network_id,
        "NETWORK_CODE:",
        m.network.code,
        "RESELLER:",
        m.network.reseller_id,
        "ACTIVE:",
        m.active
    )

print("")
print("UNITES DISTRIBUEES RECENTES :")

units = (
    GiftInventoryUnit.objects
    .filter(current_member__user=member_user)
    .select_related("current_member", "current_member__network")
    .order_by("-id")[:10]
)

for unit in units:
    print(
        "UNIT:",
        unit.id,
        unit.unit_id,
        "| MEMBER:",
        unit.current_member_id,
        "| USER:",
        unit.current_member.user_id,
        "| NETWORK:",
        unit.current_member.network_id,
        "| NETWORK_CODE:",
        unit.current_member.network.code,
        "| RESELLER:",
        unit.current_reseller_id,
        "| STATUS:",
        unit.status
    )

print("")
print("============================================================")
print(" FIN INSPECTION")
print("============================================================")