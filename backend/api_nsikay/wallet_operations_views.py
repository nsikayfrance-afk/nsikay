from decimal import Decimal, InvalidOperation

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wallet.services import (
    calculate_transfer_fee,
    calculate_withdraw_fee
)


def _decimal(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None

    if amount <= 0:
        return None

    return amount


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wallet_deposit(request):

    amount = _decimal(request.data.get("amount"))

    if amount is None:
        return Response(
            {
                "status": "ERROR",
                "message": "Montant invalide."
            },
            status=400
        )

    return Response(
        {
            "status": "PENDING_VALIDATION",
            "operation": "DEPOSIT",
            "amount": amount
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wallet_withdraw(request):

    amount = _decimal(request.data.get("amount"))

    if amount is None:
        return Response(
            {
                "status": "ERROR",
                "message": "Montant invalide."
            },
            status=400
        )

    fee = calculate_withdraw_fee(amount)

    return Response(
        {
            "status": "PENDING_VALIDATION",
            "operation": "WITHDRAW",
            "amount": amount,
            "fee": fee,
            "received": amount - fee
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wallet_transfer(request):

    amount = _decimal(request.data.get("amount"))

    if amount is None:
        return Response(
            {
                "status": "ERROR",
                "message": "Montant invalide."
            },
            status=400
        )

    fee = calculate_transfer_fee(amount)

    return Response(
        {
            "status": "PENDING_VALIDATION",
            "operation": "TRANSFER",
            "amount": amount,
            "commission": fee
        }
    )
