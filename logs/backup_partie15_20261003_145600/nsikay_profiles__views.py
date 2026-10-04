from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import NsikayProfile
from .serializers import NsikayProfileSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = NsikayProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NsikayProfile.objects.filter(
            user=self.request.user
        ).order_by(
            "-is_primary",
            "-updated_at",
        )


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NsikayProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NsikayProfile.objects.filter(
            user=self.request.user
        )
