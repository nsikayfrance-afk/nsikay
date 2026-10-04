import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

print("")
print("============================================================")
print(" NSIKAY - DIAGNOSTIC GROUPES CERTIFICATION")
print("============================================================")

print("")
print(">>> GROUPES PRESENTS")

groups = Group.objects.all().order_by("name")

if not groups.exists():
    print("AUCUN_GROUPE")
else:
    for group in groups:
        print(
            f"GROUP_ID={group.id} | "
            f"NAME={group.name}"
        )

print("")
print(">>> RECHERCHE AUTORITE CERTIFICATION")

matches = Group.objects.filter(
    name__icontains="certification"
).order_by("name")

if not matches.exists():
    print("CERTIFICATION_GROUP_MATCH=0")
else:
    for group in matches:
        print(
            f"CERTIFICATION_GROUP_ID={group.id} | "
            f"NAME={group.name}"
        )

print("")
print(">>> UTILISATEUR DORIS")

doris = (
    User.objects
    .filter(username="DORIS")
    .first()
)

if doris is None:
    print("DORIS=INTROUVABLE")
else:
    print(
        f"DORIS_ID={doris.id} | "
        f"ACTIVE={doris.is_active} | "
        f"STAFF={doris.is_staff} | "
        f"SUPERUSER={doris.is_superuser}"
    )

    user_groups = doris.groups.all().order_by("name")

    if not user_groups.exists():
        print("DORIS_GROUPS=0")
    else:
        for group in user_groups:
            print(
                f"DORIS_GROUP_ID={group.id} | "
                f"NAME={group.name}"
            )

print("")
print(">>> RECHERCHE GROUPES ATTENDUS")

expected = [
    "Super Administrateur",
    "Administration Pays",
    "Autorité Certification",
    "Banque Partenaire",
    "Contrôleur Financier",
    "Gestionnaire WENZE",
    "Agent Validation",
    "Superviseur Conformité",
    "Gestionnaire Publicité",
    "Gestionnaire Événements",
]

for name in expected:

    exists = Group.objects.filter(
        name=name
    ).exists()

    print(
        f"EXPECTED_GROUP={name} | "
        f"EXISTS={exists}"
    )

print("")
print("DIAGNOSTIC_GROUPES_TERMINE")
print("AUCUNE_MODIFICATION")
