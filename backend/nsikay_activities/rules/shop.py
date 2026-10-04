from .base import ActivityRule


RULE = ActivityRule(
    activity_type="shop",
    label="Commerce",
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
    wenzе_required=True,
    notes=(
        "Les ventes commerciales NSIKAY sont gerees via WENZE.",
        "WENZE reste gratuit et sans commission commerciale.",
    ),
)
