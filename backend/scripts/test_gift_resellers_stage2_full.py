from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError

from api_nsikay.models import VirtualGift

from gift_resellers.models import (
    Reseller,
    ResellerNetwork,
    NetworkMember,
    GiftInventoryUnit,
    DistributionAgreement,
    GiftResellerAuditLog,
)

from gift_resellers.services import (
    create_gift_inventory_unit,
    distribute_gift_unit,
    create_distribution_agreement,
    accept_distribution_agreement,
    lock_distribution_agreement,
)

User = get_user_model()

print("")
print("============================================================")
print(" TEST FONCTIONNEL COMPLET - REVENDEURS CADEAUX")
print("============================================================")

# ------------------------------------------------------------
# 1. Utilisateurs de test
# ------------------------------------------------------------

reseller_user, _ = User.objects.get_or_create(
    username="stage2_reseller_full_test",
    defaults={
        "email": "stage2_reseller_full_test@nsikay.test"
    },
)

member_user, _ = User.objects.get_or_create(
    username="stage2_member_full_test",
    defaults={
        "email": "stage2_member_full_test@nsikay.test"
    },
)

print("")
print("UTILISATEUR REVENDEUR :", reseller_user.username)
print("UTILISATEUR MEMBRE    :", member_user.username)

# ------------------------------------------------------------
# 2. Cadeau de référence
# ------------------------------------------------------------

gift = (
    VirtualGift.objects
    .filter(active=True)
    .order_by("value_eur", "id")
    .first()
)

if gift is None:
    raise RuntimeError("Aucun VirtualGift actif n'est disponible.")

print("")
print("CADEAU :", gift.name)
print("VALEUR OFFICIELLE EUR :", gift.reference_value_eur)

# ------------------------------------------------------------
# 3. Revendeur officiel
# ------------------------------------------------------------

reseller, _ = Reseller.objects.get_or_create(
    user=reseller_user,
    defaults={
        "status": Reseller.Status.ACTIVE,
        "reseller_code": "REV-STAGE2-FULL",
        "country_code": "FR",
    },
)

if reseller.status != Reseller.Status.ACTIVE:
    reseller.status = Reseller.Status.ACTIVE
    reseller.save(update_fields=["status"])

print("")
print("REVENDEUR :", reseller.reseller_code)
print("STATUT :", reseller.status)

# ------------------------------------------------------------
# 4. Réseau
# ------------------------------------------------------------

network, _ = ResellerNetwork.objects.get_or_create(
    principal_reseller=reseller,
    code="NET-STAGE2-FULL",
    defaults={
        "name": "Réseau Stage 2 Full Test"
    },
)

if not network.active:
    network.active = True
    network.save(update_fields=["active"])

print("RESEAU :", network.code)

# ------------------------------------------------------------
# 5. Membre
# ------------------------------------------------------------

member, _ = NetworkMember.objects.get_or_create(
    network=network,
    user=member_user,
    defaults={
        "active": True
    },
)

if not member.active:
    member.active = True
    member.save(update_fields=["active"])

print("MEMBRE :", member_user.username)
print("MEMBRE ACTIF :", member.active)

# ------------------------------------------------------------
# 6. Création d'une unité individuelle
# ------------------------------------------------------------

unit = create_gift_inventory_unit(
    gift=gift,
    source=GiftInventoryUnit.Source.RESELLER,
    reseller=reseller,
    official_value_eur=gift.reference_value_eur,
)

print("")
print("UNITÉ CRÉÉE")
print("ID :", unit.unit_id)
print("STATUT :", unit.status)
print("VALEUR OFFICIELLE :", unit.official_value_eur, "EUR")
print("REVENDEUR :", unit.current_reseller_id)

if not unit.unit_id.startswith("GFT-"):
    raise AssertionError(
        "L'identifiant individuel GFT- n'a pas été généré."
    )

if unit.official_value_eur != gift.reference_value_eur:
    raise AssertionError(
        "La valeur officielle du cadeau a été modifiée."
    )

if unit.status != GiftInventoryUnit.Status.AVAILABLE:
    raise AssertionError(
        "L'unité devrait être AVAILABLE."
    )

print("CREATION_UNITE = OK")

# ------------------------------------------------------------
# 7. Distribution commerciale
# ------------------------------------------------------------

unit = distribute_gift_unit(
    unit=unit,
    reseller=reseller,
    member=member_user,
)

print("")
print("DISTRIBUTION")
print("ID :", unit.unit_id)
print("STATUT :", unit.status)
print("MEMBRE :", unit.current_member_id)

if unit.status != GiftInventoryUnit.Status.DISTRIBUTED:
    raise AssertionError(
        "L'unité devrait être DISTRIBUTED."
    )

if unit.current_member_id != member.id:
    raise AssertionError(
        "Le cadeau n'est pas affecté au membre attendu."
    )

print("DISTRIBUTION_COMMERCIALE = OK")

