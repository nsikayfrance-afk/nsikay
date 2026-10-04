from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "gift_resellers" / "services.py"

text = SERVICES.read_text(encoding="utf-8")

if "def create_gift_inventory_unit" in text:
    print("SERVICES_STAGE2_DEJA_PRESENTS=OUI")
else:

    addition = r'''

# ============================================================
# NSIKAY - SERVICES REVENDEURS CADEAUX / ETAPE 2
# ============================================================

import uuid
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone


def _generate_gift_unit_id():
    """
    Identifiant individuel permanent du cadeau.
    """
    return "GFT-" + uuid.uuid4().hex.upper()


@transaction.atomic
def create_gift_inventory_unit(
    *,
    gift,
    source,
    reseller=None,
    member=None,
    credit_only=False,
    official_value_eur=None,
    actor=None,
):
    """
    Crée une unité individuelle de cadeau.

    Aucun paiement réel n'est exécuté.
    """

    from .models import GiftInventoryUnit, GiftResellerAuditLog

    if credit_only and source != GiftInventoryUnit.Source.CREDIT:
        raise ValidationError(
            "Un cadeau CREDIT doit avoir la source CREDIT."
        )

    value = (
        official_value_eur
        if official_value_eur is not None
        else gift.reference_value_eur
    )

    unit_id = _generate_gift_unit_id()

    while GiftInventoryUnit.objects.filter(unit_id=unit_id).exists():
        unit_id = _generate_gift_unit_id()

    unit = GiftInventoryUnit(
        unit_id=unit_id,
        gift=gift,
        official_value_eur=money(value),
        currency_reference="EUR",
        current_reseller=reseller,
        current_member=member,
        source=source,
        credit_only=credit_only,
        status=GiftInventoryUnit.Status.AVAILABLE,
    )

    unit.full_clean()
    unit.save()

    GiftResellerAuditLog.objects.create(
        action=GiftResellerAuditLog.Action.CREATED,
        actor=actor,
        reference=unit.unit_id,
        details={
            "gift_id": gift.pk,
            "gift_name": gift.name,
            "official_value_eur": str(unit.official_value_eur),
            "source": unit.source,
            "credit_only": unit.credit_only,
        },
    )

    return unit


@transaction.atomic
def distribute_gift_unit(
    *,
    unit,
    reseller,
    member,
    actor=None,
):
    """
    Transfère une unité du stock du revendeur vers un membre
    du réseau pour vente.

    Ce n'est PAS un don.
    Aucun mouvement financier n'est réalisé.
    """

    from .models import (
        GiftInventoryUnit,
        NetworkMember,
        GiftResellerAuditLog,
    )

    locked_unit = (
        GiftInventoryUnit.objects
        .select_for_update()
        .get(pk=unit.pk)
    )

    if locked_unit.status != GiftInventoryUnit.Status.AVAILABLE:
        raise ValidationError(
            f"Le cadeau {locked_unit.unit_id} n'est pas disponible."
        )

    if locked_unit.current_reseller_id != reseller.pk:
        raise ValidationError(
            "Le cadeau ne se trouve pas dans le stock du revendeur."
        )

    membership = (
        NetworkMember.objects
        .filter(
            network__principal_reseller=reseller,
            user=member,
            active=True,
        )
        .select_related("network")
        .first()
    )

    if membership is None:
        raise ValidationError(
            "Le membre n'appartient pas à un réseau actif "
            "de ce revendeur."
        )

    locked_unit.current_member = membership
    locked_unit.status = GiftInventoryUnit.Status.DISTRIBUTED

    locked_unit.full_clean()
    locked_unit.save(
        update_fields=[
            "current_member",
            "status",
            "updated_at",
        ]
    )

    GiftResellerAuditLog.objects.create(
        action=GiftResellerAuditLog.Action.DISTRIBUTED,
        actor=actor,
        reference=locked_unit.unit_id,
        details={
            "reseller_id": reseller.pk,
            "member_id": member.pk,
            "network_id": membership.network_id,
            "gift_id": locked_unit.gift_id,
            "official_value_eur": str(
                locked_unit.official_value_eur
            ),
            "credit_only": locked_unit.credit_only,
            "commercial_purpose": True,
        },
    )

    return locked_unit


@transaction.atomic
def create_distribution_agreement(
    *,
    principal_reseller,
    network_member,
    gift,
    quantity,
    member_percentage,
    principal_reseller_percentage,
    other_percentage=0,
    effective_from=None,
    effective_until=None,
    actor=None,
):
    """
    Crée une nouvelle version d'accord commercial.

    NSIKAY reste obligatoirement à 5 % de la valeur officielle EUR.
    """

    from .models import DistributionAgreement, GiftResellerAuditLog

    if quantity <= 0:
        raise ValidationError(
            "La quantité doit être supérieure à zéro."
        )

    member_percentage = money(member_percentage)
    principal_reseller_percentage = money(
        principal_reseller_percentage
    )
    other_percentage = money(other_percentage)
    nsikay_percentage = money("5.00")

    if (
        member_percentage < 0
        or principal_reseller_percentage < 0
        or other_percentage < 0
    ):
        raise ValidationError(
            "Les pourcentages ne peuvent pas être négatifs."
        )

    total = (
        member_percentage
        + principal_reseller_percentage
        + other_percentage
        + nsikay_percentage
    )

    if total > 100:
        raise ValidationError(
            "La somme des répartitions dépasse 100 %."
        )

    previous = (
        DistributionAgreement.objects
        .filter(
            principal_reseller=principal_reseller,
            network_member=network_member,
            gift=gift,
        )
        .order_by("-version")
        .first()
    )

    version = (
        previous.version + 1
        if previous is not None
        else 1
    )

    agreement = DistributionAgreement(
        principal_reseller=principal_reseller,
        network_member=network_member,
        gift=gift,
        quantity=quantity,
        official_value_eur=money(gift.reference_value_eur),
        member_percentage=member_percentage,
        principal_reseller_percentage=principal_reseller_percentage,
        nsikay_percentage=nsikay_percentage,
        other_percentage=other_percentage,
        effective_from=effective_from,
        effective_until=effective_until,
        status=DistributionAgreement.Status.DRAFT,
        version=version,
        previous_agreement=previous,
    )

    agreement.full_clean()
    agreement.save()

    GiftResellerAuditLog.objects.create(
        action=GiftResellerAuditLog.Action.CREATED,
        actor=actor,
        reference=f"AGR-{agreement.pk}-V{agreement.version}",
        details={
            "agreement_id": agreement.pk,
            "version": agreement.version,
            "previous_agreement_id": (
                previous.pk if previous else None
            ),
            "official_value_eur": str(
                agreement.official_value_eur
            ),
            "member_percentage": str(
                agreement.member_percentage
            ),
            "principal_reseller_percentage": str(
                agreement.principal_reseller_percentage
            ),
            "nsikay_percentage": str(
                agreement.nsikay_percentage
            ),
            "other_percentage": str(
                agreement.other_percentage
            ),
        },
    )

    return agreement


@transaction.atomic
def accept_distribution_agreement(
    *,
    agreement,
    actor=None,
):
    """
    Passe un accord DRAFT/PENDING_ACCEPTANCE à ACCEPTED.
    """

    from .models import (
        DistributionAgreement,
        GiftResellerAuditLog,
    )

    agreement = (
        DistributionAgreement.objects
        .select_for_update()
        .get(pk=agreement.pk)
    )

    allowed = (
        DistributionAgreement.Status.DRAFT,
        DistributionAgreement.Status.PENDING_ACCEPTANCE,
    )

    if agreement.status not in allowed:
        raise ValidationError(
            "Cet accord ne peut plus être accepté."
        )

    agreement.status = (
        DistributionAgreement.Status.ACCEPTED
    )
    agreement.accepted_at = timezone.now()

    agreement.full_clean()
    agreement.save(
        update_fields=[
            "status",
            "accepted_at",
        ]
    )

    GiftResellerAuditLog.objects.create(
        action=GiftResellerAuditLog.Action.AGREEMENT_ACCEPTED,
        actor=actor,
        reference=f"AGR-{agreement.pk}-V{agreement.version}",
        details={
            "agreement_id": agreement.pk,
            "version": agreement.version,
        },
    )

    return agreement


@transaction.atomic
def lock_distribution_agreement(
    *,
    agreement,
    actor=None,
):
    """
    Verrouille définitivement un accord ACCEPTED.

    Après LOCKED, les conditions commerciales ne doivent
    plus être modifiées. Une nouvelle version doit être créée.
    """

    from .models import (
        DistributionAgreement,
        GiftResellerAuditLog,
    )

    agreement = (
        DistributionAgreement.objects
        .select_for_update()
        .get(pk=agreement.pk)
    )

    if agreement.status == DistributionAgreement.Status.LOCKED:
        return agreement

    if agreement.status != DistributionAgreement.Status.ACCEPTED:
        raise ValidationError(
            "Seul un accord ACCEPTED peut être verrouillé."
        )

    agreement.status = (
        DistributionAgreement.Status.LOCKED
    )
    agreement.locked_at = timezone.now()

    agreement.full_clean()
    agreement.save(
        update_fields=[
            "status",
            "locked_at",
        ]
    )

    GiftResellerAuditLog.objects.create(
        action=GiftResellerAuditLog.Action.AGREEMENT_LOCKED,
        actor=actor,
        reference=f"AGR-{agreement.pk}-V{agreement.version}",
        details={
            "agreement_id": agreement.pk,
            "version": agreement.version,
            "principal_reseller_id": (
                agreement.principal_reseller_id
            ),
            "network_member_id": (
                agreement.network_member_id
            ),
            "gift_id": agreement.gift_id,
            "quantity": agreement.quantity,
            "official_value_eur": str(
                agreement.official_value_eur
            ),
            "member_percentage": str(
                agreement.member_percentage
            ),
            "principal_reseller_percentage": str(
                agreement.principal_reseller_percentage
            ),
            "nsikay_percentage": str(
                agreement.nsikay_percentage
            ),
            "other_percentage": str(
                agreement.other_percentage
            ),
        },
    )

    return agreement
'''

    text = text.rstrip() + addition + "\n"
    SERVICES.write_text(text, encoding="utf-8")
    print("SERVICES_STAGE2_AJOUTES=OK")
