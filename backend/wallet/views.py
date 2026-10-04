from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WalletBalance, WalletTransaction


class WalletBalanceView(APIView):

    def get(self, request):

        balances = WalletBalance.objects.all()

        data = []

        for item in balances:
            data.append({
                "currency": item.currency,
                "balance": item.available_balance
            })

        return Response(data)



class WalletHistoryView(APIView):

    def get(self, request):

        transactions = WalletTransaction.objects.all()

        data = []

        for t in transactions:
            data.append({
                "type": t.transaction_type,
                "amount": t.amount,
                "currency": t.currency,
                "status": t.status
            })

        return Response(data)

