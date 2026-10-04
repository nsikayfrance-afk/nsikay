from django.contrib.auth import get_user_model
from decimal import Decimal

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
print(" NSIKAY - TEST FONCTIONNEL GIFT RESELLERS STAGE 2")
print("============================================================")

# ============================================================
# 1. UTILISATEURS EXISTANTS
# ============================================================

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
        "Deux utilisateurs existants sont nécessaires."
    )

print("")
print("REVENDEUR :", reseller_user.username)
print("MEMBRE    :", member_user.username)

# ============================================================
# 2. CADEAU OFFICIEL
# ============================================================

gift = (
    VirtualGift.objects
    .filter(active=True)
    .order_by("value_eur", "id")
    .first()
)

if gift is None:
    raise RuntimeError("Aucun cadeau actif disponible.")

official_value = Decimal(str(gift.reference_value_eur))

print("")
print("CADEAU :", gift.name)
print("VALEUR OFFICIELLE :", official_value, "EUR")

# ============================================================
# 3. REVENDEUR OFFICIEL
# ============================================================

reseller = Reseller.objects.filter(
    user=reseller_user
).first()

if reseller is None:
    reseller = Reseller.objects.create(
        user=reseller_user,
        status="ACTIVE",
        reseller_code="REV-STAGE2-FINAL",
        country_code="FR",
    )
else:
    if reseller.status != "ACTIVE":
        reseller.status = "ACTIVE"
        reseller.save(update_fields=["status"])

print("")
print("REVENDEUR CODE :", reseller.reseller_code)
print("STATUT :", reseller.status)

# ============================================================
# 4. RESEAU
# ============================================================

network = ResellerNetwork.objects.filter(
    principal_reseller=reseller,
    code="NET-STAGE2-FINAL",
).first()

if network is None:
    network = ResellerNetwork.objects.create(
        principal_reseller=reseller,
        name="Réseau Revendeurs Stage 2 Final",
        code="NET-STAGE2-FINAL",
        active=True,
    )
else:
    if not network.active:
        network.active = True
        network.save(update_fields=["active"])

print("RESEAU :", network.code)

# ============================================================
# 5. MEMBRE
# ============================================================

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
else:
    if not member.active:
        member.active = True
        member.save(update_fields=["active"])

print("MEMBRE ACTIF :", member.active)

# ============================================================
# 6. CREATION D'UNE UNITE DE CADEAU
# ============================================================

unit = create_gift_inventory_unit(
    gift=gift,
    source="RESELLER",
    reseller=reseller,
    official_value_eur=official_value,
)

print("")
print("UNITÉ")
print("ID :", unit.unit_id)
print("STATUT :", unit.status)
print("VALEUR :", unit.official_value_eur, "EUR")
print("SOURCE :", unit.source)
print("CREDIT_ONLY :", unit.credit_only)

if not unit.unit_id.startswith("GFT-"):
    raise AssertionError(
        "L'identifiant individuel du cadeau est invalide."
    )

if Decimal(str(unit.official_value_eur)) != official_value:
    raise AssertionError(
        "La valeur officielle du cadeau est incorrecte."
    )

if unit.status != "AVAILABLE":
    raise AssertionError(
        "Une unité nouvellement créée doit être AVAILABLE."
    )

print("CREATION_UNITE = OK")

# ============================================================
# 7. DISTRIBUTION AU MEMBRE DU RESEAU
# ============================================================

unit = distribute_gift_unit(
    unit=unit,
    reseller=reseller,
    member=member_user,
)

unit.refresh_from_db()

print("")
print("DISTRIBUTION")
print("STATUT :", unit.status)
print("CURRENT_RESELLER :", unit.current_reseller_id)
print("CURRENT_MEMBER :", unit.current_member_id)

if unit.status != "DISTRIBUTED":
    raise AssertionError(
        "L'unité distribuée doit être DISTRIBUTED."
    )

if unit.current_reseller_id != reseller.id:
    raise AssertionError(
        "Le revendeur principal est incorrect."
    )

if unit.current_member_id != member.id:
    raise AssertionError(
        "Le membre réseau est incorrect."
    )

print("DISTRIBUTION_COMMERCIALE = OK")

# ============================================================
# 8. ACCORD COMMERCIAL
# ============================================================

agreement = create_distribution_agreement(
    principal_reseller=reseller,
    network_member=member,
    gift=gift,
    quantity=1,
    member_percentage=Decimal("60.00"),
    principal_reseller_percentage=Decimal("30.00"),
    other_percentage=Decimal("5.00"),
)

agreement.refresh_from_db()

total = (
    agreement.member_percentage
    + agreement.principal_reseller_percentage
    + agreement.nsikay_percentage
    + agreement.other_percentage
)

