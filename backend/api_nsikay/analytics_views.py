from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_nsikay.models import AdminAnalytics



@api_view(["GET"])

def admin_analytics(request):


    data = AdminAnalytics.objects.all()


    return Response([

        {

            "metric":x.metric,

            "value":x.value,

            "category":x.category

        }

        for x in data

    ])


