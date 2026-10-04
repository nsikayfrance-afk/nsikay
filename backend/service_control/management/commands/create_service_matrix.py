from django.core.management.base import BaseCommand
from service_control.models import GlobalService, CountryServiceStatus, ServiceActivation


class Command(BaseCommand):
    help = "Création de la matrice complète Services x Pays NSIKAY"

    def handle(self, *args, **options):

        services = list(GlobalService.objects.all())
        countries = list(CountryServiceStatus.objects.all())

        if not services:
            self.stdout.write(self.style.ERROR(
                "Aucun service GlobalService trouvé."
            ))
            return

        if not countries:
            self.stdout.write(self.style.ERROR(
                "Aucun pays CountryServiceStatus trouvé."
            ))
            return

        created = 0
        existing = 0

        for service in services:
            for country in countries:

                activation, was_created = ServiceActivation.objects.get_or_create(
                    service=service,
                    country=country,
                    defaults={
                        "active": False,
                        "reason": "En attente validation administration NSIKAY",
                        "validated_by_admin": False,
                    }
                )

                if was_created:
                    created += 1
                else:
                    existing += 1

        total = ServiceActivation.objects.count()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            "=== MATRICE SERVICES x PAYS NSIKAY ==="
        ))
        self.stdout.write(f"Services : {len(services)}")
        self.stdout.write(f"Pays : {len(countries)}")
        self.stdout.write(f"Lignes creees : {created}")
        self.stdout.write(f"Lignes deja existantes : {existing}")
        self.stdout.write(f"Total matrice : {total}")
        self.stdout.write("")
        self.stdout.write(
            "Toutes les activations restent DESACTIVEES jusqu'a "
            "validation de l'administration."
        )

