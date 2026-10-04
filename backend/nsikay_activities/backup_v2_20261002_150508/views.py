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
        ).select_related("activity", "activity__profile")


class ServiceDetailView(
    UserActivityMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity", "activity__profile")


class ProjectListCreateView(
    UserActivityMixin,
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity", "activity__profile")


class ProjectDetailView(
    UserActivityMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            activity__profile_id__in=self.get_user_profile_ids()
        ).select_related("activity", "activity__profile")
