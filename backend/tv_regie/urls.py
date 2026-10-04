from rest_framework.routers import DefaultRouter

from .views import (
    CameraSystemViewSet,
    LiveStreamViewSet,
    VideoEffectViewSet,
    TextAnimationViewSet,
    AudioControlViewSet,
    RegieSceneViewSet,
    BroadcastScheduleViewSet,
    BroadcastViewSet,
)

router = DefaultRouter()

router.register(r"cameras", CameraSystemViewSet, basename="camera")
router.register(r"streams", LiveStreamViewSet, basename="stream")
router.register(r"effects", VideoEffectViewSet, basename="effect")
router.register(r"animations", TextAnimationViewSet, basename="animation")
router.register(r"audio", AudioControlViewSet, basename="audio")
router.register(r"scenes", RegieSceneViewSet, basename="scene")
router.register(r"schedules", BroadcastScheduleViewSet, basename="schedule")
router.register(r"broadcasts", BroadcastViewSet, basename="broadcast")

urlpatterns = router.urls
