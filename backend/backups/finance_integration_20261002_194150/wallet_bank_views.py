from rest_framework.decorators import api_view

from rest_framework.response import Response


from wallet.models import WalletBankAccount



@api_view(["POST"])

def add_bank_account(request):

    bank = WalletBankAccount.objects.create(

        wallet_id=request.data.get("wallet_id"),

        bank_name=request.data.get("bank_name"),

        account_name=request.data.get("account_name"),

        account_number=request.data.get("account_number"),

        country=request.data.get("country"),

        currency=request.data.get(
            "currency",
            "USD"
        )

    )


    return Response({

        "status":"PENDING",

        "bank_account_id":bank.id,

        "message":
        "Compte bancaire soumis pour certification NSIKAY"

    })



@api_view(["GET"])

def wallet_banks(request, wallet_id):

    banks = WalletBankAccount.objects.filter(

        wallet_id=wallet_id

    )


    return Response([

        {

            "bank":b.bank_name,

            "currency":b.currency,

            "certified":b.certified,

            "status":b.status

        }

        for b in banks

    ])


