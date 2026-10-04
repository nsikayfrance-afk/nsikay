from rest_framework.decorators import api_view

from rest_framework.response import Response


@api_view(["GET"])

def gateway_status(request):


    return Response({

        "platform":
        "NSIKAY",

        "gateway":
        "ACTIVE",

        "environment":
        "PRODUCTION_READY"

    })


