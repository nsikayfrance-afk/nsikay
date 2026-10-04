from django.contrib import admin
from .models import (
    MediaContent,
    TVChannel,
    TVProgram,
    Event,
    EventRegistration
)

admin.site.register(MediaContent)
admin.site.register(TVChannel)
admin.site.register(TVProgram)
admin.site.register(Event)
admin.site.register(EventRegistration)

