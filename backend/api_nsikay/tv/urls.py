from django.urls import path

from .views import TVListAPIView


urlpatterns=[

    path(
        "channels/",
        TVListAPIView.as_view(),
        name="tv-channels"
    ),

]

