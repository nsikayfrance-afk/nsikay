from .base import ActivityRule

from .company import RULE as COMPANY_RULE
from .bank import RULE as BANK_RULE
from .shop import RULE as SHOP_RULE
from .gift_reseller import RULE as GIFT_RESELLER_RULE
from .professional import RULE as PROFESSIONAL_RULE
from .health import RULE as HEALTH_RULE
from .education import SCHOOL_RULE, TRAINING_RULE
from .association import ASSOCIATION_RULE, INSTITUTION_RULE
from .media import RULE as MEDIA_RULE
from .technology import RULE as TECHNOLOGY_RULE
from .agriculture import RULE as AGRICULTURE_RULE
from .logistics import RULE as LOGISTICS_RULE


ACTIVITY_RULES = {
    "professional": PROFESSIONAL_RULE,

    "company": COMPANY_RULE,

    "bank": BANK_RULE,

    "service": ActivityRule(
        activity_type="service",
        label="Service",
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
            "Le domaine du service doit etre identifiable.",
        ),
    ),

    "shop": SHOP_RULE,

    "creator": ActivityRule(
        activity_type="creator",
        label="Createur",
        certification_required=True,
        activation_requires_certification=True,
        mandatory_fields=(
            "name",
        ),
        optional_fields=(
            "description",
            "sector",
            "country",
            "city",
            "phone",
            "website",
        ),
        notes=(
            "Le createur peut exercer plusieurs formes d'activites creatives.",
        ),
    ),

    "artist": ActivityRule(
        activity_type="artist",
        label="Artiste",
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
            "La discipline artistique doit etre identifiable.",
        ),
    ),

    "sport": ActivityRule(
        activity_type="sport",
        label="Sport",
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
            "La discipline ou activite sportive doit etre identifiable.",
        ),
    ),

    "training": TRAINING_RULE,

    "school": SCHOOL_RULE,

    "health": HEALTH_RULE,

    "association": ASSOCIATION_RULE,

    "institution": INSTITUTION_RULE,

    "agent": ActivityRule(
        activity_type="agent",
        label="Agent / Expert",
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
            "Le domaine d'expertise doit etre identifiable.",
            "La certification est distincte de l'evaluation publique.",
        ),
    ),

    "media": MEDIA_RULE,

    "agriculture": AGRICULTURE_RULE,

    "technology": TECHNOLOGY_RULE,

    "gift_reseller": GIFT_RESELLER_RULE,

    "logistics": LOGISTICS_RULE,

    "other": ActivityRule(
        activity_type="other",
        label="Autre",
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
            "Le type Autre ne peut pas servir a contourner les regles.",
            "Une reclassification administrative peut etre demandee.",
        ),
    ),
}


def get_activity_rule(activity_type):
    return ACTIVITY_RULES.get(activity_type)


def get_activity_rules():
    return ACTIVITY_RULES.copy()
