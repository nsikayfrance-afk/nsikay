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