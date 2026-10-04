import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import PasswordRecoveryRequest


CODE_LENGTH = 6
CODE_TTL_MINUTES = 10
MAX_ATTEMPTS = 5
REQUEST_WINDOW_MINUTES = 15
MAX_REQUESTS_PER_WINDOW = 3


def _sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def generate_code():
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_code(code):
    return _sha256(code)


def resolve_user(identifier):
    User = get_user_model()

    identifier = (identifier or "").strip()

    if not identifier:
        return None

    user = User.objects.filter(
        email__iexact=identifier
    ).first()

    if user:
        return user

    user = User.objects.filter(
        username__iexact=identifier
    ).first()

    if user:
        return user

    return None


def can_request_recovery(user):
    since = timezone.now() - timedelta(
        minutes=REQUEST_WINDOW_MINUTES
    )

    count = PasswordRecoveryRequest.objects.filter(
        user=user,
        requested_at__gte=since,
    ).count()

    return count < MAX_REQUESTS_PER_WINDOW


def _invalidate_previous_requests(user):
    PasswordRecoveryRequest.objects.filter(
        user=user,
        used=False,
    ).update(
        used=True,
    )


@transaction.atomic
def create_recovery_request(user, ip_address="", user_agent=""):
    if not can_request_recovery(user):
        return None, None

    _invalidate_previous_requests(user)

    code = generate_code()

    request = PasswordRecoveryRequest.objects.create(
        user=user,
        channel=PasswordRecoveryRequest.CHANNEL_EMAIL,
        destination=(user.email or "")[:320],
        code_hash=hash_code(code),
        expires_at=timezone.now()
        + timedelta(minutes=CODE_TTL_MINUTES),
        max_attempts=MAX_ATTEMPTS,
        requested_ip_hash=_sha256(ip_address) if ip_address else "",
        user_agent_hash=_sha256(user_agent) if user_agent else "",
    )

    if user.email:
        send_mail(
            subject="NSIKAY — récupération de votre mot de passe",
            message=(
                "Une demande de récupération de mot de passe "
                "a été effectuée pour votre compte NSIKAY.\n\n"
                f"Votre code temporaire est : {code}\n\n"
                f"Ce code expire dans {CODE_TTL_MINUTES} minutes.\n"
                "Il ne doit pas être communiqué à une autre personne."
            ),
            from_email=getattr(
                settings,
                "DEFAULT_FROM_EMAIL",
                None,
            ),
            recipient_list=[user.email],
            fail_silently=False,
        )

    return request, code


@transaction.atomic
def verify_recovery_code(request, code):
    if not request.is_usable():
        return False

    code = (code or "").strip()

    request.attempts += 1

    if not secrets.compare_digest(
        request.code_hash,
        hash_code(code),
    ):
        request.save(
            update_fields=["attempts"]
        )
        return False

    request.verified_at = timezone.now()

    request.save(
        update_fields=[
            "attempts",
            "verified_at",
        ]
    )

    return True


@transaction.atomic
def reset_password(request, new_password):
    if not request.is_usable():
        raise ValueError(
            "La demande de récupération n'est plus valide."
        )

    validate_password(
        new_password,
        request.user,
    )

    request.user.set_password(new_password)
    request.user.save(
        update_fields=["password"]
    )

    request.used = True
    request.completed_at = timezone.now()

    request.save(
        update_fields=[
            "used",
            "completed_at",
        ]
    )

    # Toutes les autres demandes encore ouvertes deviennent invalides.
    PasswordRecoveryRequest.objects.filter(
        user=request.user,
        used=False,
    ).exclude(
        pk=request.pk,
    ).update(
        used=True,
    )

    return request.user
