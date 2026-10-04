from django.db.models import Q
from django.utils import timezone

from .models import FinancialRoutingRule


def resolve_financial_route(
    source_type,
    country_code="",
    currency_code="",
    operation_type="REVENUE",
):
    """
    Recherche la règle active la plus précise.

    Priorité :
    1. pays + devise
    2. pays seul
    3. règle internationale + devise
    4. règle internationale générale

    Une règle doit être APPROVED et active.
    """

    now = timezone.now()

    queryset = FinancialRoutingRule.objects.filter(
        source_type=source_type,
        operation_type=operation_type,
        active=True,
        status="APPROVED",
    ).filter(
        Q(valid_from__isnull=True) | Q(valid_from__lte=now),
        Q(valid_until__isnull=True) | Q(valid_until__gte=now),
    )

    candidates = list(queryset)

    def score(rule):
        points = 0

        if country_code and rule.country_code.upper() == country_code.upper():
            points += 100

        if currency_code and rule.currency_code.upper() == currency_code.upper():
            points += 50

        if not rule.country_code:
            points += 10

        if not rule.currency_code:
            points += 5

        points -= rule.priority

        return points

    candidates.sort(key=score, reverse=True)

    return candidates[0] if candidates else None
