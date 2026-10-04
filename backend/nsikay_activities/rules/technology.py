from .base import ActivityRule


RULE = ActivityRule(
    activity_type="technology",
    label="Technologie",
    certification_required=True,
    activation_requires_certification=True,
    mandatory_fields=(
        "name",
        "sector",
    ),
    optional_fields=(
        "description",
        "country",
        "city",
        "phone",
        "website",
    ),
    notes=(
        "Le domaine technologique doit etre identifiable.",
    ),
)
