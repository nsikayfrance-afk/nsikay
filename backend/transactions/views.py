from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Transaction
from .services import process_transaction



def execute_transaction(request, transaction_id):

    transaction = get_object_or_404(

        Transaction,

        id=transaction_id

    )


    result = process_transaction(transaction)


    return JsonResponse(result)

