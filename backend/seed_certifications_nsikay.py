import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

django.setup()


from certification.models import NSIKAYCertification


print("=== INITIALISATION CERTIFICATIONS NSIKAY ===")


certifications = [

    {
        "type_certification": "banque",
        "nom_entite": "NSIKAY Bank RDC",
        "reference": "CERT-BANK-RDC-001",
        "statut": "valide",
        "valide_par": "Administration NSIKAY"
    },

    {
        "type_certification": "banque",
        "nom_entite": "NSIKAY Bank International",
        "reference": "CERT-BANK-INT-001",
        "statut": "valide",
        "valide_par": "Administration NSIKAY"
    },

    {
        "type_certification": "service",
        "nom_entite": "Portefeuille NSIKAY Wallet",
        "reference": "CERT-SERVICE-WALLET-001",
        "statut": "valide",
        "valide_par": "Administration NSIKAY"
    }

]


for item in certifications:

    obj, created = NSIKAYCertification.objects.update_or_create(

        reference=item["reference"],

        defaults=item

    )

    print(
        obj.nom_entite,
        "=>",
        obj.statut
    )


print("=== CERTIFICATIONS NSIKAY TERMINEES ===")