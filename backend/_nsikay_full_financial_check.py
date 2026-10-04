import os
import inspect
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsikay.settings")

import django
django.setup()

from django.db import connection

from financial_routing.models import (
    FinancialFeeRule,
    FinancialRoutingRule,
    FinancialRoutingLog,
    FinancialPartner,
)

from financial_routing.services import (
    calculate_fee,
    get_official_fee_rates,
    resolve_financial_route,
    route_financial_operation,
)

from transactions.services import calculate_fees

from finance import fees as finance_fees
from finance import ledger as finance_ledger

from finance.models import MarketplaceCommission


print("")
print("------------------------------------------------------------")
print("A. VERIFICATION DES REGLES FINANCIERES EN BASE")
print("------------------------------------------------------------")

expected = {
    "TRANSFER_INTERNAL": Decimal("0.500"),
    "TRANSFER_EXTERNAL": Decimal("0.850"),
    "TRANSFER_MOBILE_MONEY": Decimal("0.850"),
    "TRANSFER_VISA": Decimal("0.850"),
    "WITHDRAWAL": Decimal("1.200"),
    "WENZE": Decimal("0.000"),
}

rules = {
    r.fee_type: r
    for r in FinancialFeeRule.objects.all()
}

if len(rules) != 6:
    raise RuntimeError(
        f"Nombre inattendu de règles financières : {len(rules)} au lieu de 6."
    )

for fee_type, expected_rate in expected.items():
    if fee_type not in rules:
        raise RuntimeError(f"Règle absente : {fee_type}")

    rule = rules[fee_type]

    if rule.percentage != expected_rate:
        raise RuntimeError(
            f"{fee_type}: taux {rule.percentage} au lieu de {expected_rate}"
        )

    if not rule.active:
        raise RuntimeError(
            f"{fee_type}: la règle existe mais n'est pas active."
        )

    print(
        f"OK | {fee_type:<25} "
        f"{rule.percentage}% | active={rule.active}"
    )

print("")
print("REGLES EN BASE : OK")


print("")
print("------------------------------------------------------------")
print("B. VERIFICATION DU MOTEUR CENTRAL")
print("------------------------------------------------------------")

central_tests = [
    ("TRANSFER_INTERNAL", Decimal("1000"), Decimal("5.00"), Decimal("995.00")),
    ("TRANSFER_EXTERNAL", Decimal("1000"), Decimal("8.50"), Decimal("991.50")),
    ("TRANSFER_MOBILE_MONEY", Decimal("1000"), Decimal("8.50"), Decimal("991.50")),
    ("TRANSFER_VISA", Decimal("1000"), Decimal("8.50"), Decimal("991.50")),
    ("WITHDRAWAL", Decimal("1000"), Decimal("12.00"), Decimal("988.00")),
    ("WENZE", Decimal("1000"), Decimal("0.00"), Decimal("1000.00")),
]

for fee_type, amount, expected_fee, expected_net in central_tests:
    result = calculate_fee(amount, fee_type)

    if not isinstance(result, dict):
        raise RuntimeError(
            f"{fee_type}: format inattendu {type(result)}"
        )

    required_keys = {
        "amount",
        "fee_type",
        "percentage",
        "fee_amount",
        "net_amount",
    }

    if not required_keys.issubset(result.keys()):
        raise RuntimeError(
            f"{fee_type}: clés manquantes dans le retour : "
            f"{required_keys - set(result.keys())}"
        )

    if result["fee_amount"] != expected_fee:
        raise RuntimeError(
            f"{fee_type}: frais {result['fee_amount']} "
            f"au lieu de {expected_fee}"
        )

    if result["net_amount"] != expected_net:
        raise RuntimeError(
            f"{fee_type}: net {result['net_amount']} "
            f"au lieu de {expected_net}"
        )

    print(
        f"OK | {fee_type:<25} "
        f"taux={result['percentage']}% | "
        f"frais={result['fee_amount']} | "
        f"net={result['net_amount']}"
    )

print("")
print("MOTEUR CENTRAL : OK")


print("")
print("------------------------------------------------------------")
print("C. VERIFICATION transactions/services.py")
print("------------------------------------------------------------")

transaction_tests = [
    ("transfer", Decimal("1000"), Decimal("5.00"), Decimal("995.00")),
    ("withdrawal", Decimal("1000"), Decimal("12.00"), Decimal("988.00")),
]

for operation, amount, expected_fee, expected_net in transaction_tests:
    result = calculate_fees(amount, operation)

    if not isinstance(result, dict):
        raise RuntimeError(
            f"{operation}: résultat inattendu {type(result)}"
        )

    if result["fee_amount"] != expected_fee:
        raise RuntimeError(
            f"{operation}: frais {result['fee_amount']} "
            f"au lieu de {expected_fee}"
        )

    if result["net_amount"] != expected_net:
        raise RuntimeError(
            f"{operation}: net {result['net_amount']} "
            f"au lieu de {expected_net}"
        )

    print(
        f"OK | {operation:<12} "
        f"frais={result['fee_amount']} | "
        f"net={result['net_amount']}"
    )

print("")
print("TRANSACTIONS SERVICES : OK")


print("")
print("------------------------------------------------------------")
print("D. VERIFICATION finance/fees.py")
print("------------------------------------------------------------")