# ------------------------------------------------------------
# 8. Accord commercial
# ------------------------------------------------------------

agreement = create_distribution_agreement(
    principal_reseller=reseller,
    network_member=member,
    gift=gift,
    quantity=1,
    member_percentage="60.00",
    principal_reseller_percentage="30.00",
    other_percentage="5.00",
)

print("")
print("ACCORD CRÉÉ")
print("ID :", agreement.pk)
print("VERSION :", agreement.version)
print("STATUT :", agreement.status)
print("MEMBRE :", agreement.member_percentage, "%")
print(
    "REVENDEUR PRINCIPAL :",
    agreement.principal_reseller_percentage,
    "%"
)
print("NSIKAY :", agreement.nsikay_percentage, "%")
print("AUTRE :", agreement.other_percentage, "%")

if agreement.nsikay_percentage != 5:
    raise AssertionError(
        "La commission NSIKAY doit être exactement 5 %."
    )

total = (
    agreement.member_percentage
    + agreement.principal_reseller_percentage
    + agreement.nsikay_percentage
    + agreement.other_percentage
)

print("TOTAL REPARTITION :", total, "%")

if total > 100:
    raise AssertionError(
        "La répartition dépasse 100 %."
    )

print("ACCORD_CREATION = OK")

# ------------------------------------------------------------
# 9. Acceptation
# ------------------------------------------------------------

agreement = accept_distribution_agreement(
    agreement=agreement
)

print("")
print("ACCORD ACCEPTÉ")
print("STATUT :", agreement.status)
print("ACCEPTED_AT :", agreement.accepted_at)

if agreement.status != DistributionAgreement.Status.ACCEPTED:
    raise AssertionError(
        "L'accord devrait être ACCEPTED."
    )

print("ACCEPTATION = OK")

# ------------------------------------------------------------
# 10. Verrouillage
# ------------------------------------------------------------

agreement = lock_distribution_agreement(
    agreement=agreement
)

print("")
print("ACCORD VERROUILLÉ")
print("STATUT :", agreement.status)
print("LOCKED_AT :", agreement.locked_at)

if agreement.status != DistributionAgreement.Status.LOCKED:
    raise AssertionError(
        "L'accord devrait être LOCKED."
    )

if agreement.locked_at is None:
    raise AssertionError(
        "LOCKED doit avoir une date de verrouillage."
    )

print("VERROUILLAGE = OK")

# ------------------------------------------------------------
# 11. Test d'immutabilité
# ------------------------------------------------------------

original_percentage = agreement.member_percentage

agreement.member_percentage = "61.00"

immutability_blocked = False

try:
    agreement.save()
except ValueError as exc:
    immutability_blocked = True
    print("")
    print("MODIFICATION REFUSÉE :", str(exc))

if not immutability_blocked:
    raise AssertionError(
        "ERREUR : un accord LOCKED a pu être modifié."
    )

agreement.refresh_from_db()

if agreement.member_percentage != original_percentage:
    raise AssertionError(
        "La valeur historique de l'accord a été modifiée."
    )

print("IMMUTABILITE = OK")

# ------------------------------------------------------------
# 12. Audit
# ------------------------------------------------------------

audit_count = GiftResellerAuditLog.objects.filter(
    reference__in=[
        unit.unit_id,
        f"AGR-{agreement.pk}-V{agreement.version}",
    ]
).count()

print("")
print("AUDIT ASSOCIÉ :", audit_count)

if audit_count < 3:
    raise AssertionError(
        "La traçabilité attendue n'a pas été créée."
    )

print("AUDIT = OK")

# ------------------------------------------------------------
# 13. Vérification finale du cadeau
# ------------------------------------------------------------

unit.refresh_from_db()

print("")
print("============================================================")
print(" ETAT FINAL DU CADEAU")
print("============================================================")
print("ID INDIVIDUEL :", unit.unit_id)
print("CADEAU :", unit.gift.name)
print("VALEUR OFFICIELLE EUR :", unit.official_value_eur)
print("SOURCE :", unit.source)
print("CREDIT ONLY :", unit.credit_only)
print("STATUT :", unit.status)
print("REVENDEUR :", unit.current_reseller_id)
print("MEMBRE :", unit.current_member_id)

if unit.official_value_eur != gift.reference_value_eur:
    raise AssertionError(
        "La valeur officielle EUR a été altérée."
    )

print("")
print("============================================================")
print(" RESULTATS")
print("============================================================")
print("CREATION_UNITE = OK")
print("DISTRIBUTION_COMMERCIALE = OK")
print("ACCORD_CREATION = OK")
print("ACCEPTATION = OK")
print("VERROUILLAGE = OK")
print("IMMUTABILITE = OK")
print("AUDIT = OK")
print("VALEUR_OFFICIELLE_IMMUTABLE = OK")
print("")
print("TEST_STAGE2_COMPLET = OK")
print("============================================================")