from django.db.models import Sum

from finance.models import FinancialOperation


def financial_report():

    return {

        "total_operations":
            FinancialOperation.objects.count(),

        "volume":
            FinancialOperation.objects.aggregate(
                total=Sum("amount")
            )["total"] or 0,

        "commissions":
            FinancialOperation.objects.aggregate(
                total=Sum("fee")
            )["total"] or 0,
    }
