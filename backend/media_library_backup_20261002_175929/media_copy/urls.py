from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MediaContentViewSet,
    TVChannelViewSet,
    TVProgramViewSet,
    EventViewSet,
    EventRegistrationViewSet
)

router = DefaultRouter()

router.register('contents', MediaContentViewSet)
router.register('channels', TVChannelViewSet)
router.register('programs', TVProgramViewSet)
router.register('events', EventViewSet)
router.register('registrations', EventRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

