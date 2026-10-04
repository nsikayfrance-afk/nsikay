from django.core.management.base import BaseCommand
from service_control.models import CountryServiceStatus
import pycountry


class Command(BaseCommand):

    help = "Charge les 240 pays NSIKAY"

    def handle(self, *args, **kwargs):

        count = 0

        for country in pycountry.countries:

            code = country.alpha_3
            name = country.name

            CountryServiceStatus.objects.get_or_create(
                country_code=code,
                country_name=name
            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Pays charges : {count}"
            )
        )

