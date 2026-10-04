from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q
from django.utils import timezone

from .models import FinancialRoutingRule, FinancialFeeRule


MONEY_QUANTUM = Decimal("0.01")


def money(value):
    """
    Normalise un montant monétaire à deux décimales.
    """
    return Decimal(str(value)).quantize(
        MONEY_QUANTUM,
        rounding=ROUND_HALF_UP,
    )


def get_fee_rule(fee_type):
    """
    Retourne uniquement une règle de frais active.
    """
    return FinancialFeeRule.objects.filter(
        fee_type=fee_type,
        active=True,
    ).first()


def calculate_fee(amount, fee_type):
    """
    Calcule les frais NSIKAY sans créer de transaction.

    Retourne :
        amount
        fee_type
        percentage
        fee_amount
        net_amount
    """
    amount = money(amount)

    rule = get_fee_rule(fee_type)

    if not rule:
        raise ValueError(
            f"Aucune règle de frais active pour {fee_type}."
        )

    percentage = Decimal(str(rule.percentage))

    fee_amount = money(
        amount * percentage / Decimal("100")
    )

    net_amount = money(
        amount - fee_amount
    )

    return {
        "amount": amount,
        "fee_type": fee_type,
        "percentage": percentage,
        "fee_amount": fee_amount,
        "net_amount": net_amount,
    }


def resolve_financial_route(
    source_type,
    country_code="",
    currency_code="",
    operation_type="REVENUE",
):
    """
    Recherche la règle de routage APPROVED la plus précise.

    Priorité :
        1. pays + devise
        2. pays seul
        3. international + devise
        4. international général
    """

    now = timezone.now()

    country_code = (country_code or "").upper().strip()
    currency_code = (currency_code or "").upper().strip()

    queryset = FinancialRoutingRule.objects.filter(
        source_type=source_type,
        operation_type=operation_type,
        active=True,
        status="APPROVED",
    ).filter(
        Q(valid_from__isnull=True) | Q(valid_from__lte=now),
        Q(valid_until__isnull=True) | Q(valid_until__gte=now),
    )

    candidates = list(queryset)

    def score(rule):
        rule_country = (rule.country_code or "").upper().strip()
        rule_currency = (rule.currency_code or "").upper().strip()

        if (
            country_code
            and currency_code
            and rule_country == country_code
            and rule_currency == currency_code
        ):
            return 400 - rule.priority

        if (
            country_code
            and rule_country == country_code
            and not rule_currency
        ):
            return 300 - rule.priority

        if (
            currency_code
            and not rule_country
            and rule_currency == currency_code
        ):
            return 200 - rule.priority

        if not rule_country and not rule_currency:
            return 100 - rule.priority

        return -1000 - rule.priority

    candidates.sort(key=score, reverse=True)

    return candidates[0] if candidates else None


def route_financial_operation(
    amount,
    fee_type,
    source_type,
    country_code="",
    currency_code="",
    operation_type="REVENUE",
):
    """
    Simulation complète d'une opération financière NSIKAY.

    IMPORTANT :
    - aucune transaction n'est créée ;
    - aucun portefeuille n'est modifié ;
    - aucun compte bancaire n'est débité/crédité ;
    - aucun partenaire n'est créé.

    Cette fonction prépare uniquement le résultat
    qui pourra ensuite être branché sur les vraies opérations.
    """

    fee_result = calculate_fee(
        amount=amount,
        fee_type=fee_type,
    )

    rule = resolve_financial_route(
        source_type=source_type,
        country_code=country_code,
        currency_code=currency_code,
        operation_type=operation_type,
    )

    route = None

    if rule:
        route = {
            "rule_id": rule.id,
            "source_type": rule.source_type,
            "source_name": rule.source_name,
            "operation_type": rule.operation_type,
            "partner_type": rule.partner_type,
            "partner_name": rule.partner_name,
            "bank_name": rule.bank_name,
            "bank_country": rule.bank_country,
            "bank_account_reference": rule.bank_account_reference,
            "destination_label": rule.destination_label,
            "country_code": rule.country_code,
            "currency_code": rule.currency_code,
            "status": rule.status,
        }

    return {
        "simulation": True,
        "transaction_created": False,
        "balance_modified": False,
        "amount": fee_result["amount"],
        "fee_type": fee_result["fee_type"],
        "fee_percentage": fee_result["percentage"],
        "fee_amount": fee_result["fee_amount"],
        "net_amount": fee_result["net_amount"],
        "route_found": bool(route),
        "route": route,
    }


def get_official_fee_rates():
    """
    Retourne les taux financiers NSIKAY actuellement actifs.
    """
    fee_types = [
        FinancialFeeRule.TRANSFER_INTERNAL,
        FinancialFeeRule.TRANSFER_MOBILE_MONEY,
        FinancialFeeRule.TRANSFER_VISA,
        FinancialFeeRule.WITHDRAWAL,
        FinancialFeeRule.WENZE,
    ]

    result = {}

    for fee_type in fee_types:
        rule = get_fee_rule(fee_type)

        result[fee_type] = (
            Decimal(str(rule.percentage))
            if rule
            else None
        )

    return result

# ============================================================
# ADMINISTRATION DU ROUTAGE FINANCIER
# ============================================================

def approve_routing_rule(rule, user=None):
    """
    Approuve une règle de routage financier.

    Aucun mouvement financier n'est exécuté.
    """
    rule.status = "APPROVED"

    if user is not None:
        rule.approved_by = user

    rule.active = True
    rule.save(
        update_fields=[
            "status",
            "approved_by",
            "active",
            "updated_at",
        ]
    )

    return rule


def suspend_routing_rule(rule):
    """
    Suspend une règle de routage financier.

    La règle reste enregistrée mais ne peut plus
    être sélectionnée par le moteur.
    """
    rule.status = "SUSPENDED"
    rule.active = False

    rule.save(
        update_fields=[
            "status",
            "active",
            "updated_at",
        ]
    )

    return rule


def activate_routing_rule(rule):
    """
    Réactive une règle existante.

    La règle devient active mais reste soumise
    à son statut administratif.
    """
    rule.active = True

    rule.save(
        update_fields=[
            "active",
            "updated_at",
        ]
    )

    return rule


def deactivate_routing_rule(rule):
    """
    Désactive une règle sans supprimer son historique.
    """
    rule.active = False

    rule.save(
        update_fields=[
            "active",
            "updated_at",
        ]
    )

    return rule
