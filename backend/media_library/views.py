from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import (
    MediaAsset,
    MediaDestination,
    MediaDistribution,
    MediaSegment,
)
from .serializers import (
    MediaAssetSerializer,
    MediaDestinationSerializer,
    MediaDistributionSerializer,
    MediaSegmentSerializer,
)


class MediaAssetViewSet(viewsets.ModelViewSet):

    queryset = MediaAsset.objects.prefetch_related(
        "distributions__destination",
        "segments__destinations",
    ).all()

    serializer_class = MediaAssetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        uploaded = self.request.FILES.get("file")

        serializer.save(
            owner=self.request.user,
            original_filename=(
                uploaded.name if uploaded else ""
            ),
            mime_type=(
                uploaded.content_type if uploaded else ""
            ),
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="set-destinations"
    )
    def set_destinations(self, request, pk=None):
        asset = self.get_object()

        destination_ids = request.data.get(
            "destination_ids",
            []
        )

        if not isinstance(destination_ids, list):
            return Response(
                {
                    "detail": "destination_ids doit être une liste."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        destinations = MediaDestination.objects.filter(
            id__in=destination_ids,
            active=True
        )

        existing = {
            distribution.destination_id
            for distribution in asset.distributions.all()
        }

        selected = set(
            destinations.values_list("id", flat=True)
        )

        for destination in destinations:
            MediaDistribution.objects.get_or_create(
                asset=asset,
                destination=destination,
                defaults={
                    "created_by": request.user,
                    "status": MediaDistribution.STATUS_PENDING,
                }
            )

        for distribution in asset.distributions.all():
            if distribution.destination_id not in selected:
                distribution.delete()

        return Response(
            MediaAssetSerializer(
                asset,
                context={"request": request}
            ).data
        )


class MediaDestinationViewSet(viewsets.ModelViewSet):

    queryset = MediaDestination.objects.filter(
        active=True
    ).all()

    serializer_class = MediaDestinationSerializer
    permission_classes = [IsAuthenticated]


class MediaDistributionViewSet(viewsets.ModelViewSet):

    queryset = MediaDistribution.objects.select_related(
        "asset",
        "destination"
    ).all()

    serializer_class = MediaDistributionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-live"
    )
    def mark_live(self, request, pk=None):
        distribution = self.get_object()

        distribution.status = MediaDistribution.STATUS_LIVE
        distribution.started_at = timezone.now()
        distribution.message = "Diffusion marquée comme active."
        distribution.save(
            update_fields=[
                "status",
                "started_at",
                "message",
                "updated_at",
            ]
        )

        return Response(
            MediaDistributionSerializer(distribution).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-published"
    )
    def mark_published(self, request, pk=None):
        distribution = self.get_object()

        distribution.status = MediaDistribution.STATUS_PUBLISHED
        distribution.finished_at = timezone.now()
        distribution.message = "Publication marquée comme terminée."
        distribution.save(
            update_fields=[
                "status",
                "finished_at",
                "message",
                "updated_at",
            ]
        )

        return Response(
            MediaDistributionSerializer(distribution).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-failed"
    )
    def mark_failed(self, request, pk=None):
        distribution = self.get_object()

        distribution.status = MediaDistribution.STATUS_FAILED
        distribution.finished_at = timezone.now()
        distribution.message = request.data.get(
            "message",
            "Diffusion en échec."
        )
        distribution.save(
            update_fields=[
                "status",
                "finished_at",
                "message",
                "updated_at",
            ]
        )

        return Response(
            MediaDistributionSerializer(distribution).data
        )


class MediaSegmentViewSet(viewsets.ModelViewSet):

    queryset = MediaSegment.objects.prefetch_related(
        "destinations"
    ).all()

    serializer_class = MediaSegmentSerializer
    permission_classes = [IsAuthenticated]
