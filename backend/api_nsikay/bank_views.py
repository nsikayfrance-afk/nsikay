from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .bank_models import PartnerBank


class BanksListView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        banks = PartnerBank.objects.filter(
            status="ACTIVE"
        )


        return Response([

            {
                "id":b.id,
                "name":b.name,
                "country":b.country
            }

            for b in banks

        ])

