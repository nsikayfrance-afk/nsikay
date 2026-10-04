from rest_framework.decorators import api_view

from rest_framework.response import Response

from finance.models import MarketplaceProduct



@api_view(["GET"])

def marketplace_products(request):


    products = MarketplaceProduct.objects.filter(

        available=True

    )


    return Response([

        {

            "id":p.id,

            "name":p.name,

            "price":p.price,

            "currency":p.currency

        }

        for p in products

    ])


