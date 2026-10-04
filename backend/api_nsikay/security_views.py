from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response



@api_view(["GET"])

@permission_classes([IsAuthenticated])

def security_profile(request):


    user = request.user


    role = "CLIENT"


    if hasattr(
        user,
        "nsikay_role"
    ):

        role = user.nsikay_role.role



    return Response({

        "platform":"NSIKAY",

        "user":user.username,

        "role":role,

        "authenticated":True

    })


