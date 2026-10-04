from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Activity, Service, Project
from .serializers import (
    ActivitySerializer,
    ServiceSerializer,
    ProjectSerializer,
)


class UserActivityMixin:
    def get_user_profile_ids(self):
        return self.request.user.nsikay_profiles.values_list(
            "id",
            flat=True,
        )


class ActivityListCreateView(
    UserActivityMixin,
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(
            profile_id__in=self.get_user_profile_ids()
        ).select_related("profile")

    def perform_create(self, serializer):
        profile_id = self.request.data.get("profile")

        if not profile_id:
            raise ValueError(
                "Le profil NSIKAY est obligatoire."
            )

        if not self.request.user.nsikay_profiles.filter(
            id=profile_id
        ).exists():
            raise ValueError(
                "Ce profil n'appartient pas à l'utilisateur."
            )

        serializer.save()


class ActivityDetailView(
    UserActivityMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(
            profile_id__in=self.get_user_profile_ids()
        ).select_related("profile")


class ServiceListCreateView(
    UserActivityMixin,
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity")

    def perform_create(self, serializer):
        activity_id = self.request.data.get("activity")

        if not activity_id:
            raise ValueError(
                "L'activité est obligatoire."
            )

        if not Activity.objects.filter(
            id=activity_id,
            profile_id__in=self.get_user_profile_ids(),
        ).exists():
            raise ValueError(
                "Cette activité n'appartient pas à l'utilisateur."
            )

        serializer.save()


class ServiceDetailView(
    UserActivityMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity")


class ProjectListCreateView(
    UserActivityMixin,
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity")

    def perform_create(self, serializer):
        activity_id = self.request.data.get("activity")

        if not activity_id:
            raise ValueError(
                "L'activité est obligatoire."
            )

        if not Activity.objects.filter(
            id=activity_id,
            profile_id__in=self.get_user_profile_ids(),
        ).exists():
            raise ValueError(
                "Cette activité n'appartient pas à l'utilisateur."
            )

        serializer.save()


class ProjectDetailView(
    UserActivityMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity")
