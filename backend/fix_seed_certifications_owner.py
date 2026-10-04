import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")
django.setup()

from django.contrib.auth import get_user_model
from certification.models import NSIKAYCertification


print("=== SEED CERTIFICATIONS NSIKAY AVEC OWNER ===")


User = get_user_model()


admin = User.objects.filter(username="admin_test_nsikay").first()

if not admin:
    admin = User.objects.first()


if not admin:
    print("Aucun utilisateur disponible")
    exit()


certifications = [

    {
        "certification_type": "BANK",
        "activity": "Services financiers et bancaires",
        "document_reference": "NSK-CERT-BANK-001",
        "status": "VALIDE",
    },

    {
        "certification_type": "BUSINESS",
        "activity": "Entreprise partenaire NSIKAY",
        "document_reference": "NSK-CERT-BUS-001",
        "status": "VALIDE",
    },

    {
        "certification_type": "SPORT",
        "activity": "Agent sportif certifié NSIKAY",
        "document_reference": "NSK-CERT-SPORT-001",
        "status": "VALIDE",
    },

    {
        "certification_type": "HEALTH",
        "activity": "Service santé certifié NSIKAY",
        "document_reference": "NSK-CERT-HEALTH-001",
        "status": "VALIDE",
    },

]


for item in certifications:

    obj, created = NSIKAYCertification.objects.update_or_create(

        document_reference=item["document_reference"],

        defaults={
            **item,
            "owner": admin
        }

    )

    if created:
        print("CREATION :", obj.certification_type)
    else:
        print("MISE A JOUR :", obj.certification_type)



print("=== CERTIFICATIONS NSIKAY INITIALISEES ===")