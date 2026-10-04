from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Event,
    EventTicket,
    EventRegistration,
    EventMediaLink,
)

from .serializers import (
    EventSerializer,
    EventTicketSerializer,
    EventRegistrationSerializer,
    EventMediaLinkSerializer,
)


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.select_related(
        "organizer"
    ).prefetch_related(
        "tickets",
        "registrations",
        "media_links",
    )

    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None):
        event = self.get_object()
        event.status = Event.STATUS_PUBLISHED
        event.save(update_fields=["status", "updated_at"])
        return Response(EventSerializer(
            event,
            context={"request": request}
        ).data)

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
    )
    def cancel(self, request, pk=None):
        event = self.get_object()
        event.status = Event.STATUS_CANCELLED
        event.save(update_fields=["status", "updated_at"])
        return Response(EventSerializer(
            event,
            context={"request": request}
        ).data)

    @action(
        detail=True,
        methods=["post"],
        url_path="finish",
    )
    def finish(self, request, pk=None):
        event = self.get_object()
        event.status = Event.STATUS_FINISHED
        event.save(update_fields=["status", "updated_at"])
        return Response(EventSerializer(
            event,
            context={"request": request}
        ).data)


class EventTicketViewSet(viewsets.ModelViewSet):

    queryset = EventTicket.objects.select_related("event")
    serializer_class = EventTicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventRegistrationViewSet(viewsets.ModelViewSet):

    queryset = EventRegistration.objects.select_related(
        "event",
        "user",
        "ticket",
    )

    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventMediaLinkViewSet(viewsets.ModelViewSet):

    queryset = EventMediaLink.objects.select_related("event")
    serializer_class = EventMediaLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