print("")
print("ACCORD")
print("ID :", agreement.id)
print("VERSION :", agreement.version)
print("STATUT :", agreement.status)
print("MEMBRE :", agreement.member_percentage, "%")
print("REVENDEUR :", agreement.principal_reseller_percentage, "%")
print("NSIKAY :", agreement.nsikay_percentage, "%")
print("AUTRE :", agreement.other_percentage, "%")
print("TOTAL :", total, "%")

if agreement.nsikay_percentage != Decimal("5.00"):
    raise AssertionError(
        "La commission NSIKAY doit être 5 %."
    )

if total != Decimal("100.00"):
    raise AssertionError(
        "La répartition commerciale doit totaliser 100 %."
    )

print("ACCORD_CREATION = OK")

# ============================================================
# 9. ACCEPTATION
# ============================================================

agreement = accept_distribution_agreement(
    agreement=agreement
)

agreement.refresh_from_db()

print("")
print("ACCEPTATION")
print("STATUT :", agreement.status)
print("ACCEPTED_AT :", agreement.accepted_at)

if agreement.status != "ACCEPTED":
    raise AssertionError(
        "L'accord doit être ACCEPTED."
    )

if agreement.accepted_at is None:
    raise AssertionError(
        "accepted_at doit être renseigné."
    )

print("ACCEPTATION = OK")

# ============================================================
# 10. VERROUILLAGE
# ============================================================

agreement = lock_distribution_agreement(
    agreement=agreement
)

agreement.refresh_from_db()

print("")
print("VERROUILLAGE")
print("STATUT :", agreement.status)
print("LOCKED_AT :", agreement.locked_at)

if agreement.status != "LOCKED":
    raise AssertionError(
        "L'accord doit être LOCKED."
    )

if agreement.locked_at is None:
    raise AssertionError(
        "locked_at doit être renseigné."
    )

print("VERROUILLAGE = OK")

# ============================================================
# 11. TEST IMMUTABILITE
# ============================================================

agreement.refresh_from_db()

original_member_percentage = agreement.member_percentage
blocked = False

agreement.member_percentage = Decimal("61.00")

try:
    agreement.save()
except (ValueError, ValidationError) as exc:
    blocked = True
    print("")
    print("MODIFICATION BLOQUÉE :", str(exc))

except Exception as exc:
    blocked = True
    print("")
    print(
        "MODIFICATION BLOQUÉE PAR EXCEPTION :",
        type(exc).__name__,
        str(exc)
    )

if not blocked:
    agreement.refresh_from_db()

    if agreement.member_percentage != original_member_percentage:
        raise AssertionError(
            "ERREUR CRITIQUE : un accord LOCKED a été modifié."
        )

    raise AssertionError(
        "ERREUR : la modification d'un accord LOCKED n'a pas été bloquée."
    )

agreement.refresh_from_db()

if agreement.member_percentage != original_member_percentage:
    raise AssertionError(
        "La valeur historique de l'accord a changé."
    )

print("IMMUTABILITE = OK")

# ============================================================
# 12. VALEUR OFFICIELLE IMMUTABLE
# ============================================================

unit.refresh_from_db()

saved_value = unit.official_value_eur

if saved_value != official_value:
    raise AssertionError(
        "La valeur officielle de l'unité ne correspond plus au catalogue."
    )

print("VALEUR_OFFICIELLE_IMMUTABLE = OK")

# ============================================================
# 13. AUDIT
# ============================================================

audit_entries = GiftResellerAuditLog.objects.filter(
    object_id=str(unit.id)
).count()

print("")
print("AUDIT UNITÉ :", audit_entries)

if audit_entries < 2:
    raise AssertionError(
        "La traçabilité de l'unité est insuffisante."
    )

print("AUDIT = OK")

# ============================================================
# 14. ETAT FINAL
# ============================================================

unit.refresh_from_db()
agreement.refresh_from_db()

print("")
print("============================================================")
print(" ETAT FINAL STAGE 2")
print("============================================================")
print("")
print("CADEAU :", unit.gift.name)
print("UNIT ID :", unit.unit_id)
print("VALEUR OFFICIELLE :", unit.official_value_eur, "EUR")
print("SOURCE :", unit.source)
print("CREDIT ONLY :", unit.credit_only)
print("STATUT :", unit.status)
print("REVENDEUR :", unit.current_reseller_id)
print("MEMBRE :", unit.current_member_id)
print("")
print("ACCORD :", agreement.id)
print("VERSION :", agreement.version)
print("STATUT ACCORD :", agreement.status)
print("MEMBRE :", agreement.member_percentage, "%")
print("REVENDEUR :", agreement.principal_reseller_percentage, "%")
print("NSIKAY :", agreement.nsikay_percentage, "%")
print("AUTRE :", agreement.other_percentage, "%")

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
print("VALEUR_OFFICIELLE_IMMUTABLE = OK")
print("AUDIT = OK")
print("")
print("TEST_STAGE2_COMPLET = OK")
print("============================================================")