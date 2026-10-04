from decimal import Decimal

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from finance.models import (
    Currency,
    ExchangeRate,
    PlatformCommission,
    FeeConfiguration,
    FinancialControlReport,
    FinancialAuditLog,
    FinancialComplianceLog,
    FraudDetectionAlert,
    ComplianceReport,
)

from financial_routing.models import (
    FinancialRoutingRule,
    FinancialRoutingLog,
)
from banking.models import (
    Bank,
    BankAccount,
    BankingOperation,
    BankCountry,
    BankCurrency,
    BankService,
    BankCredit,
    BankInsurance,
    BankReport,
    BankTransaction,
    BankBalance,
    PartnerApproval,
)

from partner_finance.models import (
    PartnerApplication,
    PartnerCertification,
    PartnerSupply,
    PartnerWallet,
    PartnerDeposit,
    SupplyTransaction,
)


def _safe_value(value):
    if isinstance(value, Decimal):
        return str(value)

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass

    return value


def _serialize_queryset(queryset, fields, limit=50):
    result = []

    for item in queryset[:limit]:
        row = {}

        for field in fields:
            try:
                value = getattr(item, field)
                row[field] = _safe_value(value)
            except Exception:
                row[field] = None

        result.append(row)

    return result


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def finance_overview(request):

    return Response({
        "platform": "NSIKAY",
        "status": "ACTIVE",

        "currencies": _serialize_queryset(
            Currency.objects.all(),
            ["id", "code", "name"],
        ),

        "exchange_rates": _serialize_queryset(
            ExchangeRate.objects.all().order_by("-id"),
            ["id", "base_currency", "quote_currency", "rate"],
            50,
        ),

        "banks": _serialize_queryset(
            Bank.objects.all(),
            ["id", "name"],
            50,
        ),

        "bank_accounts": _serialize_queryset(
            BankAccount.objects.all(),
            ["id", "bank", "account_number"],
            50,
        ),

        "bank_services": _serialize_queryset(
            BankService.objects.all(),
            ["id", "name"],
            50,
        ),

        "bank_credits": _serialize_queryset(
            BankCredit.objects.all(),
            ["id"],
            50,
        ),

        "bank_insurances": _serialize_queryset(
            BankInsurance.objects.all(),
            ["id"],
            50,
        ),

        "bank_operations": _serialize_queryset(
            BankingOperation.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "bank_transactions": _serialize_queryset(
            BankTransaction.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "bank_balances": _serialize_queryset(
            BankBalance.objects.all(),
            ["id"],
            50,
        ),

        "partner_applications": _serialize_queryset(
            PartnerApplication.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "partner_certifications": _serialize_queryset(
            PartnerCertification.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "partner_supplies": _serialize_queryset(
            PartnerSupply.objects.all(),
            ["id"],
            50,
        ),

        "partner_wallets": _serialize_queryset(
            PartnerWallet.objects.all(),
            ["id"],
            50,
        ),

        "partner_deposits": _serialize_queryset(
            PartnerDeposit.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "supply_transactions": _serialize_queryset(
            SupplyTransaction.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "commissions": _serialize_queryset(
            PlatformCommission.objects.all().order_by("-id"),
            ["id", "amount", "currency"],
            50,
        ),

        "fees": _serialize_queryset(
            FeeConfiguration.objects.all(),
            ["id"],
            50,
        ),

        "routing_rules": _serialize_queryset(
            FinancialRoutingRule.objects.all(),
            ["id"],
            50,
        ),

        "routing_logs": _serialize_queryset(
            FinancialRoutingLog.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "control_reports": _serialize_queryset(
            FinancialControlReport.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "audit_logs": _serialize_queryset(
            FinancialAuditLog.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "compliance_logs": _serialize_queryset(
            FinancialComplianceLog.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "fraud_alerts": _serialize_queryset(
            FraudDetectionAlert.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "compliance_reports": _serialize_queryset(
            ComplianceReport.objects.all().order_by("-id"),
            ["id"],
            50,
        ),

        "partner_approvals": _serialize_queryset(
            PartnerApproval.objects.all().order_by("-id"),
            ["id"],
            50,
        ),
    })

