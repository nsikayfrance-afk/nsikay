from rest_framework import serializers

from .models import NsikayProfile


class NsikayProfileSerializer(serializers.ModelSerializer):

    profile_type_label = serializers.CharField(
        source="get_profile_type_display",
        read_only=True,
    )

    visibility_label = serializers.CharField(
        source="get_visibility_display",
        read_only=True,
    )

    status_label = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = NsikayProfile
        fields = [
            "id",
            "profile_type",
            "profile_type_label",
            "display_name",
            "legal_name",
            "professional_title",
            "description",
            "country",
            "city",
            "phone",
            "website",
            "sector",
            "visibility",
            "visibility_label",
            "status",
            "status_label",
            "is_primary",
            "certification_required",
            "certification_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "certification_status",
        ]

    def validate_display_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le nom du profil est obligatoire."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return NsikayProfile.objects.create(
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        validated_data.pop("certification_status", None)

        return super().update(
            instance,
            validated_data,
        )
