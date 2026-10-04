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
from django.utils import timezone

from service_control.models import (
    CountryServiceStatus,
    ServiceActivation,
)

from service_dashboard.models import (
    OperationalCountryConfigurationLog,
)


# ============================================================
# CONFIGURATION OFFICIELLE
# ============================================================

EXCLUDED_CODES = {
    "ATA",
    "BVT",
    "IOT",
    "ATF",
    "HMD",
    "PCN",
    "SGS",
    "UMI",
    "SJM",
}

EXPECTED_PRIMARY = 249
EXPECTED_OPERATIONAL = 240
EXPECTED_EXCLUDED = 9
EXPECTED_ACTIVATIONS = 10472


print("")
print("=" * 70)
print(" NSIKAY - VALIDATION AVANT ACTIVATION")
print("=" * 70)

primary = (
    CountryServiceStatus.objects
    .filter(is_primary=True)
)

activation_count_before = ServiceActivation.objects.count()

print(
    "PAYS_ISO_PRINCIPAUX =",
    primary.count()
)

print(
    "PAYS_OPERATIONNELS_AVANT =",
    primary.filter(is_operational=True).count()
)

print(
    "ACTIVATIONS_AVANT =",
    activation_count_before
)

# ============================================================
# CONTROLES PREALABLES
# ============================================================

if primary.count() != EXPECTED_PRIMARY:
    raise RuntimeError(
        f"Nombre de pays principaux incorrect : "
        f"{primary.count()} au lieu de {EXPECTED_PRIMARY}."
    )

if activation_count_before != EXPECTED_ACTIVATIONS:
    raise RuntimeError(
        f"Nombre d'activations inattendu : "
        f"{activation_count_before} au lieu de "
        f"{EXPECTED_ACTIVATIONS}."
    )

available_codes = set(
    primary.values_list(
        "country_code",
        flat=True
    )
)

missing_codes = sorted(
    EXCLUDED_CODES - available_codes
)

if missing_codes:
    raise RuntimeError(
        "Codes ISO3 d'exclusion inexistants : "
        + ", ".join(missing_codes)
    )

# ============================================================
# CALCUL DES 240 PAYS
# ============================================================

operational_codes = available_codes - EXCLUDED_CODES

if len(operational_codes) != EXPECTED_OPERATIONAL:
    raise RuntimeError(
        f"Calcul invalide : {len(operational_codes)} "
        f"pays operationnels au lieu de "
        f"{EXPECTED_OPERATIONAL}."
    )

if len(EXCLUDED_CODES) != EXPECTED_EXCLUDED:
    raise RuntimeError(
        "Le nombre d'exclusions n'est pas egal a 9."
    )

print("")
print("CONTROLES PREALABLES = OK")
print(
    "240 pays operationnels calcules =",
    len(operational_codes)
)

print(
    "9 exclusions calculees =",
    len(EXCLUDED_CODES)
)

# ============================================================
# TRANSACTION ATOMIQUE
# ============================================================

with transaction.atomic():

    # Verrouillage des lignes principales
    locked = list(
        CountryServiceStatus.objects
        .select_for_update()
        .filter(is_primary=True)
    )

    if len(locked) != EXPECTED_PRIMARY:
        raise RuntimeError(
            "Le nombre de lignes verrouillees est incorrect."
        )

    # Remise a zero controlee uniquement du champ
    # is_operational des pays principaux.
    CountryServiceStatus.objects.filter(
        is_primary=True
    ).update(
        is_operational=False
    )

    # Activation exacte des 240 pays.
    updated = (
        CountryServiceStatus.objects
        .filter(
            is_primary=True,
            country_code__in=operational_codes
        )
        .update(
            is_operational=True
        )
    )

    if updated != EXPECTED_OPERATIONAL:
        raise RuntimeError(
            f"Seulement {updated} pays ont ete actives "
            f"au lieu de {EXPECTED_OPERATIONAL}."
        )

    # Verification immediate.
    final_primary = (
        CountryServiceStatus.objects
        .filter(is_primary=True)
    )

    final_operational = (
        final_primary
        .filter(is_operational=True)
        .count()
    )

    final_excluded = (
        final_primary
        .filter(is_operational=False)
        .count()
    )

    if final_operational != EXPECTED_OPERATIONAL:
        raise RuntimeError(
            f"Verification operationnelle echouee : "
            f"{final_operational} au lieu de "
            f"{EXPECTED_OPERATIONAL}."
        )

    if final_excluded != EXPECTED_EXCLUDED:
        raise RuntimeError(
            f"Verification exclusions echouee : "
            f"{final_excluded} au lieu de "
            f"{EXPECTED_EXCLUDED}."
        )

    # Controle des ServiceActivation.
    activation_count_after = (
        ServiceActivation.objects.count()
    )

    if activation_count_after != EXPECTED_ACTIVATIONS:
        raise RuntimeError(
            "Le nombre de ServiceActivation a change."
        )

    # Journal administratif.
    OperationalCountryConfigurationLog.objects.create(
        admin_user="constantdoriskayembe",
        selected_count=EXPECTED_OPERATIONAL,
        selected_codes=",".join(
            sorted(operational_codes)
        ),
        action="configuration_officielle_240_pays",
    )

# ============================================================
# CONTROLE FINAL APRES TRANSACTION
# ============================================================

primary = (
    CountryServiceStatus.objects
    .filter(is_primary=True)
)

operational = primary.filter(
    is_operational=True
)

excluded = primary.filter(
    is_operational=False
)

activations = ServiceActivation.objects.count()

logs = OperationalCountryConfigurationLog.objects.count()

print("")
print("=" * 70)
print(" CONTROLE FINAL NSIKAY")
print("=" * 70)

print(
    "LIGNES_PAYS =",
    CountryServiceStatus.objects.count()
)

print(
    "PAYS_ISO_PRINCIPAUX =",
    primary.count()
)

print(
    "PAYS_OPERATIONNELS =",
    operational.count()
)

print(
    "PAYS_EXCLUS =",
    excluded.count()
)

print(
    "ACTIVATIONS =",
    activations
)

print(
    "JOURNAUX_CONFIGURATION =",
    logs
)

# ============================================================
# INTEGRITE FINALE
# ============================================================

assert CountryServiceStatus.objects.count() == 374
assert primary.count() == 249
assert operational.count() == 240
assert excluded.count() == 9
assert activations == 10472

print("")
print("=" * 70)
print(" INTEGRITE FINALE = OK")
print("=" * 70)
print("")
print("249 pays principaux")
print("240 pays operationnels")
print("9 pays exclus")
print("10 472 ServiceActivation conservees")
print("Journal administratif cree")
print("")
print("Aucune activation automatique des services/pays.")
print("La configuration des pays reste distincte")
print("de l'activation individuelle des services.")
print("")

