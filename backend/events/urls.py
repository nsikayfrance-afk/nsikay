from rest_framework.routers import DefaultRouter

from .views import (
    EventViewSet,
    EventTicketViewSet,
    EventRegistrationViewSet,
    EventMediaLinkViewSet,
)

router = DefaultRouter()

router.register(
    r"events",
    EventViewSet,
    basename="event",
)

router.register(
    r"tickets",
    EventTicketViewSet,
    basename="event-ticket",
)

router.register(
    r"registrations",
    EventRegistrationViewSet,
    basename="event-registration",
)

router.register(
    r"media-links",
    EventMediaLinkViewSet,
    basename="event-media-link",
)

urlpatterns = router.urls
