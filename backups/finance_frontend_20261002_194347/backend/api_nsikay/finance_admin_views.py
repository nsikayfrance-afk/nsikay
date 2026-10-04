from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from wallet.models import Wallet

from finance.models import (
    FinancialLedger,
    PlatformCommission
)



@api_view(["GET"])
@permission_classes([IsAdminUser])
def finance_admin_dashboard(request):


    wallets = Wallet.objects.count()


    ledger_count = FinancialLedger.objects.count()


    commissions = PlatformCommission.objects.all()


    total_commission = sum(

        [
            c.amount
            for c in commissions
        ]

    )


    currencies = {}


    for item in FinancialLedger.objects.all():

        currencies[item.currency] = (

            currencies.get(item.currency,0)

            +

            float(item.amount)

        )


    latest = []


    for entry in FinancialLedger.objects.order_by(
        "-created_at"
    )[:20]:

        latest.append({

            "reference":
            entry.reference,

            "type":
            entry.transaction_type,

            "amount":
            entry.amount,

            "currency":
            entry.currency,

            "date":
            entry.created_at

        })


    return Response({

        "platform":
        "NSIKAY",

        "wallets":
        wallets,

        "ledger_entries":
        ledger_count,

        "commission_total":
        total_commission,

        "volumes":
        currencies,

        "latest_transactions":
        latest,

        "security":
        "ADMIN_PROTECTED"

    })

