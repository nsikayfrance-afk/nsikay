from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone

from service_control.models import CountryServiceStatus

from .models import (
    OperationalCountryConfigurationLog,
    OperationalCountryConfigurationSnapshot,
)


def _is_nsikay_admin(user):
    if not user or not user.is_authenticated:
        return False

    username = str(user.username).strip().lower()

    if username == "constantdoriskayembe":
        return True

    return (
        user.is_superuser
        or user.groups.filter(
            name__in=[
                "Super Administrateur",
                "Administration Pays",
            ]
        ).exists()
    )


@user_passes_test(_is_nsikay_admin)
def operational_countries(request):

    countries = (
        CountryServiceStatus.objects
        .filter(is_primary=True)
        .order_by("country_name")
    )

    if request.method == "POST":

        selected_codes = [
            str(code).strip().upper()
            for code in request.POST.getlist("countries")
            if str(code).strip()
        ]

        selected_codes = sorted(set(selected_codes))

        if len(selected_codes) != 240:
            messages.error(
                request,
                (
                    "La configuration NSIKAY doit contenir exactement "
                    f"240 pays opérationnels. Sélection actuelle : "
                    f"{len(selected_codes)}."
                ),
            )

            return render(
                request,
                "service_dashboard/operational_countries.html",
                {
                    "countries": countries,
                    "operational_count": CountryServiceStatus.objects.filter(
                        is_primary=True,
                        is_operational=True,
                    ).count(),
                    "selected_count": len(selected_codes),
                    "limit": 240,
                    "remaining_slots": max(
                        240 - len(selected_codes),
                        0,
                    ),
                },
            )

        with transaction.atomic():

            # -------------------------------------------------
            # VERROUILLAGE DES 249 PAYS PRINCIPAUX
            # -------------------------------------------------

            locked_countries = list(
                CountryServiceStatus.objects
                .select_for_update()
                .filter(is_primary=True)
                .order_by("country_code")
            )

            if len(locked_countries) != 249:
                raise ValueError(
                    "Configuration interrompue : le nombre de pays "
                    f"principaux est {len(locked_countries)} au lieu de 249."
                )

            # -------------------------------------------------
            # ETAT PRECEDENT
            # -------------------------------------------------

            previous_codes = sorted(
                country.country_code.strip().upper()
                for country in locked_countries
                if country.is_operational
            )

            previous_count = len(previous_codes)

            # -------------------------------------------------
            # CREATION DU JOURNAL
            # -------------------------------------------------

            admin_username = (
                request.user.get_username()
                if request.user.is_authenticated
                else "system"
            )

            configuration_log = (
                OperationalCountryConfigurationLog.objects.create(
                    selected_count=len(selected_codes),
                    selected_codes=",".join(selected_codes),
                    action="configuration_officielle_240_pays",
                    admin_user=admin_username,
                )
            )

            # -------------------------------------------------
            # CREATION DU SNAPSHOT AVANT MODIFICATION
            # -------------------------------------------------

            OperationalCountryConfigurationSnapshot.objects.create(
                configuration_log=configuration_log,
                previous_operational_codes=",".join(previous_codes),
                previous_operational_count=previous_count,
            )

            # -------------------------------------------------
            # APPLICATION DE LA NOUVELLE CONFIGURATION
            # -------------------------------------------------

            CountryServiceStatus.objects.filter(
                is_primary=True
            ).update(
                is_operational=False
            )

            CountryServiceStatus.objects.filter(
                is_primary=True,
                country_code__in=selected_codes,
            ).update(
                is_operational=True
            )

            # -------------------------------------------------
            # VERIFICATION STRICTE
            # -------------------------------------------------

            operational_count = (
                CountryServiceStatus.objects
                .filter(
                    is_primary=True,
                    is_operational=True,
                )
                .count()
            )

            if operational_count != 240:
                raise ValueError(
                    "Configuration interrompue : le nombre final de pays "
                    f"opérationnels est {operational_count} au lieu de 240."
                )

            # -------------------------------------------------
            # VERIFICATION DES CODES SELECTIONNES
            # -------------------------------------------------

            final_codes = sorted(
                CountryServiceStatus.objects
                .filter(
                    is_primary=True,
                    is_operational=True,
                )
                .values_list(
                    "country_code",
                    flat=True,
                )
            )

            if final_codes != selected_codes:
                raise ValueError(
                    "Configuration interrompue : les codes pays finaux "
                    "ne correspondent pas exactement à la sélection."
                )

        messages.success(
            request,
            (
                "Configuration des 240 pays enregistrée avec succès. "
                "Un snapshot de l'état précédent a été créé."
            ),
        )

        return redirect(
            "service_dashboard:operational_countries"
        )

    operational_count = (
        CountryServiceStatus.objects
        .filter(
            is_primary=True,
            is_operational=True,
        )
        .count()
    )

    return render(
        request,
        "service_dashboard/operational_countries.html",
        {
            "countries": countries,
            "operational_count": operational_count,
            "selected_count": operational_count,
            "limit": 240,
            "remaining_slots": max(
                240 - operational_count,
                0,
            ),
        },
    )


