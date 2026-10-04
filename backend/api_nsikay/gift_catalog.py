from decimal import Decimal
from django.apps import apps


REFERENCE_CURRENCY = "EUR"
SUPPORTED_DISPLAY_CURRENCIES = ("EUR", "USD", "CDF")


def _field_names(model):
    return {field.name for field in model._meta.fields}


def get_exchange_rate(target_currency):
    """
    Retourne le taux EUR -> devise cible depuis finance.ExchangeRate.

    La structure existante du modele ExchangeRate pouvant evoluer,
    le service detecte les noms de champs usuels au lieu de figer
    une structure non verifiee.
    """

    target_currency = str(target_currency).upper()

    if target_currency == REFERENCE_CURRENCY:
        return Decimal("1")

    ExchangeRate = apps.get_model("finance", "ExchangeRate")
    fields = _field_names(ExchangeRate)

    source_names = [
        "base_currency",
        "from_currency",
        "source_currency",
        "currency_from",
    ]

    target_names = [
        "target_currency",
        "to_currency",
        "destination_currency",
        "currency_to",
    ]

    rate_names = [
        "rate",
        "exchange_rate",
        "value",
        "rate_value",
    ]

    source_field = next(
        (name for name in source_names if name in fields),
        None
    )

    target_field = next(
        (name for name in target_names if name in fields),
        None
    )

    rate_field = next(
        (name for name in rate_names if name in fields),
        None
    )

    if not source_field or not target_field or not rate_field:
        raise LookupError(
            "Structure ExchangeRate incompatible avec le service "
            "de conversion EUR -> devise principale."
        )

    queryset = ExchangeRate.objects.all()

    source_value = "EUR"
    target_value = target_currency

    queryset = queryset.filter(
        **{
            source_field: source_value,
            target_field: target_value,
        }
    )

    row = queryset.order_by("-id").first()

    if row is None:
        raise LookupError(
            f"Taux EUR -> {target_currency} introuvable."
        )

    rate = Decimal(str(getattr(row, rate_field)))

    if rate <= 0:
        raise ValueError(
            f"Taux EUR -> {target_currency} invalide."
        )

    return rate


def convert_gift_value(value_eur, target_currency):
    """
    Convertit une valeur catalogue EUR vers la devise principale
    de l'utilisateur.
    """

    value_eur = Decimal(str(value_eur))
    target_currency = str(target_currency).upper()

    if target_currency not in SUPPORTED_DISPLAY_CURRENCIES:
        raise ValueError(
            f"Devise d'affichage non prise en charge : {target_currency}"
        )

    rate = get_exchange_rate(target_currency)

    return {
        "currency": target_currency,
        "value": (value_eur * rate).quantize(Decimal("0.01")),
        "reference_currency": "EUR",
        "reference_value": value_eur,
        "rate": rate,
    }
