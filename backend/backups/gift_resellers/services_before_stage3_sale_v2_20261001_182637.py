from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import (
    GiftResellerAuditLog,
    ResellerSale,
    SaleAllocation,
)


MONEY = Decimal("0.01")


def money(value):
    return Decimal(value).quantize(MONEY, rounding=ROUND_HALF_UP)


def calculate_reseller_sale_split(
    retail_amount,
    retail_currency,
    official_value_eur,
    member_percentage,
    principal_reseller_percentage,
    other_percentage=Decimal("0.000"),
    nsikay_percentage=Decimal("5.000"),
):
    """
    NSIKAY = 5 % de la valeur officielle initiale EUR.
    Les parts commerciales sont calculées sur le prix retail.
    """

    retail_amount = money(retail_amount)
    official_value_eur = money(official_value_eur)

    if retail_amount <= 0:
        raise ValidationError("Le prix de vente doit etre positif.")

    if official_value_eur <= 0:
        raise ValidationError("La valeur officielle doit etre positive.")

    if nsikay_percentage != Decimal("5.000"):
        raise ValidationError(
            "La commission revendeur NSIKAY doit rester a 5 %."
        )

    member_amount = money(
        retail_amount * Decimal(member_percentage) / Decimal("100")
    )

    principal_amount = money(
        retail_amount
        * Decimal(principal_reseller_percentage)
        / Decimal("100")
    )

    other_amount = money(
        retail_amount * Decimal(other_percentage) / Decimal("100")
    )

    # IMPORTANT :
    # NSIKAY est calculé sur la valeur officielle EUR,
    # et non sur le prix retail.
    nsikay_amount = money(
        official_value_eur
        * Decimal(nsikay_percentage)
        / Decimal("100")
    )

    total = member_amount + principal_amount + other_amount + nsikay_amount

    if total > retail_amount:
        raise ValidationError(
            "La repartition depasse le montant effectivement paye par le client."
        )

    return {
        "retail_amount": retail_amount,
        "official_value_eur": official_value_eur,
        "nsikay_base_eur": official_value_eur,
        "member_amount": member_amount,
        "principal_reseller_amount": principal_amount,
        "other_amount": other_amount,
        "nsikay_amount_eur": nsikay_amount,
        "unallocated_amount": money(retail_amount - total),
        "currency": retail_currency.upper(),
    }


@transaction.atomic
def create_sale_allocation(
    *,
    sale,
    split,
):
    """
    Crée les lignes financières immuables de la vente.
    Aucun paiement n'est débité ici.
    Le branchement au moyen de paiement sera effectué après validation.
    """

    if not sale.agreement_id:
        raise ValidationError("La vente doit avoir un accord.")

    agreement = sale.agreement

    if agreement.status != "LOCKED":
        raise ValidationError(
            "Une vente ne peut utiliser qu'un accord commercial verrouille."
        )

    if SaleAllocation.objects.filter(sale=sale).exists():
        raise ValidationError(
            "Cette vente possede deja une repartition."
        )

    rows = [
        (
            "MEMBER",
            agreement.member_percentage,
            split["retail_amount"],
            split["member_amount"],
        ),
        (
            "PRINCIPAL_RESELLER",
            agreement.principal_reseller_percentage,
            split["retail_amount"],
            split["principal_reseller_amount"],
        ),
        (
            "NSIKAY",
            Decimal("5.000"),
            split["nsikay_base_eur"],
            split["nsikay_amount_eur"],
        ),
        (
            "OTHER",
            agreement.other_percentage,
            split["retail_amount"],
            split["other_amount"],
        ),
    ]

    for allocation_type, percentage, base_amount, amount in rows:
        if amount <= 0:
            continue

        SaleAllocation.objects.create(
            sale=sale,
            allocation_type=allocation_type,
            percentage=percentage,
            base_amount=base_amount,
            amount=amount,
            currency=split["currency"],
            reference=f"{sale.reference}-{allocation_type}",
        )

    sale.member_amount = split["member_amount"]
    sale.principal_reseller_amount = split["principal_reseller_amount"]
    sale.other_amount = split["other_amount"]
    sale.nsikay_base_eur = split["nsikay_base_eur"]
    sale.nsikay_amount_eur = split["nsikay_amount_eur"]
    sale.status = "SETTLED"
    sale.settled_at = timezone.now()
    sale.save(
        update_fields=[
            "member_amount",
            "principal_reseller_amount",
            "other_amount",
            "nsikay_base_eur",
            "nsikay_amount_eur",
            "status",
            "settled_at",
        ]
    )

    GiftResellerAuditLog.objects.create(
        action="ALLOCATED",
        actor=None,
        reference=sale.reference,
        details={
            "retail_amount": str(split["retail_amount"]),
            "retail_currency": split["currency"],
            "official_value_eur": str(split["official_value_eur"]),
            "nsikay_base_eur": str(split["nsikay_base_eur"]),
            "nsikay_amount_eur": str(split["nsikay_amount_eur"]),
            "member_amount": str(split["member_amount"]),
            "principal_reseller_amount": str(
                split["principal_reseller_amount"]
            ),
            "other_amount": str(split["other_amount"]),
        },
    )

    return sale

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
        status="AVAILABLE",
    )

    unit.full_clean()
    unit.save()

    GiftResellerAuditLog.objects.create(
        action="CREATED",
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

    if locked_unit.status != "AVAILABLE":
        raise ValidationError(
            f"Le cadeau {locked_unit.unit_id} n'est pas disponible."
        )

    if locked_unit.current_reseller_id != reseller.pk:
        raise ValidationError(
            "Le cadeau ne se trouve pas dans le stock du revendeur."
        )

    # Le membre peut être transmis directement comme NetworkMember.
    # Cela permet de sélectionner précisément le réseau voulu lorsqu'un
    # même utilisateur appartient à plusieurs réseaux du même revendeur.
    if isinstance(member, NetworkMember):
        membership = (
            NetworkMember.objects
            .select_related("network")
            .filter(
                pk=member.pk,
                network__principal_reseller=reseller,
                active=True,
            )
            .first()
        )
    else:
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
    locked_unit.status = "DISTRIBUTED"

    locked_unit.full_clean()
    locked_unit.save(
        update_fields=[
            "current_member",
            "status",
            "updated_at",
        ]
    )

    GiftResellerAuditLog.objects.create(
        action="DISTRIBUTED",
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
        effective_from=effective_from or timezone.now(),
        effective_until=effective_until,
        status="DRAFT",
        version=version,
        previous_agreement=previous,
    )

    agreement.full_clean()
    agreement.save()

    GiftResellerAuditLog.objects.create(
        action="CREATED",
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
        "DRAFT",
        "PENDING_ACCEPTANCE",
    )

    if agreement.status not in allowed:
        raise ValidationError(
            "Cet accord ne peut plus être accepté."
        )

    agreement.status = (
        "ACCEPTED"
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
        action="AGREEMENT_ACCEPTED",
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

    if agreement.status == "LOCKED":
        return agreement

    if agreement.status != "ACCEPTED":
        raise ValidationError(
            "Seul un accord ACCEPTED peut être verrouillé."
        )

    agreement.status = (
        "LOCKED"
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
        action="AGREEMENT_LOCKED",
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

