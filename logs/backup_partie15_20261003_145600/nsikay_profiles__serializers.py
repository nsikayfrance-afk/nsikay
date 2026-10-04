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
        "specialized_data",
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

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Un utilisateur authentifié est requis."
            )

        profile_type = attrs.get(
            "profile_type",
            getattr(self.instance, "profile_type", None),
        )

        is_primary = attrs.get(
            "is_primary",
            getattr(self.instance, "is_primary", False),
        )

        if is_primary:
            existing_primary = (
                NsikayProfile.objects
                .filter(
                    user=request.user,
                    is_primary=True,
                )
            )

            if self.instance is not None:
                existing_primary = existing_primary.exclude(
                    pk=self.instance.pk
                )

            if existing_primary.exists():
                raise serializers.ValidationError({
                    "is_primary": (
                        "Ce compte possède déjà un profil personnel principal."
                    )
                })

        if is_primary and profile_type != "person":
            raise serializers.ValidationError({
                "profile_type": (
                    "Le profil principal d'un compte doit être de type personne."
                )
            })

        return attrs
    def validate_display_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le nom du profil est obligatoire."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user

        has_primary = NsikayProfile.objects.filter(
            user=user,
            is_primary=True,
        ).exists()

        if not has_primary:
            validated_data["is_primary"] = True
            validated_data["profile_type"] = "person"

        elif validated_data.get("is_primary", False):
            raise serializers.ValidationError({
                "is_primary": (
                    "Ce compte possède déjà un profil personnel principal."
                )
            })

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




