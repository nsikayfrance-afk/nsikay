from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TVChannel
from .serializers.tv_serializer import TVChannelSerializer



class TVListAPIView(APIView):

    def get(self,request):

        channels = TVChannel.objects.filter(
            is_active=True
        )

        serializer = TVChannelSerializer(
            channels,
            many=True
        )

        return Response(
            serializer.data
        )

