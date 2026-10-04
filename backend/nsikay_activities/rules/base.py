from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class ActivityRule:
    """
    Regle interne NSIKAY applicable a un type d'activite.

    Cette classe ne remplace pas les obligations legales du pays
    concerne. Elle definit uniquement les regles fonctionnelles
    internes de la plateforme NSIKAY.
    """

    activity_type: str
    label: str

    certification_required: bool = False

    activation_requires_certification: bool = False

    default_visibility: str = "public"

    mandatory_fields: Tuple[str, ...] = field(default_factory=tuple)

    optional_fields: Tuple[str, ...] = field(default_factory=tuple)

    wenzе_required: bool = False

    unique_per_account: bool = False

    notes: Tuple[str, ...] = field(default_factory=tuple)
