from django.db import transaction
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from jobs.models import (
    Company,
    JobOffer,
    Application,
    InsurancePartner,
    InsuranceProduct,
    EmploymentInsurance,
    EmploymentEngagement,
    EmploymentContract,
    EmploymentContractAnnex,
)
from datetime import date, timedelta
import json

print("")
print("=" * 70)
print(" NSIKAY - TEST E2E EMPLOI + ASSURANCE + CONTRAT")
print("=" * 70)

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

if not admin:
    raise RuntimeError("Aucun super administrateur disponible.")

client = Client()
client.force_login(admin)


def post(url, payload):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
        follow=True,
    )


try:
    with transaction.atomic():

        print("")
        print("=== 1. CREATION DES DONNEES DE TEST ===")

        company = Company.objects.create(
            name="NSIKAY E2E TEST",
            country="CD",
            city="Kinshasa",
            email="e2e-company@nsikay.test",
            phone="+243000000001",
            administrative_status="VALIDEE",
            certification_status="CERTIFIEE",
            is_verified=True,
            is_active=True,
        )

        partner = InsurancePartner.objects.create(
            name="NSIKAY E2E ASSURANCE",
            legal_name="NSIKAY E2E ASSURANCE SA",
            registration_number="E2E-001",
            country="CD",
            email="e2e-insurance@nsikay.test",
            phone="+243000000002",
            status="CERTIFIE",
            is_active=True,
            certification_date=timezone.now(),
            validated_by=admin,
        )

        product = InsuranceProduct.objects.create(
            partner=partner,
            name="Assurance Emploi E2E",
            description="Test",
            coverage="Emploi",
            duration_months=12,
            price=100,
            currency="EUR",
            status="VALIDE",
            is_active=True,
            validated_by=admin,
        )

        offer = JobOffer.objects.create(
            company=company,
            title="Responsable E2E",
            employment_type="CDI",
            description="Offre test NSIKAY",
            status="BROUILLON",
            country="CD",
            city="Kinshasa",
        )

        application = Application.objects.create(
            offer=offer,
            candidate_name="Candidat E2E",
            candidate_email="candidat@nsikay.test",
            candidate_phone="+243000000003",
            status="ACCEPTEE",
        )

        print("Entreprise :", company.id)
        print("Partenaire assurance :", partner.id)
        print("Produit assurance :", product.id)
        print("Offre :", offer.id)
        print("Candidature :", application.id)

        print("")
        print("=== 2. SECURITE : ENGAGEMENT SANS ASSURANCE ===")

        response = post(
            "/api/jobs/employment/engagements/",
            {
                "application_id": application.id,
                "position_title": offer.title,
                "engagement_date": str(date.today()),
                "start_date": str(date.today() + timedelta(days=7)),
                "work_location": "Kinshasa",
                "salary_amount": "1000.00",
                "salary_currency": "EUR",
            },
        )

        print("HTTP :", response.status_code)
        print("URL finale :", response.request["PATH_INFO"])

        if response.status_code in (200, 201):
            raise AssertionError(
                "ERREUR CRITIQUE : engagement autorise sans assurance validee."
            )

        print("SUCCES : engagement bloque sans assurance validee.")

        print("")
        print("=== 3. CREATION ASSURANCE VALIDEE ===")

        insurance = EmploymentInsurance.objects.create(
            company=company,
            job_offer=offer,
            product=product,
            policy_number="E2E-POLICY-001",
            certificate_reference="E2E-CERT-001",
            coverage_start=date.today(),
            coverage_end=date.today() + timedelta(days=365),
            status="VALIDEE",
            verified_by=admin,
        )

        print("Assurance :", insurance.id)
        print("Statut :", insurance.status)

        print("")
        print("=== 4. CREATION ENGAGEMENT ===")

        response = post(
            "/api/jobs/employment/engagements/",
            {
                "application_id": application.id,
                "position_title": offer.title,
                "engagement_date": str(date.today()),
                "start_date": str(date.today() + timedelta(days=7)),
                "work_location": "Kinshasa",
                "salary_amount": "1000.00",
                "salary_currency": "EUR",
            },
        )

        print("HTTP :", response.status_code)
        print("URL finale :", response.request["PATH_INFO"])

        if response.status_code not in (200, 201):
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Creation engagement impossible.")

        engagement = EmploymentEngagement.objects.latest("id")

        print("Engagement :", engagement.id)
        print("Statut :", engagement.status)

        print("")
        print("=== 5. VALIDATION ENGAGEMENT ===")

        response = post(
            f"/api/jobs/employment/engagements/{engagement.id}/validate/",
            {"action": "VALIDER"},
        )

        print("HTTP :", response.status_code)

        if response.status_code != 200:
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Validation engagement impossible.")

        engagement.refresh_from_db()

        print("Statut :", engagement.status)

        if engagement.status != "ENGAGE":
            raise AssertionError("Engagement non valide.")

        print("SUCCES : engagement valide.")

        print("")
        print("=== 6. CREATION CONTRAT ===")

        response = post(
            "/api/jobs/employment/contracts/",
            {
                "engagement_id": engagement.id,
                "contract_type": "CDI",
                "title": offer.title,
                "start_date": str(date.today() + timedelta(days=7)),
                "salary_amount": "1000.00",
                "salary_currency": "EUR",
            },
        )

        print("HTTP :", response.status_code)

        if response.status_code not in (200, 201):
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Creation contrat impossible.")

        contract = EmploymentContract.objects.latest("id")

        print("Contrat :", contract.id)
        print("Numero :", contract.contract_number)
        print("Statut :", contract.status)

        print("")
        print("=== 7. CREATION ANNEXE OBLIGATOIRE ===")

        response = post(
            f"/api/jobs/employment/contracts/{contract.id}/annexes/",
            {
                "title": "Annexe obligatoire E2E",
                "description": "Annexe de test",
                "is_required": True,
            },
        )

        print("HTTP :", response.status_code)

        if response.status_code not in (200, 201):
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Creation annexe impossible.")

        annex = EmploymentContractAnnex.objects.latest("id")

        print("Annexe :", annex.id)
        print("Statut :", annex.status)

        print("")
        print("=== 8. SECURITE : CONTRAT SANS ANNEXE VALIDEE ===")

        response = post(
            f"/api/jobs/employment/contracts/{contract.id}/validate/",
            {"action": "VALIDER"},
        )

        print("HTTP :", response.status_code)

        if response.status_code == 200:
            raise AssertionError(
                "ERREUR CRITIQUE : contrat valide sans annexe validee."
            )

        print("SUCCES : contrat bloque sans annexe validee.")

        print("")
        print("=== 9. VALIDATION ANNEXE ===")

        response = post(
            f"/api/jobs/employment/annexes/{annex.id}/validate/",
            {"action": "VALIDER"},
        )

        print("HTTP :", response.status_code)

        if response.status_code != 200:
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Validation annexe impossible.")

        annex.refresh_from_db()

        print("Statut :", annex.status)

        if annex.status != "VALIDEE":
            raise AssertionError("Annexe non validee.")

        print("SUCCES : annexe validee.")

        print("")
        print("=== 10. VALIDATION CONTRAT ===")

        response = post(
            f"/api/jobs/employment/contracts/{contract.id}/validate/",
            {"action": "VALIDER"},
        )

        print("HTTP :", response.status_code)

        if response.status_code != 200:
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError("Validation contrat impossible.")

        contract.refresh_from_db()

        print("Statut :", contract.status)

        if contract.status != "EN_ATTENTE_TRAVAILLEUR":
            raise AssertionError(
                "Contrat non place en attente du travailleur."
            )

        print("SUCCES : contrat valide.")

        print("")
        print("=== 11. ACCEPTATION PAR LE TRAVAILLEUR ===")

        response = post(
            f"/api/jobs/employment/contracts/accept/{contract.worker_acceptance_token}/",
            {
                "accept": True,
                "note": "Contrat accepte E2E.",
            },
        )

        print("HTTP :", response.status_code)

        if response.status_code != 200:
            print("REPONSE :", response.content.decode(errors="ignore"))
            raise AssertionError(
                "Acceptation travailleur impossible."
            )

        contract.refresh_from_db()
        engagement.refresh_from_db()

        print("Contrat :", contract.status)
        print("Engagement :", engagement.status)

        if contract.status != "ACCEPTE_TRAVAILLEUR":
            raise AssertionError(
                "Contrat non accepte par le travailleur."
            )

        if engagement.status != "ENGAGE":
            raise AssertionError(
                "Engagement incorrect apres acceptation."
            )

        print("SUCCES : travailleur accepte le contrat.")

        print("")
        print("=== 12. VERIFICATION FINALE ===")

        assert insurance.status == "VALIDEE"
        assert insurance.job_offer_id == offer.id
        assert engagement.application_id == application.id
        assert contract.engagement_id == engagement.id
        assert annex.contract_id == contract.id

        print("Assurance -> Offre        : OK")
        print("Offre -> Candidature      : OK")
        print("Candidature -> Engagement : OK")
        print("Engagement -> Contrat     : OK")
        print("Contrat -> Annexes        : OK")
        print("Annexe -> Validation      : OK")
        print("Contrat -> Travailleur    : OK")

        print("")
        print("=" * 70)
        print(" TEST E2E GLOBAL : SUCCES")
        print("=" * 70)
        print("")
        print("ROLLBACK AUTOMATIQUE EN FIN DE TEST.")
        print("")

        raise RuntimeError("__ROLLBACK_NSikay_E2E__")


except RuntimeError as exc:

    if str(exc) == "__ROLLBACK_NSikay_E2E__":
        print("ROLLBACK AUTOMATIQUE : OK")
        print("Aucune donnee de test conservee.")
        print("PowerShell reste ouvert.")
    else:
        raise

except Exception as exc:

    print("")
    print("=" * 70)
    print(" TEST E2E : ECHEC")
    print("=" * 70)
    print(type(exc).__name__, ":", exc)
    print("")
    print("PowerShell reste ouvert.")
    raise
