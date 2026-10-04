from .base import ActivityRule


RULE = ActivityRule(
    activity_type="bank",
    label="Banque",
    certification_required=True,
    activation_requires_certification=True,
    mandatory_fields=(
        "name",
        "country",
        "city",
    ),
    optional_fields=(
        "description",
        "phone",
        "website",
        "sector",
    ),
    notes=(
        "L'activite bancaire est soumise a une verification renforcee NSIKAY.",
        "Les autorisations legales applicables restent celles du pays concerne.",
    ),
)
