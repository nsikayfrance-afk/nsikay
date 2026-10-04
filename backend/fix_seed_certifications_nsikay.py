import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

django.setup()


from certification.models import NSIKAYCertification


print("=== INITIALISATION CERTIFICATIONS NSIKAY CORRIGEE ===")


certifications = [

    {
        "certification_type": "banque",
        "activity": "Services bancaires NSIKAY",
        "document_reference": "CERT-BANK-RDC-001",
        "status": "approved",
    },

    {
        "certification_type": "banque",
        "activity": "Services bancaires internationaux NSIKAY",
        "document_reference": "CERT-BANK-INT-001",
        "status": "approved",
    },

    {
        "certification_type": "service",
        "activity": "NSIKAY Wallet",
        "document_reference": "CERT-WALLET-001",
        "status": "approved",
    }

]


for item in certifications:

    obj = NSIKAYCertification.objects.create(
        **item
    )

    print(
        obj.id,
        obj.certification_type,
        obj.activity,
        obj.status
    )


print("=== CERTIFICATIONS CREEES ===")