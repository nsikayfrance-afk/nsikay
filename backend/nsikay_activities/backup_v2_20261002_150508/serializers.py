from rest_framework import serializers

from .models import Activity, Service, Project


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = [
            "id",
            "activity",
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
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_activity(self, activity):
        request = self.context.get("request")

        if request and not activity.profile.user_id == request.user.id:
            raise serializers.ValidationError(
                "Cette activité n'appartient pas à l'utilisateur."
            )

        return activity


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id",
            "activity",
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_activity(self, activity):
        request = self.context.get("request")

        if request and not activity.profile.user_id == request.user.id:
            raise serializers.ValidationError(
                "Cette activité n'appartient pas à l'utilisateur."
            )

        return activity


class ActivitySerializer(serializers.ModelSerializer):

    services_count = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "profile",
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
            "services_count",
            "projects_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "services_count",
            "projects_count",
        ]

    def validate_profile(self, profile):
        request = self.context.get("request")

        if request and profile.user_id != request.user.id:
            raise serializers.ValidationError(
                "Ce profil n'appartient pas à l'utilisateur."
            )

        return profile

    def get_services_count(self, obj):
        return obj.services.count()

    def get_projects_count(self, obj):
        return obj.projects.count()
