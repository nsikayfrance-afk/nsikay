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
            "profile_type",
            "profile_type_label",
            "is_primary",
            "created_at",
            "updated_at",
            "certification_status",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        if (
            not request
            or not request.user
            or not request.user.is_authenticated
        ):
            raise serializers.ValidationError(
                "Un utilisateur authentifié est requis."
            )

        # ========================================================
        # REGLE FONDAMENTALE :
        # LE PROFIL PRINCIPAL EST TOUJOURS UN PROFIL PERSONNEL.
        # ========================================================

        if self.instance is not None:
            if self.instance.is_primary:
                if self.instance.profile_type != "person":
                    raise serializers.ValidationError({
                        "profile_type": (
                            "Le profil principal doit rester de type personne."
                        )
                    })

            elif self.instance.profile_type != "person":
                raise serializers.ValidationError({
                    "profile": (
                        "Les anciens profils d'activité sont conservés "
                        "comme archives de migration. Les activités doivent "
                        "désormais être gérées dans /api/activities/."
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

        existing_primary = (
            NsikayProfile.objects
            .filter(
                user=user,
                is_primary=True,
            )
            .first()
        )

        # ========================================================
        # UN COMPTE NE PEUT PAS CREER UN SECOND PROFIL.
        # ========================================================

        if existing_primary:
            raise serializers.ValidationError({
                "profile": (
                    "Ce compte possède déjà son profil personnel principal. "
                    "Les nouvelles structures doivent être créées comme "
                    "activités."
                )
            })

        # Sécurité supplémentaire pour une éventuelle création
        # historique ou administrative.
        validated_data["profile_type"] = "person"
        validated_data["is_primary"] = True

        return NsikayProfile.objects.create(
            user=user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        # Le statut de certification ne peut pas être modifié
        # directement par le propriétaire du profil.
        validated_data.pop("certification_status", None)

        # Le profil principal reste obligatoirement "person".
        if instance.is_primary:
            validated_data["profile_type"] = "person"
            validated_data["is_primary"] = True

        return super().update(
            instance,
            validated_data,
        )
