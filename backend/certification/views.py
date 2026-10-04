from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import (
    CertificationAgent,
    FieldInspection,
    CertificationCertificate
)


def assign_agent(request, inspection_id, agent_id):

    inspection = get_object_or_404(
        FieldInspection,
        id=inspection_id
    )

    agent = get_object_or_404(
        CertificationAgent,
        id=agent_id
    )

    inspection.agent = agent
    inspection.status = "assigned"
    inspection.save()

    return JsonResponse({

        "message":
        "Agent NSIKAY affecté",

        "agent":
        agent.name

    })



def submit_inspection(request, inspection_id):

    inspection = get_object_or_404(
        FieldInspection,
        id=inspection_id
    )

    inspection.status = "submitted"

    inspection.save()


    return JsonResponse({

        "message":
        "Rapport transmis à l'administration"

    })



def approve_certification(request, inspection_id):

    inspection = get_object_or_404(
        FieldInspection,
        id=inspection_id
    )


    inspection.status = "approved"

    inspection.save()


    certificate = CertificationCertificate.objects.create(

        inspection=inspection,

        certificate_number=
        "NSK-CERT-" + str(inspection.id)

    )


    return JsonResponse({

        "message":
        "Certification officielle créée",

        "certificate":
        certificate.certificate_number

    })

