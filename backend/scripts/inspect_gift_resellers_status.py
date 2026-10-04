from gift_resellers.models import (
    GiftInventoryUnit,
    DistributionAgreement,
)

print("")
print("============================================================")
print(" INSPECTION DES CHOIX DE STATUT GIFT RESELLERS")
print("============================================================")

for Model in [GiftInventoryUnit, DistributionAgreement]:
    print("")
    print("MODELE :", Model.__name__)
    print("")

    print("ATTRIBUT Status :", hasattr(Model, "Status"))

    if hasattr(Model, "Status"):
        print("Status :", Model.Status)

        for name in dir(Model.Status):
            if name.isupper():
                try:
                    print("  ", name, "=", getattr(Model.Status, name))
                except Exception:
                    pass

    print("")
    print("Champ status :")

    try:
        field = Model._meta.get_field("status")
        print("  type :", field.__class__.__name__)
        print("  default :", field.default)
        print("  choices :")

        for choice in field.choices:
            print("   ", choice)

    except Exception as exc:
        print("  ERREUR :", exc)

print("")
print("============================================================")
print(" FIN INSPECTION")
print("============================================================")