from django.contrib.auth import get_user_model

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
print(" TEST FONCTIONNEL STAGE 2 - VERSION 2")
print("============================================================")

# ------------------------------------------------------------
# Utilisateurs existants
# ------------------------------------------------------------

reseller_user = User.objects.filter(
    username="banque_test_nsikay"
).first()

member_user = User.objects.filter(
    username="validation_test_nsikay"
).first()

if reseller_user is None:
    reseller_user = User.objects.order_by("id").first()

if member_user is None:
    member_user = (
        User.objects
        .exclude(pk=reseller_user.pk)
        .order_by("id")
        .first()
    )

if reseller_user is None or member_user is None:
    raise RuntimeError(
        "Deux utilisateurs existants sont nécessaires pour le test."
    )

print("")
print("REVENDEUR UTILISATEUR :", reseller_user.username)
print("MEMBRE UTILISATEUR    :", member_user.username)

# ------------------------------------------------------------
# Cadeau
# ------------------------------------------------------------

gift = (
    VirtualGift.objects
    .filter(active=True)
    .order_by("value_eur", "id")
    .first()
)

if gift is None:
    raise RuntimeError(
        "Aucun cadeau actif disponible."
    )

print("")
print("CADEAU :", gift.name)
print("VALEUR OFFICIELLE :", gift.reference_value_eur, "EUR")

# ------------------------------------------------------------
# Revendeur
# ------------------------------------------------------------

reseller = Reseller.objects.filter(
    user=reseller_user
).first()

if reseller is None:
    reseller = Reseller.objects.create(
        user=reseller_user,
        status="ACTIVE",
        reseller_code="REV-STAGE2-V2",
        country_code="FR",
    )
elif reseller.status != "ACTIVE":
    reseller.status = "ACTIVE"
    reseller.save(update_fields=["status"])

print("")
print("REVENDEUR :", reseller.reseller_code)
print("STATUT :", reseller.status)

# ------------------------------------------------------------
# Réseau
# ------------------------------------------------------------

network = ResellerNetwork.objects.filter(
    principal_reseller=reseller,
    code="NET-STAGE2-V2",
).first()

if network is None:
    network = ResellerNetwork.objects.create(
        principal_reseller=reseller,
        name="Réseau Stage 2 V2",
        code="NET-STAGE2-V2",
        active=True,
    )
elif not network.active:
    network.active = True
    network.save(update_fields=["active"])

print("RESEAU :", network.code)

# ------------------------------------------------------------
# Membre
# ------------------------------------------------------------

member = NetworkMember.objects.filter(
    network=network,
    user=member_user,
).first()

if member is None:
    member = NetworkMember.objects.create(
        network=network,
        user=member_user,
        active=True,
    )
elif not member.active:
    member.active = True
    member.save(update_fields=["active"])

print("MEMBRE :", member_user.username)
print("MEMBRE ACTIF :", member.active)

# ------------------------------------------------------------
# Unité individuelle
# ------------------------------------------------------------

unit = create_gift_inventory_unit(
    gift=gift,
    source="RESELLER",
    reseller=reseller,
    official_value_eur=gift.reference_value_eur,
)

print("")
print("UNITÉ CRÉÉE")
print("ID :", unit.unit_id)
print("STATUT :", unit.status)
print("VALEUR :", unit.official_value_eur, "EUR")

if not unit.unit_id.startswith("GFT-"):
    raise AssertionError(
        "L'identifiant individuel GFT- est absent."
    )

if unit.official_value_eur != gift.reference_value_eur:
    raise AssertionError(
        "La valeur officielle EUR est incorrecte."
    )

if unit.status != "AVAILABLE":
    raise AssertionError(
        "L'unité doit être AVAILABLE."
    )

print("CREATION_UNITE = OK")

# ------------------------------------------------------------
# Distribution
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
print("MEMBRE ID :", unit.current_member_id)

if unit.status != "DISTRIBUTED":
    raise AssertionError(
        "L'unité doit être DISTRIBUTED."
    )

if unit.current_member_id != member.id:
    raise AssertionError(
        "Le membre associé est incorrect."
    )

print("DISTRIBUTION_COMMERCIALE = OK")

# ------------------------------------------------------------
# Accord commercial
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

total = (
    agreement.member_percentage
    + agreement.principal_reseller_percentage
    + agreement.nsikay_percentage
    + agreement.other_percentage
)

if agreement.nsikay_percentage != 5:
    raise AssertionError(
        "La commission NSIKAY doit être exactement 5 %."
    )

if total > 100:
    raise AssertionError(
        "La répartition dépasse 100 %."
    )

print("ACCORD_CREATION = OK")

# ------------------------------------------------------------
# Acceptation
# ------------------------------------------------------------

agreement = accept_distribution_agreement(
    agreement=agreement
)

print("")
print("ACCORD ACCEPTÉ")
print("STATUT :", agreement.status)

if agreement.status != "ACCEPTED":
    raise AssertionError(
        "L'accord doit être ACCEPTED."
    )

print("ACCEPTATION = OK")

# ------------------------------------------------------------
# Verrouillage
# ------------------------------------------------------------

agreement = lock_distribution_agreement(
    agreement=agreement
)

print("")
print("ACCORD VERROUILLÉ")
print("STATUT :", agreement.status)
print("LOCKED_AT :", agreement.locked_at)

if agreement.status != "LOCKED":
    raise AssertionError(
        "L'accord doit être LOCKED."
    )

if agreement.locked_at is None:
    raise AssertionError(
        "Un accord LOCKED doit avoir locked_at."
    )

print("VERROUILLAGE = OK")

# ------------------------------------------------------------
# Immutabilité
# ------------------------------------------------------------

original_percentage = agreement.member_percentage

agreement.member_percentage = "61.00"

blocked = False

try:
    agreement.save()
except ValueError as exc:
    blocked = True
    print("")
    print("MODIFICATION REFUSÉE :", str(exc))

if not blocked:
    raise AssertionError(
        "ERREUR : un accord LOCKED a pu être modifié."
    )

agreement.refresh_from_db()

if agreement.member_percentage != original_percentage:
    raise AssertionError(
        "La valeur historique de l'accord a changé."
    )

print("IMMUTABILITE = OK")

# ------------------------------------------------------------
# Audit
# ------------------------------------------------------------

audit_count = GiftResellerAuditLog.objects.filter(
    reference__in=[
        unit.unit_id,
        f"AGR-{agreement.pk}-V{agreement.version}",
    ]
).count()

print("")
print("AUDIT :", audit_count)

if audit_count < 3:
    raise AssertionError(
        "La traçabilité attendue est insuffisante."
    )

print("AUDIT = OK")

# ------------------------------------------------------------
# Vérification finale
# ------------------------------------------------------------

unit.refresh_from_db()
agreement.refresh_from_db()

print("")
print("============================================================")
print(" ETAT FINAL")
print("============================================================")
print("CADEAU :", unit.gift.name)
print("ID INDIVIDUEL :", unit.unit_id)
print("VALEUR OFFICIELLE EUR :", unit.official_value_eur)
print("SOURCE :", unit.source)
print("CREDIT ONLY :", unit.credit_only)
print("STATUT CADEAU :", unit.status)
print("REVENDEUR :", unit.current_reseller_id)
print("MEMBRE :", unit.current_member_id)
print("")
print("ACCORD :", agreement.pk)
print("VERSION :", agreement.version)
print("STATUT ACCORD :", agreement.status)
print("NSIKAY :", agreement.nsikay_percentage, "%")

print("")
print("============================================================")
print(" RESULTATS STAGE 2")
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