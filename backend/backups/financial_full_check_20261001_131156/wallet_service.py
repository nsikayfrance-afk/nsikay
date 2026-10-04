from decimal import Decimal

from .models import WalletTransaction



def credit_wallet(wallet, amount, reference):

    wallet.balance += Decimal(amount)

    wallet.save()


    WalletTransaction.objects.create(

        wallet=wallet,

        transaction_type="deposit",

        amount=amount,

        reference=reference,

        status="completed"

    )


    return wallet.balance




def debit_wallet(wallet, amount, reference):

    amount = Decimal(amount)


    if wallet.balance < amount:

        raise Exception(
            "Solde insuffisant"
        )


    wallet.balance -= amount

    wallet.save()


    WalletTransaction.objects.create(

        wallet=wallet,

        transaction_type="withdraw",

        amount=amount,

        reference=reference,

        status="completed"

    )


    return wallet.balance




def transfer_wallet(sender, receiver, amount, reference):

    amount = Decimal(amount)


    if sender.balance < amount:

        raise Exception(
            "Solde insuffisant"
        )


    sender.balance -= amount

    receiver.balance += amount


    sender.save()

    receiver.save()


    WalletTransaction.objects.create(

        wallet=sender,

        transaction_type="transfer",

        amount=amount,

        reference=reference+"-OUT",

        status="completed"

    )


    WalletTransaction.objects.create(

        wallet=receiver,

        transaction_type="transfer",

        amount=amount,

        reference=reference+"-IN",

        status="completed"

    )


    return True


