from .base import ActivityRule


RULE = ActivityRule(
    activity_type="gift_reseller",
    label="Revendeur de cadeaux",
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
    ),
    unique_per_account=True,
    notes=(
        "Le Revendeur de cadeaux est une activite NSIKAY.",
        "Un compte ne peut posseder qu'une seule activite Revendeur de cadeaux.",
        "Un enregistrement Reseller est associe automatiquement a l'activite.",
    ),
)
