from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from .models import Wallet, WalletBalance, WalletTransaction
import uuid


class WalletSecureBalanceView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        wallet, created = Wallet.objects.get_or_create(
            user=request.user
        )

        balances = WalletBalance.objects.filter(
            wallet=wallet
        )


        return Response([
            {
                "currency": b.currency,
                "available": b.available_balance,
                "locked": b.locked_balance
            }
            for b in balances
        ])



class WalletTransferView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        amount = Decimal(
            request.data.get(
                "amount",
                0
            )
        )

        currency = request.data.get(
            "currency",
            "USD"
        )


        fee = amount * Decimal(
            "0.0025"
        )


        transaction = WalletTransaction.objects.create(

            wallet=Wallet.objects.get(
                user=request.user
            ),

            transaction_type="TRANSFER",

            amount=amount,

            currency=currency,

            reference=str(
                uuid.uuid4()
            ),

            status="COMPLETED"
        )


        return Response({

            "status":"success",

            "amount":amount,

            "fee":fee,

            "reference":transaction.reference

        })



class WalletWithdrawView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        amount = Decimal(
            request.data.get(
                "amount",
                0
            )
        )


        fee = amount * Decimal(
            "0.012"
        )


        return Response({

            "operation":
            "WITHDRAWAL",

            "amount":
            amount,

            "fee":
            fee,

            "received":
            amount-fee

        })