@user_passes_test(_is_nsikay_admin)
def rollback_last_configuration(request):

    if request.method != "POST":
        messages.error(
            request,
            "Le rollback doit être effectué par une requête POST.",
        )

        return redirect(
            "service_dashboard:operational_countries_history"
        )

    with transaction.atomic():

        # -----------------------------------------------------
        # VERROUILLAGE DU DERNIER JOURNAL ANNULABLE
        # -----------------------------------------------------

        log = (
            OperationalCountryConfigurationLog.objects
            .select_for_update()
            .filter(
                action="configuration_officielle_240_pays",
                rolled_back=False,
            )
            .order_by("-created_at")
            .first()
        )

        if not log:
            messages.error(
                request,
                "Aucune configuration officielle annulable n'a été trouvée.",
            )

            return redirect(
                "service_dashboard:operational_countries_history"
            )

        # -----------------------------------------------------
        # SNAPSHOT OBLIGATOIRE
        # -----------------------------------------------------

        snapshot = (
            OperationalCountryConfigurationSnapshot.objects
            .select_for_update()
            .filter(configuration_log=log)
            .first()
        )

        if not snapshot:
            raise ValueError(
                "Rollback interrompu : le snapshot est introuvable."
            )

        # -----------------------------------------------------
        # VERROUILLAGE DES PAYS
        # -----------------------------------------------------

        countries = list(
            CountryServiceStatus.objects
            .select_for_update()
            .filter(is_primary=True)
        )

        if len(countries) != 249:
            raise ValueError(
                "Rollback interrompu : le nombre de pays principaux "
                f"est {len(countries)} au lieu de 249."
            )

        # -----------------------------------------------------
        # CODES PRECEDENTS
        # -----------------------------------------------------

        previous_codes = sorted(
            code.strip().upper()
            for code in snapshot.previous_operational_codes.split(",")
            if code.strip()
        )

        if len(previous_codes) != snapshot.previous_operational_count:
            raise ValueError(
                "Rollback interrompu : le snapshot est incohérent."
            )

        # -----------------------------------------------------
        # RESTAURATION
        # -----------------------------------------------------

        CountryServiceStatus.objects.filter(
            is_primary=True
        ).update(
            is_operational=False
        )

        if previous_codes:
            CountryServiceStatus.objects.filter(
                is_primary=True,
                country_code__in=previous_codes,
            ).update(
                is_operational=True
            )

        restored_count = (
            CountryServiceStatus.objects
            .filter(
                is_primary=True,
                is_operational=True,
            )
            .count()
        )

        if restored_count != snapshot.previous_operational_count:
            raise ValueError(
                "Rollback interrompu : le nombre restauré "
                f"({restored_count}) ne correspond pas au snapshot "
                f"({snapshot.previous_operational_count})."
            )

        # -----------------------------------------------------
        # VERIFICATION DES CODES RESTAURES
        # -----------------------------------------------------

        restored_codes = sorted(
            CountryServiceStatus.objects
            .filter(
                is_primary=True,
                is_operational=True,
            )
            .values_list(
                "country_code",
                flat=True,
            )
        )

        if restored_codes != previous_codes:
            raise ValueError(
                "Rollback interrompu : les pays restaurés "
                "ne correspondent pas au snapshot."
            )

        # -----------------------------------------------------
        # MARQUAGE DU ROLLBACK
        # -----------------------------------------------------

        log.rolled_back = True
        log.rolled_back_at = timezone.now()
        log.rolled_back_by = (
            request.user.get_username()
            if request.user.is_authenticated
            else "system"
        )
        log.rollback_reason = (
            "Annulation de la dernière configuration officielle "
            "des 240 pays avec restauration du snapshot précédent."
        )

        log.save(
            update_fields=[
                "rolled_back",
                "rolled_back_at",
                "rolled_back_by",
                "rollback_reason",
            ]
        )

    messages.success(
        request,
        (
            "La dernière configuration officielle a été annulée. "
            "Le snapshot précédent a été restauré."
        ),
    )

    return redirect(
        "service_dashboard:operational_countries_history"
    )

