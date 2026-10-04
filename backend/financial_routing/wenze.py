from decimal import Decimal

from financial_routing.services import (
    calculate_fee,
    resolve_financial_route,
    route_financial_operation,
)


WENZE_FEE_TYPE = "WENZE"
WENZE_SOURCE_TYPE = "WENZE"
WENZE_OPERATION_TYPE = "REVENUE"


def prepare_wenze_revenue(
    amount,
    country_code="",
    currency_code="",
):
    """
    Prépare financièrement une recette WENZE.

    Règles :
    - WENZE = 0 % de commission commerciale ;
    - le routage dépend du pays/devise ;
    - aucune transaction réelle n'est créée ;
    - aucun portefeuille n'est modifié ;
    - aucun partenaire n'est débité/crédité.

    Cette fonction constitue le point central qui pourra être
    appelé par le processus de validation d'une commande WENZE.
    """

    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError(
            "Le montant WENZE doit être strictement positif."
        )

    fee = calculate_fee(
        amount=amount,
        fee_type=WENZE_FEE_TYPE,
    )

    route = resolve_financial_route(
        source_type=WENZE_SOURCE_TYPE,
        country_code=country_code,
        currency_code=currency_code,
        operation_type=WENZE_OPERATION_TYPE,
    )

    route_data = None

    if route:
        route_data = {
            "rule_id": route.id,
            "source_type": route.source_type,
            "source_name": route.source_name,
            "operation_type": route.operation_type,
            "partner_type": route.partner_type,
            "partner_name": route.partner_name,
            "bank_name": route.bank_name,
            "bank_country": route.bank_country,
            "bank_account_reference": route.bank_account_reference,
            "destination_label": route.destination_label,
            "country_code": route.country_code,
            "currency_code": route.currency_code,
            "status": route.status,
        }

    return {
        "module": "WENZE",
        "amount": fee["amount"],
        "fee_type": fee["fee_type"],
        "fee_percentage": fee["percentage"],
        "fee_amount": fee["fee_amount"],
        "net_amount": fee["net_amount"],
        "route_found": bool(route),
        "route": route_data,
        "transaction_created": False,
        "balance_modified": False,
        "simulation": True,
    }


def simulate_wenze_revenue(
    amount,
    country_code="",
    currency_code="",
):
    """
    Simulation complète du routage d'une recette WENZE.
    Aucune opération financière réelle.
    """

    return route_financial_operation(
        amount=amount,
        fee_type=WENZE_FEE_TYPE,
        source_type=WENZE_SOURCE_TYPE,
        country_code=country_code,
        currency_code=currency_code,
        operation_type=WENZE_OPERATION_TYPE,
    )
