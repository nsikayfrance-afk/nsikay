from .base import ActivityRule


RULE = ActivityRule(
    activity_type="media",
    label="Media",
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
        "Le media doit disposer d'une identite identifiable.",
        "Les autorisations applicables restent celles du pays concerne.",
    ),
)
