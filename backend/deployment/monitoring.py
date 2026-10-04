from django.http import JsonResponse
import time


def health_check(request):

    return JsonResponse({

        "service":
        "NSIKAY",

        "status":
        "ONLINE",

        "timestamp":
        time.time()

    })


