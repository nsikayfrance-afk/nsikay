from .base import ActivityRule


RULE = ActivityRule(
    activity_type="professional",
    label="Professionnel",
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
        "Le domaine professionnel doit etre identifiable.",
        "La certification depend du domaine exerce.",
    ),
)
