from django.core.management import execute_from_command_line
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()


from administration.models import (
    CountrySupervisionDetail,
    BankPartner
)


print("=== INITIALISATION SUPERVISION PAYS NSIKAY ===")


# Récupération banques partenaires

rdc_bank = BankPartner.objects.filter(
    code="NSK-RDC"
).first()


international_bank = BankPartner.objects.filter(
    code="NSK-INT"
).first()


# RDC

rdc, created = CountrySupervisionDetail.objects.update_or_create(

    code_iso="CD",

    defaults={

        "pays":
        "République Démocratique du Congo",

        "actif":
        True,

        "devises_autorisees":
        [
            "CDF",
            "USD"
        ],

        "niveau_conformite":
        "valide"
    }

)


if rdc_bank:
    rdc.banques_autorisees.add(
        rdc_bank
    )


# International

international, created = CountrySupervisionDetail.objects.update_or_create(

    code_iso="INT",

    defaults={

        "pays":
        "International",

        "actif":
        True,

        "devises_autorisees":
        [
            "EUR",
            "USD"
        ],

        "niveau_conformite":
        "valide"
    }

)


if international_bank:
    international.banques_autorisees.add(
        international_bank
    )


print("=== PAYS NSIKAY INITIALISES ===")