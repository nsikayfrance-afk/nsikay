from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import (
    CameraSystem,
    LiveStream,
    RegieScene,
    BroadcastSchedule,
)


@login_required
def tv_regie_dashboard(request):

    context = {
        "cameras": CameraSystem.objects.all(),
        "streams": LiveStream.objects.all(),
        "scenes": RegieScene.objects.all(),
        "schedules": BroadcastSchedule.objects.all(),
    }

    return render(
        request,
        "tv_regie/dashboard.html",
        context
    )

