from decimal import Decimal


MAX_TRANSACTION_RISK = 80



def analyze_operation(
    wallet,
    operation,
    amount,
    currency
):


    risk = 0


    amount = Decimal(amount)


    if amount > Decimal("10000"):

        risk += 50


    if operation in [
        "withdraw",
        "transfer"
    ]:

        risk += 20



    from finance.models import FraudDetectionEvent


    blocked = risk >= MAX_TRANSACTION_RISK



    event = FraudDetectionEvent.objects.create(

        wallet=wallet,

        operation=operation,

        amount=amount,

        currency=currency,

        risk_score=risk,

        blocked=blocked

    )


    if blocked:

        from finance.models import WalletSecurityStatus


        WalletSecurityStatus.objects.update_or_create(

            wallet=wallet,

            defaults={

                "status":"BLOCKED",

                "reason":
                "Activité financière inhabituelle détectée"

            }

        )


    return event


