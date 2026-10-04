import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "nsikay.settings"
)

import django
django.setup()

from django.db import transaction
from service_control.models import (
    CountryServiceStatus,
    ServiceActivation,
)
from service_dashboard.models import (
    OperationalCountryConfigurationLog,
)

EXPECTED_PRIMARY = 249
EXPECTED_OPERATIONAL = 240
EXPECTED_EXCLUDED = 9
EXPECTED_ACTIVATIONS = 10472

ADMIN_USER = "constantdoriskayembe"
ACTION = "configuration_officielle_240_pays"

with transaction.atomic():

    primary = CountryServiceStatus.objects.filter(
        is_primary=True
    )

    operational = primary.filter(
        is_operational=True
    )

    excluded = primary.filter(
        is_operational=False
    )

    activation_count = ServiceActivation.objects.count()

    # --------------------------------------------------------
    # CONTROLES AVANT JOURNALISATION
    # --------------------------------------------------------

    if primary.count() != EXPECTED_PRIMARY:
        raise RuntimeError(
            f"249 pays principaux attendus, "
            f"{primary.count()} trouves."
        )

    if operational.count() != EXPECTED_OPERATIONAL:
        raise RuntimeError(
            f"240 pays operationnels attendus, "
            f"{operational.count()} trouves."
        )

    if excluded.count() != EXPECTED_EXCLUDED:
        raise RuntimeError(
            f"9 exclusions attendues, "
            f"{excluded.count()} trouvees."
        )

    if activation_count != EXPECTED_ACTIVATIONS:
        raise RuntimeError(
            f"10 472 activations attendues, "
            f"{activation_count} trouvees."
        )

    selected_codes = sorted(
        operational.values_list(
            "country_code",
            flat=True
        )
    )

    selected_codes_text = ",".join(selected_codes)

    # --------------------------------------------------------
    # VERIFICATION D'UN JOURNAL EXISTANT
    # --------------------------------------------------------

    existing = (
        OperationalCountryConfigurationLog.objects
        .filter(
            action=ACTION,
            selected_count=EXPECTED_OPERATIONAL,
            selected_codes=selected_codes_text,
        )
        .order_by("-created_at")
        .first()
    )

    if existing:
        log = existing
        created = False
    else:
        log = (
            OperationalCountryConfigurationLog.objects.create(
                admin_user=ADMIN_USER,
                selected_count=EXPECTED_OPERATIONAL,
                selected_codes=selected_codes_text,
                action=ACTION,
            )
        )
        created = True

# ------------------------------------------------------------
# VERIFICATION
# ------------------------------------------------------------

journal_count = (
    OperationalCountryConfigurationLog.objects.count()
)

print("")
print("=" * 70)
print(" JOURNAL ADMINISTRATIF NSIKAY")
print("=" * 70)

print("")
print("ID JOURNAL =", log.id)
print("ADMINISTRATEUR =", log.admin_user)
print("ACTION =", log.action)
print("PAYS OPERATIONNELS =", log.selected_count)
print("DATE =", log.created_at)
print("JOURNAL CREE =", "OUI" if created else "DEJA EXISTANT")
print("TOTAL JOURNAUX =", journal_count)

print("")
print("CONTROLE :")
print("249 PAYS PRINCIPAUX =", primary.count())
print("240 OPERATIONNELS =", operational.count())
print("9 EXCLUS =", excluded.count())
print("10 472 ACTIVATIONS =", activation_count)

assert primary.count() == 249
assert operational.count() == 240
assert excluded.count() == 9
assert activation_count == 10472
assert log.selected_count == 240
assert log.admin_user == ADMIN_USER
assert log.action == ACTION

print("")
print("=" * 70)
print(" JOURNAL ADMINISTRATIF VALIDE = OK")
print("=" * 70)
print("")

