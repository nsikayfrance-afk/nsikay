from rest_framework.routers import DefaultRouter

from .views import (, BroadcastViewSet
    CameraSystemViewSet,
    LiveStreamViewSet,
    VideoEffectViewSet,
    TextAnimationViewSet,
    AudioControlViewSet,
    RegieSceneViewSet,
    BroadcastScheduleViewSet,
)

router = DefaultRouter()

router.register("cameras", CameraSystemViewSet)
router.register("broadcasts", BroadcastViewSet, basename="broadcast")
router.register("streams", LiveStreamViewSet)
router.register("effects", VideoEffectViewSet)
router.register("animations", TextAnimationViewSet)
router.register("audio", AudioControlViewSet)
router.register("scenes", RegieSceneViewSet)
router.register("schedules", BroadcastScheduleViewSet)


urlpatterns = router.urls


