from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import TVChannel
from .serializers.tv_serializer import TVChannelSerializer


class TVListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        channels = TVChannel.objects.filter(
            is_active=True
        ).order_by(
            "category",
            "title",
            "id",
        )

        serializer = TVChannelSerializer(
            channels,
            many=True
        )

        return Response(serializer.data)
