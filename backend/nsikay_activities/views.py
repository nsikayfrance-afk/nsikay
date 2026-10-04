from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, Service, Project
from .serializers import (
    ActivitySerializer,
    ServiceSerializer,
    ProjectSerializer,
)


class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Activity.objects
            .filter(profile__user=user)
            .select_related("profile")
            .prefetch_related("services", "projects")
            .order_by("-updated_at", "-id")
        )

        profile_id = self.request.query_params.get("profile")
        activity_type = self.request.query_params.get("activity_type")
        status = self.request.query_params.get("status")
        search = self.request.query_params.get("q")

        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        if status:
            queryset = queryset.filter(status=status)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(sector__icontains=search)
                | Q(city__icontains=search)
                | Q(country__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Activity.objects
            .filter(profile__user=self.request.user)
            .select_related("profile")
            .prefetch_related("services", "projects")
        )


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Service.objects
            .filter(activity__profile__user=self.request.user)
            .select_related("activity", "activity__profile")
            .order_by("-updated_at", "-id")
        )

        activity_id = self.request.query_params.get("activity")
        status = self.request.query_params.get("status")
        search = self.request.query_params.get("q")

        if activity_id:
            queryset = queryset.filter(activity_id=activity_id)

        if status:
            queryset = queryset.filter(status=status)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(category__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Service.objects
            .filter(activity__profile__user=self.request.user)
            .select_related("activity", "activity__profile")
        )


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Project.objects
            .filter(activity__profile__user=self.request.user)
            .select_related("activity", "activity__profile")
            .order_by("-updated_at", "-id")
        )

        activity_id = self.request.query_params.get("activity")
        status = self.request.query_params.get("status")
        search = self.request.query_params.get("q")

        if activity_id:
            queryset = queryset.filter(activity_id=activity_id)

        if status:
            queryset = queryset.filter(status=status)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Project.objects
            .filter(activity__profile__user=self.request.user)
            .select_related("activity", "activity__profile")
        )


class ActivityDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.filter(
            profile__user=request.user
        )

        services = Service.objects.filter(
            activity__profile__user=request.user
        )

        projects = Project.objects.filter(
            activity__profile__user=request.user
        )

        data = {
            "profiles": activities.values("profile_id").distinct().count(),
            "activities": activities.count(),
            "activities_active": activities.filter(
                status="active"
            ).count(),
            "activities_draft": activities.filter(
                status="draft"
            ).count(),
            "activities_suspended": activities.filter(
                status="suspended"
            ).count(),
            "services": services.count(),
            "services_active": services.filter(
                status="active"
            ).count(),
            "projects": projects.count(),
            "projects_active": projects.filter(
                status="active"
            ).count(),
            "projects_planned": projects.filter(
                status="planned"
            ).count(),
            "certification_required": activities.filter(
                certification_required=True
            ).count(),
            "certification_pending": activities.filter(
                certification_status="pending"
            ).count(),
            "certified": activities.filter(
                certification_status="certified"
            ).count(),
        }

        return Response(data)
