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
print(" INSPECTION IDS MEMBRE / RESEAU / UNITE - SAFE 2")
print("============================================================")
print("")

print("USER REVENDEUR :", reseller_user.id, reseller_user.username)
print("USER MEMBRE    :", member_user.id, member_user.username)

resellers = Reseller.objects.filter(user=reseller_user)

print("")
print("REVENDEURS :", resellers.count())

for reseller in resellers:

    print("")
    print(
        "RESELLER:",
        reseller.id,
        "| CODE:",
        reseller.reseller_code,
        "| STATUS:",
        reseller.status
    )

    networks = ResellerNetwork.objects.filter(
        principal_reseller=reseller
    )

    print("  RESEAUX :", networks.count())

    for network in networks:

        print(
            "  NETWORK:",
            network.id,
            "| CODE:",
            network.code,
            "| NAME:",
            network.name,
            "| ACTIVE:",
            network.active,
            "| PRINCIPAL_RESELLER:",
            network.principal_reseller_id
        )

        members = NetworkMember.objects.filter(
            network=network,
            user=member_user
        )

        print("    MEMBRES DU USER :", members.count())

        for m in members:
            print(
                "    MEMBER:",
                m.id,
                "| USER:",
                m.user_id,
                "| NETWORK:",
                m.network_id,
                "| ACTIVE:",
                m.active
            )

print("")
print("============================================================")
print(" TOUS LES NETWORKMEMBER DU USER")
print("============================================================")

all_members = NetworkMember.objects.filter(
    user=member_user
)

print("TOTAL :", all_members.count())

for m in all_members:
    print(
        "MEMBER:",
        m.id,
        "| USER:",
        m.user_id,
        "| NETWORK:",
        m.network_id,
        "| NETWORK_CODE:",
        m.network.code,
        "| PRINCIPAL_RESELLER:",
        m.network.principal_reseller_id,
        "| ACTIVE:",
        m.active
    )

print("")
print("============================================================")
print(" UNITES DISTRIBUEES AU USER")
print("============================================================")

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

print("TOTAL :", units.count())

for unit in units:

    print("")
    print("UNIT ID :", unit.id)
    print("UNIT CODE :", unit.unit_id)
    print("STATUS :", unit.status)
    print("CURRENT_RESELLER_ID :", unit.current_reseller_id)
    print("CURRENT_MEMBER_ID :", unit.current_member_id)

    if unit.current_member:
        print(
            "MEMBER.USER_ID :",
            unit.current_member.user_id
        )

        print(
            "MEMBER.NETWORK_ID :",
            unit.current_member.network_id
        )

        print(
            "MEMBER.NETWORK_CODE :",
            unit.current_member.network.code
        )

        print(
            "MEMBER.PRINCIPAL_RESELLER_ID :",
            unit.current_member.network.principal_reseller_id
        )

print("")
print("============================================================")
print(" FIN INSPECTION SAFE 2")
print("============================================================")