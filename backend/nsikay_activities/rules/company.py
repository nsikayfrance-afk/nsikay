from .base import ActivityRule


RULE = ActivityRule(
    activity_type="company",
    label="Entreprise",
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
        "L'identite de l'entreprise doit etre renseignee.",
        "La certification NSIKAY est requise avant activation.",
    ),
)
