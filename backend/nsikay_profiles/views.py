from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import NsikayProfile
from .serializers import NsikayProfileSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = NsikayProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            NsikayProfile.objects
            .filter(
                user=self.request.user,
                is_primary=True,
                profile_type="person",
            )
            .order_by("-updated_at")
        )


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NsikayProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            NsikayProfile.objects
            .filter(
                user=self.request.user,
                is_primary=True,
                profile_type="person",
            )
        )

    def perform_destroy(self, instance):
        raise ValidationError({
            "profile": (
                "Le profil personnel principal ne peut pas être supprimé. "
                "Le compte NSIKAY doit conserver son identité personnelle."
            )
        })
