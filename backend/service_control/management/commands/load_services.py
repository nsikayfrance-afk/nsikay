from django.core.management.base import BaseCommand
from service_control.models import GlobalService


SERVICES = [

("Entreprise", "Professionnel"),
("Ecole", "Education"),
("Universite", "Education"),
("Centre Formation", "Education"),
("Hopital", "Sante"),
("Telecom", "Reseaux"),
("Banque", "Finance"),
("Assurance", "Finance"),
("Immobilier", "Immobilier"),
("Construction", "Construction"),
("Automobile", "Transport"),
("Transport", "Transport"),
("Justice", "Justice"),
("Emploi", "Emploi"),
("WENZE", "Commerce"),
("Evenements", "Communication"),
("Publicite", "Communication"),
("Reseaux Sociaux", "Social"),
("Video", "Media"),
("Audio", "Media"),
("Sport", "Sport"),
("Musique", "Culture"),
("Agriculture", "Agriculture"),
("Tourisme", "Tourisme"),
("Technologie", "Technologie"),
("Environnement", "Environnement"),
("Social", "Social"),
("Religion Histoire Culture", "Culture"),

]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for name, category in SERVICES:

            GlobalService.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "active_global": True
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Services NSIKAY charges correctement"
            )
        )

