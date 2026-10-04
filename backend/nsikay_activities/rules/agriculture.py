from .base import ActivityRule


RULE = ActivityRule(
    activity_type="agriculture",
    label="Agriculture",
    certification_required=True,
    activation_requires_certification=True,
    mandatory_fields=(
        "name",
        "country",
        "city",
        "sector",
    ),
    optional_fields=(
        "description",
        "phone",
        "website",
    ),
    notes=(
        "Le domaine agricole ou agronomique doit etre renseigne.",
    ),
)
