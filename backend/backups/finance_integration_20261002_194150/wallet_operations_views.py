from rest_framework.decorators import api_view
from rest_framework.response import Response

from decimal import Decimal

from wallet.services import (
    calculate_transfer_fee,
    calculate_withdraw_fee
)


@api_view(["POST"])
def wallet_deposit(request):

    return Response(
        {
            "status":"SUCCESS",
            "operation":"DEPOSIT",
            "amount":request.data.get("amount")
        }
    )



@api_view(["POST"])
def wallet_withdraw(request):

    amount = Decimal(
        request.data.get("amount",0)
    )

    fee = calculate_withdraw_fee(amount)

    return Response(
        {
            "status":"PENDING_VALIDATION",
            "operation":"WITHDRAW",
            "amount":amount,
            "fee":fee,
            "received":amount-fee
        }
    )



@api_view(["POST"])
def wallet_transfer(request):

    amount = Decimal(
        request.data.get("amount",0)
    )

    fee = calculate_transfer_fee(amount)

    return Response(
        {
            "status":"SUCCESS",
            "operation":"TRANSFER",
            "amount":amount,
            "commission":fee
        }
    )


