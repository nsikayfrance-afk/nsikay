from .base import ActivityRule


RULE = ActivityRule(
    activity_type="health",
    label="Sante",
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
        "Les activites de sante font l'objet d'une verification renforcee.",
        "Les autorisations sanitaires applicables restent celles du pays concerne.",
    ),
)
