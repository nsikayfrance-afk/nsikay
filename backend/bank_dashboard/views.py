from django.shortcuts import render, redirect

from banking.models import (
    OnlineBankAccountRequest,
    BankReport
)

from operations.models import (
    DepositRequest,
    WithdrawalRequest
)



def dashboard(request):

    accounts = OnlineBankAccountRequest.objects.all()

    deposits = DepositRequest.objects.all()

    withdrawals = WithdrawalRequest.objects.all()

    reports = BankReport.objects.all()


    return render(

        request,

        "bank_dashboard/dashboard.html",

        {

            "accounts": accounts,

            "deposits": deposits,

            "withdrawals": withdrawals,

            "reports": reports

        }

    )




def accept_account(request, account_id):

    account = OnlineBankAccountRequest.objects.get(

        id=account_id

    )


    account.status = "approved"

    account.save()


    return redirect("bank_dashboard")




def activate_account(request, account_id):

    account = OnlineBankAccountRequest.objects.get(

        id=account_id

    )


    account.status = "activated"

    account.save()


    return redirect("bank_dashboard")




def reject_account(request, account_id):

    account = OnlineBankAccountRequest.objects.get(

        id=account_id

    )


    account.status = "rejected"

    account.save()


    return redirect("bank_dashboard")




def validate_deposit(request, deposit_id):

    deposit = DepositRequest.objects.get(

        id=deposit_id

    )


    deposit.status = "completed"

    deposit.save()


    return redirect("bank_dashboard")




def validate_withdrawal(request, withdrawal_id):

    withdrawal = WithdrawalRequest.objects.get(

        id=withdrawal_id

    )


    withdrawal.status = "completed"

    withdrawal.save()


    return redirect("bank_dashboard")


from django.http import JsonResponse


def index(request):
    return JsonResponse({
        'module':'NSIKAY',
        'status':'active'
    })

