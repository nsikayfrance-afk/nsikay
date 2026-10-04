from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def marketplace_products(request):
    """
    Interface Marketplace historique desactivee.

    Le module commercial officiel de NSIKAY est WENZE.
    Les anciens modeles Marketplace restent conserves pour
    compatibilite historique et migrations.
    """
    return Response(
        {
            "status": "deprecated",
            "module": "WENZE",
            "message": "Le module Marketplace historique est desactive. Utilisez WENZE.",
            "wenze_path": "/wenze/"
        },
        status=410
    )
