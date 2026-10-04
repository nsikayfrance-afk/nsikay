from django.core.management.base import BaseCommand
from django.db import transaction
from service_control.models import GlobalService, CountryServiceStatus, ServiceActivation


class Command(BaseCommand):
    help = "Complete rapidement la matrice Services x Pays NSIKAY"

    def handle(self, *args, **options):

        services = list(GlobalService.objects.values_list("id", flat=True))
        countries = list(CountryServiceStatus.objects.values_list("id", flat=True))

        expected = len(services) * len(countries)

        existing = set(
            ServiceActivation.objects.values_list(
                "service_id",
                "country_id"
            )
        )

        missing = []

        for service_id in services:
            for country_id in countries:

                if (service_id, country_id) not in existing:

                    missing.append(
                        ServiceActivation(
                            service_id=service_id,
                            country_id=country_id,
                            active=False,
                            reason="En attente validation administration NSIKAY",
                            validated_by_admin=False
                        )
                    )

        self.stdout.write(f"Services : {len(services)}")
        self.stdout.write(f"Pays : {len(countries)}")
        self.stdout.write(f"Relations existantes : {len(existing)}")
        self.stdout.write(f"Relations manquantes : {len(missing)}")
        self.stdout.write(f"Total attendu : {expected}")

        if missing:

            with transaction.atomic():

                ServiceActivation.objects.bulk_create(
                    missing,
                    batch_size=1000
                )

        total = ServiceActivation.objects.count()

        self.stdout.write("")
        self.stdout.write(f"Relations ajoutees : {len(missing)}")
        self.stdout.write(f"Total final : {total}")

        if total == expected:

            self.stdout.write(
                self.style.SUCCESS(
                    "=== MATRICE SERVICES x PAYS COMPLETE ==="
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "Matrice encore incomplete."
                )
            )

