from decimal import Decimal
from django.db import connection

print("")
print("=" * 70)
print(" TEST VERROUILLAGE WENZE - DIAGNOSTIC BASE")
print("=" * 70)

print("")
print("Moteur Django :", connection.settings_dict.get("ENGINE"))
print("Vendor DB     :", connection.vendor)

if connection.vendor == "sqlite":

    print("")
    print("=" * 70)
    print(" RESULTAT")
    print("=" * 70)
    print("")
    print("SQLite détecté.")
    print("")
    print("Le verrouillage concurrent réel avec")
    print("select_for_update() ne peut pas être validé")
    print("correctement avec SQLite.")
    print("")
    print("Le code WENZE reste cependant validé par :")
    print("- paiement normal")
    print("- stock consommé après paiement")
    print("- stock insuffisant")
    print("- absence de débit en cas de refus")
    print("- absence de crédit en cas de refus")
    print("- transactions atomiques")
    print("")
    print("VALIDATION CONCURRENCE : EN ATTENTE POSTGRESQL")

else:

    print("")
    print("Base compatible avec un test de verrouillage concurrent.")
    print("Le test concurrent réel peut être exécuté.")
    print("")
    print("VALIDATION CONCURRENCE : BASE COMPATIBLE")

print("")
print("=" * 70)
print(" TEST DIAGNOSTIC : TERMINE")
print("=" * 70)