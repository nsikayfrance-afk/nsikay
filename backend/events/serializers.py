from rest_framework import serializers

from .models import (
    Event,
    EventTicket,
    EventRegistration,
    EventMediaLink,
)


class EventTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventTicket
        fields = "__all__"
        read_only_fields = ["created_at"]


class EventRegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = EventRegistration
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]


class EventMediaLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventMediaLink
        fields = "__all__"
        read_only_fields = ["created_at"]


class EventSerializer(serializers.ModelSerializer):

    organizer_username = serializers.CharField(
        source="organizer.username",
        read_only=True,
    )

    tickets = EventTicketSerializer(
        many=True,
        read_only=True,
    )

    registrations_count = serializers.IntegerField(
        source="registrations.count",
        read_only=True,
    )

    media_links = EventMediaLinkSerializer(
        many=True,
        read_only=True,
    )

    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = [
            "organizer",
            "created_at",
            "updated_at",
        ]

    def get_poster_url(self, obj):
        if not obj.poster:
            return ""

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.poster.url)

        return obj.poster.url
