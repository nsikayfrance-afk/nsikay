from rest_framework.views import APIView
from rest_framework.response import Response

from media.models import (
    MediaContent,
    Event
)

from marketing.models import (
    AdvertisingCampaign,
    Advertisement,
    AdvertisementStatistic
)


class NsikayMediaMarketingDashboard(APIView):

    def get(self, request):

        data = {
            "media": {
                "contents": MediaContent.objects.count(),
                "events": Event.objects.count(),
            },

            "marketing": {
                "campaigns": AdvertisingCampaign.objects.count(),
                "advertisements": Advertisement.objects.count(),
                "views": sum(
                    AdvertisementStatistic.objects.values_list(
                        'views',
                        flat=True
                    )
                ),
                "clicks": sum(
                    AdvertisementStatistic.objects.values_list(
                        'clicks',
                        flat=True
                    )
                ),
            }
        }

        return Response(data)

