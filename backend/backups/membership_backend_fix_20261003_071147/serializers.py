from rest_framework import serializers

from .models import (
    Member,
    MembershipType,
    MembershipApplication,
    MemberCard,
    Subscription,
)


class MembershipTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipType
        fields = [
            "id",
            "name",
            "description",
            "contribution_required",
        ]


class MemberCardSerializer(serializers.ModelSerializer):

    verification_path = serializers.ReadOnlyField()

    class Meta:
        model = MemberCard
        fields = [
            "member_number",
            "status",
            "issued_at",
            "expires_at",
            "verification_path",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            "id",
            "amount",
            "currency",
            "payment_status",
            "paid_at",
        ]


class MembershipApplicationSerializer(serializers.ModelSerializer):

    membership_type_detail = MembershipTypeSerializer(
        source="membership_type",
        read_only=True,
    )

    class Meta:
        model = MembershipApplication
        fields = [
            "id",
            "membership_type",
            "membership_type_detail",
            "status",
            "message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status",
            "created_at",
            "updated_at",
        ]


class MemberSerializer(serializers.ModelSerializer):

    membership_type_detail = MembershipTypeSerializer(
        source="membership_type",
        read_only=True,
    )

    card = MemberCardSerializer(
        source="official_card",
        read_only=True,
    )

    subscriptions = SubscriptionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Member
        fields = [
            "id",
            "status",
            "joined_at",
            "membership_type",
            "membership_type_detail",
            "card",
            "subscriptions",
        ]
        read_only_fields = [
            "status",
            "joined_at",
        ]
