from rest_framework.decorators import api_view, permission_classes`r`nfrom rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from wallet.models import Wallet, WalletTransaction



@api_view(["GET"])
@authentication_classes([TokenAuthentication])`r`n@permission_classes([IsAuthenticated])
def wallet_dashboard(request):

    user = request.user


    wallet = Wallet.objects.filter(
        user=user
    ).first()


    if not wallet:

        return Response(
            {
                "status":"NO_WALLET"
            }
        )


    balances = []


    if hasattr(wallet, "currency_balances"):

        for item in wallet.currency_balances.all():

            balances.append(
                {
                    "currency": item.currency,
                    "balance": item.balance
                }
            )


    operations = []


    if hasattr(wallet, "operations"):

        for operation in wallet.operations.all()[:10]:

            operations.append(
                {
                    "type": operation.operation_type,
                    "amount": operation.amount,
                    "currency": operation.currency,
                    "date": operation.created_at
                }
            )


    kyc = getattr(
        user,
        "wallet_kyc",
        None
    )


    return Response(
        {

            "platform":"NSIKAY",

            "wallet_id":wallet.id,

            "balances":balances,

            "kyc":{

                "level":
                kyc.level if kyc else "LEVEL_1",

                "active":
                kyc.active if kyc else False

            },


            "operations":operations,

            "security":"ACTIVE"

        }
    )



