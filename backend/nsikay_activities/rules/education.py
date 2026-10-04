from .base import ActivityRule


SCHOOL_RULE = ActivityRule(
    activity_type="school",
    label="Ecole",
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
        "Une ecole doit etre verifiee avant activation.",
    ),
)


TRAINING_RULE = ActivityRule(
    activity_type="training",
    label="Formation",
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
        "Le domaine de formation doit etre renseigne.",
    ),
)
