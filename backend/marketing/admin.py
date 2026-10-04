from django.contrib import admin
from .models import (
    Advertiser,
    AdvertisingCampaign,
    AdvertisementPlacement,
    Advertisement,
    AdvertisementStatistic
)

admin.site.register(Advertiser)
admin.site.register(AdvertisingCampaign)
admin.site.register(AdvertisementPlacement)
admin.site.register(Advertisement)
admin.site.register(AdvertisementStatistic)

