from .base import ActivityRule


RULE = ActivityRule(
    activity_type="logistics",
    label="Logistique",
    certification_required=True,
    activation_requires_certification=True,
    mandatory_fields=(
        "name",
        "country",
        "city",
    ),
    optional_fields=(
        "description",
        "sector",
        "phone",
        "website",
    ),
    notes=(
        "Les services logistiques doivent etre identifies avant activation.",
        "Les autorisations de transport applicables restent celles du pays concerne.",
    ),
)
