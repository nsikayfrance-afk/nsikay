from django.db import transaction
from rest_framework import serializers

from .models import Activity, Service, Project
from gift_resellers.models import Reseller


class ActivitySerializer(serializers.ModelSerializer):

    profile_display_name = serializers.CharField(
        source="profile.display_name",
        read_only=True,
    )

    profile_type = serializers.CharField(
        source="profile.profile_type",
        read_only=True,
    )

    profile_type_label = serializers.CharField(
        source="profile.get_profile_type_display",
        read_only=True,
    )

    service_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity

        fields = [
            "id",
            "profile",
            "profile_display_name",
            "profile_type",
            "profile_type_label",
            "name",
            "activity_type",
            "description",
            "sector",
            "country",
            "city",
            "phone",
            "website",
            "status",
            "visibility",
            "certification_required",
            "certification_status",
            "service_count",
            "project_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "profile",
            "profile_display_name",
            "profile_type",
            "profile_type_label",
            "certification_status",
            "service_count",
            "project_count",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        name = attrs.get("name")

        if name is not None and not str(name).strip():
            raise serializers.ValidationError({
                "name": "Le nom de l'activité est obligatoire."
            })

        activity_type = attrs.get("activity_type")

        # ========================================================
        # REGLES MINIMALES PAR TYPE
        # ========================================================

        if activity_type == "gift_reseller":
            request = self.context.get("request")

            if request and request.user.is_authenticated:
                existing_reseller = (
                    Reseller.objects
                    .filter(
                        user=request.user,
                        activity__isnull=False,
                    )
                    .first()
                )

                if (
                    existing_reseller
                    and (
                        self.instance is None
                        or existing_reseller.activity_id != self.instance.pk
                    )
                ):
                    raise serializers.ValidationError({
                        "activity_type": (
                            "Ce compte possède déjà une activité "
                            "Revendeur de cadeaux."
                        )
                    })

        return attrs

    def _get_primary_profile(self):
        request = self.context.get("request")

        if (
            not request
            or not request.user
            or not request.user.is_authenticated
        ):
            raise serializers.ValidationError({
                "profile": "Un utilisateur authentifié est requis."
            })

        profile = (
            request.user.nsikay_profiles
            .filter(
                is_primary=True,
                profile_type="person",
            )
            .first()
        )

        if profile is None:
            raise serializers.ValidationError({
                "profile": (
                    "Aucun profil personnel principal valide n'est disponible "
                    "pour ce compte."
                )
            })

        return profile

    @transaction.atomic
    def create(self, validated_data):
        # ========================================================
        # REGLE FONDAMENTALE :
        # UNE ACTIVITE EST TOUJOURS RATTACHEE AU PROFIL PERSONNEL
        # PRINCIPAL DU COMPTE.
        # ========================================================

        profile = self._get_primary_profile()

        validated_data["profile"] = profile

        activity = Activity.objects.create(
            **validated_data
        )

        # ========================================================
        # REVENDEUR DE CADEAUX
        # ========================================================

        if activity.activity_type == "gift_reseller":
            user = profile.user

            reseller = (
                Reseller.objects
                .filter(user=user)
                .first()
            )

            if reseller is None:
                Reseller.objects.create(
                    user=user,
                    activity=activity,
                    status="PENDING",
                    reseller_code=f"NSIKAY-R-{user.id}-{activity.id}",
                    country_code="",
                    notes=(
                        "Créé automatiquement depuis l'activité "
                        "Revendeur de cadeaux."
                    ),
                )

            elif reseller.activity_id and reseller.activity_id != activity.id:
                raise serializers.ValidationError({
                    "activity_type": (
                        "Ce compte possède déjà un Revendeur de cadeaux."
                    )
                })

            else:
                reseller.activity = activity
                reseller.save(
                    update_fields=[
                        "activity",
                        "updated_at",
                    ]
                )

        return activity

    def update(self, instance, validated_data):
        # Le rattachement au profil personnel est immuable.
        validated_data.pop("profile", None)

        validated_data.pop(
            "certification_status",
            None,
        )

        return super().update(
            instance,
            validated_data,
        )

    def get_service_count(self, obj):
        return obj.services.count()

    def get_project_count(self, obj):
        return obj.projects.count()


class ServiceSerializer(serializers.ModelSerializer):

    activity_name = serializers.CharField(
        source="activity.name",
        read_only=True,
    )

    class Meta:
        model = Service

        fields = [
            "id",
            "activity",
            "activity_name",
            "name",
            "description",
            "category",
            "price",
            "currency",
            "status",
            "certification_required",
            "certification_status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
            "activity_name",
        ]

    def validate_activity(self, activity):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            if activity.profile.user_id != request.user.id:
                raise serializers.ValidationError(
                    "Cette activité n'appartient pas à l'utilisateur."
                )

        return activity

    def validate(self, attrs):
        price = attrs.get("price")

        if price is not None and price < 0:
            raise serializers.ValidationError({
                "price": "Le prix ne peut pas être négatif."
            })

        return attrs


class ProjectSerializer(serializers.ModelSerializer):

    activity_name = serializers.CharField(
        source="activity.name",
        read_only=True,
    )

    class Meta:
        model = Project

        fields = [
            "id",
            "activity",
            "activity_name",
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
            "activity_name",
        ]

    def validate_activity(self, activity):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            if activity.profile.user_id != request.user.id:
                raise serializers.ValidationError(
                    "Cette activité n'appartient pas à l'utilisateur."
                )

        return activity

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": (
                    "La date de fin ne peut pas précéder "
                    "la date de début."
                )
            })

        return attrs
