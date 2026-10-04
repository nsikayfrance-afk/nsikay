from gift_resellers.models import (
    GiftInventoryUnit,
    NetworkMember,
    Reseller,
)

print("")
print("============================================================")
print(" INSPECTION RELATIONS GIFT RESELLERS")
print("============================================================")

for Model, fields in [
    (
        GiftInventoryUnit,
        ["current_reseller", "current_member", "gift", "status"]
    ),
    (
        NetworkMember,
        ["network", "user", "active"]
    ),
    (
        Reseller,
        ["user", "status"]
    ),
]:
    print("")
    print("MODELE :", Model.__name__)

    for field_name in fields:
        try:
            field = Model._meta.get_field(field_name)

            print("")
            print("CHAMP :", field_name)
            print("TYPE :", field.__class__.__name__)
            print("REMOTE :", getattr(field, "remote_field", None))

            if getattr(field, "remote_field", None):
                remote = field.remote_field.model
                print("MODELE CIBLE :", remote)

        except Exception as exc:
            print("CHAMP", field_name, "ERREUR :", exc)

print("")
print("============================================================")
print(" RELATIONS EXACTES")
print("============================================================")

unit_member = GiftInventoryUnit._meta.get_field("current_member")

if unit_member.remote_field:
    print(
        "GiftInventoryUnit.current_member ->",
        unit_member.remote_field.model
    )

network_member_user = NetworkMember._meta.get_field("user")

if network_member_user.remote_field:
    print(
        "NetworkMember.user ->",
        network_member_user.remote_field.model
    )

network_member_network = NetworkMember._meta.get_field("network")

if network_member_network.remote_field:
    print(
        "NetworkMember.network ->",
        network_member_network.remote_field.model
    )

print("")
print("============================================================")
print(" FIN INSPECTION")
print("============================================================")