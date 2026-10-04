from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_nsikay.models import SocialPost



@api_view(["GET"])
def social_feed(request):

    posts = SocialPost.objects.all().order_by(
        "-created_at"
    )[:50]


    return Response([

        {

            "author":
            p.author.username,

            "content":
            p.content,

            "likes":
            p.likes

        }

        for p in posts

    ])