finance_fee_tests = [
    ("platform_commission", finance_fees.calculate_platform_commission, Decimal("5.00")),
    ("transfer_fee", finance_fees.calculate_transfer_fee, Decimal("5.00")),
    ("withdraw_cost", finance_fees.calculate_withdraw_cost, Decimal("12.00")),
    ("withdrawal_fee", finance_fees.calculate_withdrawal_fee, Decimal("12.00")),
    ("mobile_money", finance_fees.calculate_mobile_money_fee, Decimal("8.50")),
    ("visa", finance_fees.calculate_visa_fee, Decimal("8.50")),
    ("wenze", finance_fees.calculate_wenze_fee, Decimal("0.00")),
]

for name, function, expected_fee in finance_fee_tests:
    result = function(Decimal("1000"))

    if result != expected_fee:
        raise RuntimeError(
            f"{name}: {result} au lieu de {expected_fee}"
        )

    print(
        f"OK | {name:<20} {result}"
    )

print("")
print("FINANCE FEES : OK")


print("")
print("------------------------------------------------------------")
print("E. VERIFICATION finance/ledger.py")
print("------------------------------------------------------------")

ledger_tests = [
    ("transfer", finance_ledger.calculate_transfer_fee, Decimal("5.00")),
    ("withdrawal", finance_ledger.calculate_withdrawal_fee, Decimal("12.00")),
    ("mobile_money", finance_ledger.calculate_mobile_money_fee, Decimal("8.50")),
    ("visa", finance_ledger.calculate_visa_fee, Decimal("8.50")),
    ("wenze", finance_ledger.calculate_wenze_fee, Decimal("0.00")),
]

for name, function, expected_fee in ledger_tests:
    result = function(Decimal("1000"))

    if result != expected_fee:
        raise RuntimeError(
            f"{name}: {result} au lieu de {expected_fee}"
        )

    print(
        f"OK | {name:<20} {result}"
    )

print("")
print("FINANCE LEDGER : OK")


print("")
print("------------------------------------------------------------")
print("F. VERIFICATION WENZE = 0 %")
print("------------------------------------------------------------")

marketplace_field = MarketplaceCommission._meta.get_field("rate")
default_rate = marketplace_field.default

if callable(default_rate):
    default_rate = default_rate()

default_rate = Decimal(str(default_rate))

print(
    f"MarketplaceCommission.rate default = {default_rate}"
)

if default_rate != Decimal("0.0000"):
    raise RuntimeError(
        f"MarketplaceCommission.rate n'est pas à 0 : {default_rate}"
    )

wenze = calculate_fee(Decimal("5000"), "WENZE")

if wenze["fee_amount"] != Decimal("0.00"):
    raise RuntimeError(
        f"WENZE: frais inattendus {wenze['fee_amount']}"
    )

print("OK | WENZE 5000.00 | frais=0.00 | net=5000.00")
print("WENZE : OK")


print("")
print("------------------------------------------------------------")
print("G. VERIFICATION DES TAUX OFFICIELS EXPOSES PAR LE SERVICE")
print("------------------------------------------------------------")

official_rates = get_official_fee_rates()

print("Retour officiel :")

for key, value in official_rates.items():
    print(f"  {key} = {value}")

print("")
print("TAUX OFFICIELS : SERVICE ACCESSIBLE")


print("")
print("------------------------------------------------------------")
print("H. VERIFICATION DU ROUTAGE FINANCIER")
print("------------------------------------------------------------")

print("")
print("Nombre actuel de règles de routage :",
      FinancialRoutingRule.objects.count())

print("Nombre actuel de logs de routage :",
      FinancialRoutingLog.objects.count())

print("Nombre actuel de partenaires financiers :",
      FinancialPartner.objects.count())

print("")

route_signature = inspect.signature(resolve_financial_route)
operation_signature = inspect.signature(route_financial_operation)

print("Signature resolve_financial_route :")
print(route_signature)

print("")
print("Signature route_financial_operation :")
print(operation_signature)

print("")
print("Routage financier : API accessible")


print("")
print("------------------------------------------------------------")
print("I. VERIFICATION DES DONNEES FINANCIERES DE REFERENCE")
print("------------------------------------------------------------")

print("Tables financières détectées :")

financial_tables = [
    "financial_routing_financialfeerule",
    "financial_routing_financialroutingrule",
    "financial_routing_financialroutinglog",
    "financial_routing_financialpartner",
]

existing_tables = set(connection.introspection.table_names())

for table in financial_tables:
    status = "EXISTE" if table in existing_tables else "ABSENTE"
    print(f"  {table:<50} {status}")

print("")
print("STRUCTURE FINANCIERE : ACCESSIBLE")


print("")
print("------------------------------------------------------------")
print("J. VERIFICATION ABSENCE DE DONNEES CREEES PAR LE TEST")
print("------------------------------------------------------------")

print("FinancialFeeRule :", FinancialFeeRule.objects.count())
print("FinancialRoutingRule :", FinancialRoutingRule.objects.count())
print("FinancialRoutingLog :", FinancialRoutingLog.objects.count())
print("FinancialPartner :", FinancialPartner.objects.count())

print("")
print("Aucun objet de test n'a été créé par ce script.")


print("")
print("============================================================")
print(" TEST FINANCIER COMPLET : REUSSI")
print("============================================================")
print("")
print("MOTEUR CENTRAL              : OK")
print("TRANSACTIONS                : OK")
print("FINANCE FEES                : OK")
print("FINANCE LEDGER              : OK")
print("WENZE                       : OK")
print("REGLES EN BASE              : OK")
print("ROUTAGE FINANCIER           : ACCESSIBLE")
print("DJANGO                      : OK")
print("")
print("MODE TEST : AUCUN MOUVEMENT FINANCIER REEL")
print("")
