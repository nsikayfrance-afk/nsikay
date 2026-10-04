from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class FinanceStatusView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        return Response({

            "system":
            "NSIKAY FINANCE",

            "status":
            "ACTIVE",

            "controls":[

                "KYC",

                "TRANSACTION LIMITS",

                "AUDIT LOG",

                "RISK MONITORING"

            ]

        })





