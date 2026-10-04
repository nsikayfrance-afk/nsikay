from decimal import Decimal

from finance.models import Wallet
from finance.wallet_service import (
    credit_wallet,
    debit_wallet
)

from .models import (
    DepositRequest,
    WithdrawalRequest,
    OperationApproval
)



def complete_deposit(deposit_id):

    deposit = DepositRequest.objects.get(
        id=deposit_id
    )


    wallet = Wallet.objects.get(

        user=deposit.user,

        currency=deposit.currency

    )


    credit_wallet(

        wallet,

        deposit.amount,

        deposit.reference

    )


    deposit.status = "completed"

    deposit.save()


    OperationApproval.objects.create(

        operation_type="deposit",

        operation_id=deposit.id,

        approved_by="bank",

        decision="approved"

    )


    return True




def complete_withdrawal(withdrawal_id):

    withdrawal = WithdrawalRequest.objects.get(

        id=withdrawal_id

    )


    wallet = Wallet.objects.get(

        user=withdrawal.user,

        currency=withdrawal.currency

    )


    debit_wallet(

        wallet,

        withdrawal.amount,

        withdrawal.reference

    )


    withdrawal.status = "completed"

    withdrawal.save()


    OperationApproval.objects.create(

        operation_type="withdrawal",

        operation_id=withdrawal.id,

        approved_by="bank",

        decision="approved"

    )


    return True

