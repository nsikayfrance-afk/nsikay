from decimal import Decimal


def calculate_fees(transaction_type, amount):

    amount = Decimal(amount)


    if transaction_type == "transfer":

        return amount * Decimal("0.0025")


    if transaction_type == "withdrawal":

        return amount * Decimal("0.0050")


    return Decimal("0.00")



def process_transaction(transaction):


    fees = calculate_fees(

        transaction.transaction_type,

        transaction.amount

    )


    transaction.status = "completed"

    transaction.save()


    return {

        "reference":
        transaction.reference,


        "amount":
        str(transaction.amount),


        "currency":
        transaction.currency.code,


        "fees":
        str(fees),


        "status":
        transaction.status

    }

