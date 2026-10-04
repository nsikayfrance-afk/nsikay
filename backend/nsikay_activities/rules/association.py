from .base import ActivityRule


ASSOCIATION_RULE = ActivityRule(
    activity_type="association",
    label="Association",
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
        "L'identite de l'association doit etre renseignee.",
    ),
)


INSTITUTION_RULE = ActivityRule(
    activity_type="institution",
    label="Institution",
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
        "L'institution doit etre verifiee avant activation.",
    ),
)
