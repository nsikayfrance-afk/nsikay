from django.db import transaction
from rest_framework import serializers

from .models import Activity, Service, Project
from .rules import get_activity_rule
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
            "certification_required",
            "certification_status",
            "service_count",
            "project_count",
            "created_at",
            "updated_at",
        ]

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

    def _validate_rule_fields(self, attrs, activity_type):
        rule = get_activity_rule(activity_type)

        if rule is None:
            raise serializers.ValidationError({
                "activity_type": (
                    "Ce type d'activité ne possède aucune règle NSIKAY."
                )
            })

        errors = {}

        # En creation, les valeurs sont dans attrs.
        # En modification partielle, on complete avec l'instance.
        for field_name in rule.mandatory_fields:
            value = attrs.get(field_name)

            if value is None and self.instance is not None:
                value = getattr(self.instance, field_name, None)

            if value is None or not str(value).strip():
                errors[field_name] = (
                    f"Le champ '{field_name}' est obligatoire "
                    f"pour une activité de type '{rule.label}'."
                )

        if errors:
            raise serializers.ValidationError(errors)

        return rule

    def validate(self, attrs):
        name = attrs.get("name")

        if name is not None and not str(name).strip():
            raise serializers.ValidationError({
                "name": "Le nom de l'activité est obligatoire."
            })

        # --------------------------------------------------------
        # TYPE
        # --------------------------------------------------------

        if self.instance is not None:
            activity_type = attrs.get(
                "activity_type",
                self.instance.activity_type,
            )
        else:
            activity_type = attrs.get("activity_type")

        if not activity_type:
            raise serializers.ValidationError({
                "activity_type": "Le type d'activité est obligatoire."
            })

        rule = self._validate_rule_fields(
            attrs,
            activity_type,
        )

        # --------------------------------------------------------
        # LE TYPE D'ACTIVITE EST IMMUTABLE APRES CREATION
        # --------------------------------------------------------

        if (
            self.instance is not None
            and "activity_type" in attrs
            and attrs["activity_type"] != self.instance.activity_type
        ):
            raise serializers.ValidationError({
                "activity_type": (
                    "Le type d'une activité existante ne peut pas être "
                    "modifié directement. Créez une nouvelle activité "
                    "ou utilisez le processus de reclassification NSIKAY."
                )
            })

        # --------------------------------------------------------
        # REVendeur DE CADEAUX
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # ACTIVATION
        # --------------------------------------------------------

        requested_status = attrs.get("status")

        # --------------------------------------------------------
        # CREATION :
        # Une activité certifiable est toujours créée en brouillon.
        # La demande "active" est donc transformée en "draft".
        # Le contrôle d'activation intervient ensuite lors d'une
        # véritable modification d'une activité existante.
        # --------------------------------------------------------

        if (
            self.instance is None
            and requested_status == "active"
            and rule.activation_requires_certification
        ):
            attrs["status"] = "draft"

        # --------------------------------------------------------
        # MODIFICATION :
        # Une activité existante ne peut passer à active qu'après
        # certification NSIKAY.
        # --------------------------------------------------------

        if (
            self.instance is not None
            and requested_status == "active"
            and rule.activation_requires_certification
        ):
            current_cert_status = (
                getattr(
                    self.instance,
                    "certification_status",
                    "not_required",
                )
            )

            if current_cert_status != "certified":
                raise serializers.ValidationError({
                    "status": (
                        f"L'activité '{rule.label}' ne peut pas être "
                        "activée avant sa certification NSIKAY."
                    )
                })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        # --------------------------------------------------------
        # PROFIL PERSONNEL PRINCIPAL
        # --------------------------------------------------------

        profile = self._get_primary_profile()

        validated_data["profile"] = profile

        activity_type = validated_data.get("activity_type")

        rule = get_activity_rule(activity_type)

        if rule is None:
            raise serializers.ValidationError({
                "activity_type": (
                    "Ce type d'activité ne possède aucune règle NSIKAY."
                )
            })

        # --------------------------------------------------------
        # VALEURS CONTROLEES PAR LE MOTEUR
        # --------------------------------------------------------

        validated_data["certification_required"] = (
            rule.certification_required
        )

        if rule.certification_required:
            validated_data["certification_status"] = "pending"
        else:
            validated_data["certification_status"] = "not_required"

        # Une nouvelle activité certifiable démarre en brouillon.
        if rule.activation_requires_certification:
            validated_data["status"] = "draft"

        activity = Activity.objects.create(
            **validated_data
        )

        # --------------------------------------------------------
        # REVENDEUR DE CADEAUX
        # --------------------------------------------------------

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
        # --------------------------------------------------------
        # IMMUTABILITE DU PROFIL
        # --------------------------------------------------------

        validated_data.pop("profile", None)

        # --------------------------------------------------------
        # IMMUTABILITE DU TYPE
        # --------------------------------------------------------

        validated_data.pop(
            "activity_type",
            None,
        )

        # --------------------------------------------------------
        # CERTIFICATION CONTROLEE PAR NSIKAY
        # --------------------------------------------------------

        validated_data.pop(
            "certification_required",
            None,
        )

        validated_data.pop(
            "certification_status",
            None,
        )

        rule = get_activity_rule(
            instance.activity_type
        )

        if rule is None:
            raise serializers.ValidationError({
                "activity_type": (
                    "Cette activité ne possède aucune règle NSIKAY."
                )
            })

        requested_status = validated_data.get("status")

        if requested_status == "active":
            if rule.activation_requires_certification:
                if instance.certification_status != "certified":
                    raise serializers.ValidationError({
                        "status": (
                            f"L'activité '{rule.label}' ne peut pas être "
                            "activée avant sa certification NSIKAY."
                        )
                    })

        # La règle reste la source de vérité pour ce champ.
        validated_data["certification_required"] = (
            rule.certification_required
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

