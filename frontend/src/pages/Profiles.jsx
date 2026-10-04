import { useEffect, useMemo, useState } from "react";
import api from "../services/api";

const PROFILE_TYPES = [
    {
        value: "person",
        label: "Profil personnel",
        icon: "👤",
        description: "Identité et informations personnelles.",
    },
    {
        value: "professional",
        label: "Métier / Professionnel",
        icon: "💼",
        description: "Compétences, services et expérience.",
    },
    {
        value: "company",
        label: "Entreprise",
        icon: "🏢",
        description: "Entreprise, secteur, services et dirigeants.",
    },
    {
        value: "bank",
        label: "Banque",
        icon: "🏦",
        description: "Services bancaires, pays et devises.",
    },
    {
        value: "school",
        label: "École",
        icon: "🎓",
        description: "Établissement, formations et enseignants.",
    },
    {
        value: "training",
        label: "Centre de formation",
        icon: "📚",
        description: "Programmes, formations et certifications.",
    },
    {
        value: "health",
        label: "Santé",
        icon: "🏥",
        description: "Établissement, spécialités et professionnels.",
    },
    {
        value: "association",
        label: "Association",
        icon: "🤝",
        description: "Missions, activités et événements.",
    },
    {
        value: "institution",
        label: "Institution",
        icon: "🏛️",
        description: "Domaine, services et territoire.",
    },
    {
        value: "artist",
        label: "Artiste / Créateur",
        icon: "🎨",
        description: "Domaine artistique, œuvres et événements.",
    },
    {
        value: "agent",
        label: "Agent / Expert",
        icon: "🛡️",
        description: "Expertise, missions et certification.",
    },
];

const SPECIAL_FIELDS = {
    person: [
        ["profession", "Profession"],
        ["skills", "Compétences"],
        ["interests", "Centres d'intérêt"],
    ],

    professional: [
        ["profession", "Métier / Profession"],
        ["skills", "Compétences"],
        ["services", "Services proposés"],
        ["experience", "Expérience"],
        ["languages", "Langues"],
    ],

    company: [
        ["sector", "Secteur d'activité"],
        ["services", "Services"],
        ["leaders", "Dirigeants"],
        ["employees", "Effectif"],
        ["projects", "Projets"],
    ],

    bank: [
        ["bank_type", "Type de banque"],
        ["services", "Services bancaires"],
        ["countries", "Pays couverts"],
        ["currencies", "Devises"],
        ["swift", "Code SWIFT / BIC"],
        ["certification", "Certification / Autorisation"],
    ],

    school: [
        ["school_type", "Type d'établissement"],
        ["formations", "Formations"],
        ["teachers", "Enseignants"],
        ["levels", "Niveaux d'enseignement"],
        ["certifications", "Certifications / diplômes"],
    ],

    training: [
        ["programs", "Programmes"],
        ["domains", "Domaines de formation"],
        ["trainers", "Formateurs"],
        ["certifications", "Certifications"],
        ["duration", "Durée des formations"],
    ],

    health: [
        ["establishment_type", "Type d'établissement"],
        ["specialties", "Spécialités"],
        ["professionals", "Professionnels"],
        ["services", "Services de santé"],
        ["emergency", "Service d'urgence"],
    ],

    association: [
        ["mission", "Mission"],
        ["activities", "Activités"],
        ["domains", "Domaines d'action"],
        ["events", "Événements"],
        ["members", "Membres"],
    ],

    institution: [
        ["domain", "Domaine"],
        ["services", "Services"],
        ["territory", "Territoire d'intervention"],
        ["responsibilities", "Responsabilités"],
    ],

    artist: [
        ["artistic_domain", "Domaine artistique"],
        ["works", "Œuvres"],
        ["events", "Événements"],
        ["social_links", "Réseaux / médias"],
        ["portfolio", "Portfolio"],
    ],

    agent: [
        ["expertise", "Expertise"],
        ["missions", "Missions"],
        ["domains", "Domaines d'intervention"],
        ["certification", "Certification"],
        ["territory", "Territoire d'intervention"],
    ],
};

const EMPTY_FORM = {
    profile_type: "person",
    display_name: "",
    legal_name: "",
    professional_title: "",
    description: "",
    country: "",
    city: "",
    phone: "",
    website: "",
    sector: "",
    visibility: "public",
    status: "active",
    is_primary: false,
    certification_required: false,
    specialized_data: {},
};

function getType(value) {
    return PROFILE_TYPES.find((item) => item.value === value) || PROFILE_TYPES[0];
}

function buildForm(profile) {
    if (!profile) return { ...EMPTY_FORM, specialized_data: {} };

    return {
        profile_type: profile.profile_type || "person",
        display_name: profile.display_name || "",
        legal_name: profile.legal_name || "",
        professional_title: profile.professional_title || "",
        description: profile.description || "",
        country: profile.country || "",
        city: profile.city || "",
        phone: profile.phone || "",
        website: profile.website || "",
        sector: profile.sector || "",
        visibility: profile.visibility || "public",
        status: profile.status || "active",
        is_primary: Boolean(profile.is_primary),
        certification_required: Boolean(profile.certification_required),
        specialized_data: profile.specialized_data || {},
    };
}

export default function Profiles() {
    const [profiles, setProfiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [search, setSearch] = useState("");
    const [filterType, setFilterType] = useState("all");
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [form, setForm] = useState({ ...EMPTY_FORM });

    const loadProfiles = async () => {
        setLoading(true);
        setError("");

        try {
            const data = await api.profiles();
            setProfiles(Array.isArray(data) ? data : data.results || []);
        } catch (err) {
            setError(err.message || "Impossible de charger les profils.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProfiles();
    }, []);

    const filteredProfiles = useMemo(() => {
        const term = search.trim().toLowerCase();

        return profiles.filter((profile) => {
            const matchesType =
                filterType === "all" || profile.profile_type === filterType;

            if (!term) return matchesType;

            const specialized = JSON.stringify(
                profile.specialized_data || {}
            ).toLowerCase();

            return (
                matchesType &&
                (
                    profile.display_name ||
                    profile.legal_name ||
                    profile.description ||
                    profile.country ||
                    profile.city ||
                    profile.sector ||
                    ""
                )
                    .toLowerCase()
                    .includes(term) ||
                specialized.includes(term)
            );
        });
    }, [profiles, search, filterType]);

    const openCreate = () => {
        setEditingId(null);
        setForm({ ...EMPTY_FORM, specialized_data: {} });
        setError("");
        setSuccess("");
        setShowForm(true);
    };

    const openEdit = (profile) => {
        setEditingId(profile.id);
        setForm(buildForm(profile));
        setError("");
        setSuccess("");
        setShowForm(true);
    };

    const closeForm = () => {
        if (saving) return;
        setShowForm(false);
        setEditingId(null);
    };

    const updateField = (field, value) => {
        setForm((current) => ({
            ...current,
            [field]: value,
        }));
    };

    const updateSpecialField = (field, value) => {
        setForm((current) => ({
            ...current,
            specialized_data: {
                ...current.specialized_data,
                [field]: value,
            },
        }));
    };

    const saveProfile = async (event) => {
        event.preventDefault();

        if (!form.display_name.trim()) {
            setError("Le nom du profil est obligatoire.");
            return;
        }

        setSaving(true);
        setError("");
        setSuccess("");

        try {
            if (editingId) {
                await api.updateProfileItem(editingId, form);
                setSuccess("Profil modifié avec succès.");
            } else {
                await api.createProfile(form);
                setSuccess("Profil créé avec succès.");
            }

            await loadProfiles();

            setTimeout(() => {
                setShowForm(false);
                setEditingId(null);
            }, 500);
        } catch (err) {
            setError(err.message || "Erreur lors de l'enregistrement.");
        } finally {
            setSaving(false);
        }
    };

    const deleteProfile = async (profile) => {
        const confirmed = window.confirm(
            `Supprimer le profil « ${profile.display_name} » ?`
        );

        if (!confirmed) return;

        setError("");
        setSuccess("");

        try {
            await api.deleteProfileItem(profile.id);
            setSuccess("Profil supprimé.");
            await loadProfiles();
        } catch (err) {
            setError(err.message || "Impossible de supprimer le profil.");
        }
    };

    const currentType = getType(form.profile_type);
    const fields = SPECIAL_FIELDS[form.profile_type] || [];

    return (
        <div className="nsikay-page">
            <section className="nsikay-page-header">
                <div>
                    <span className="nsikay-eyebrow">NSIKAY · IDENTITÉ</span>
                    <h1>Profils</h1>
                    <p>
                        Une identité NSIKAY, plusieurs dimensions personnelles,
                        professionnelles et institutionnelles.
                    </p>
                </div>

                <button className="nsikay-primary-btn" onClick={openCreate}>
                    + Créer un profil
                </button>
            </section>

            <section className="profiles-toolbar">
                <input
                    type="search"
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                    placeholder="Rechercher un profil..."
                />

                <select
                    value={filterType}
                    onChange={(event) => setFilterType(event.target.value)}
                >
                    <option value="all">Tous les profils</option>
                    {PROFILE_TYPES.map((type) => (
                        <option key={type.value} value={type.value}>
                            {type.label}
                        </option>
                    ))}
                </select>
            </section>

            {error && !showForm && (
                <div className="nsikay-alert nsikay-alert-error">
                    {error}
                </div>
            )}

            {success && !showForm && (
                <div className="nsikay-alert nsikay-alert-success">
                    {success}
                </div>
            )}

            {loading ? (
                <div className="profiles-empty">
                    Chargement des profils...
                </div>
            ) : filteredProfiles.length === 0 ? (
                <div className="profiles-empty">
                    <div className="profiles-empty-icon">◉</div>
                    <h2>Aucun profil trouvé</h2>
                    <p>
                        Crée ton premier profil NSIKAY ou modifie les critères
                        de recherche.
                    </p>
                    <button
                        className="nsikay-primary-btn"
                        onClick={openCreate}
                    >
                        Créer mon profil
                    </button>
                </div>
            ) : (
                <section className="profiles-grid">
                    {filteredProfiles.map((profile) => {
                        const type = getType(profile.profile_type);

                        return (
                            <article className="profile-card" key={profile.id}>
                                <div className="profile-card-top">
                                    <div className="profile-type-icon">
                                        {type.icon}
                                    </div>

                                    <div className="profile-card-status">
                                        {profile.is_primary && (
                                            <span className="profile-badge primary">
                                                Principal
                                            </span>
                                        )}

                                        {profile.certification_required && (
                                            <span className="profile-badge certification">
                                                Certification
                                            </span>
                                        )}
                                    </div>
                                </div>

                                <span className="profile-card-type">
                                    {type.label}
                                </span>

                                <h2>{profile.display_name}</h2>

                                {profile.professional_title && (
                                    <p className="profile-title">
                                        {profile.professional_title}
                                    </p>
                                )}

                                {profile.description && (
                                    <p className="profile-description">
                                        {profile.description}
                                    </p>
                                )}

                                <div className="profile-meta">
                                    {(profile.city || profile.country) && (
                                        <span>
                                            📍{" "}
                                            {[profile.city, profile.country]
                                                .filter(Boolean)
                                                .join(", ")}
                                        </span>
                                    )}

                                    {profile.sector && (
                                        <span>▣ {profile.sector}</span>
                                    )}
                                </div>

                                <div className="profile-specialized">
                                    {Object.entries(
                                        profile.specialized_data || {}
                                    )
                                        .filter(
                                            ([, value]) =>
                                                value !== null &&
                                                value !== undefined &&
                                                String(value).trim() !== ""
                                        )
                                        .slice(0, 4)
                                        .map(([key, value]) => (
                                            <div key={key}>
                                                <strong>{key}</strong>
                                                <span>{String(value)}</span>
                                            </div>
                                        ))}
                                </div>

                                <div className="profile-card-actions">
                                    <button
                                        className="nsikay-secondary-btn"
                                        onClick={() => openEdit(profile)}
                                    >
                                        Modifier
                                    </button>

                                    <button
                                        className="nsikay-danger-btn"
                                        onClick={() => deleteProfile(profile)}
                                    >
                                        Supprimer
                                    </button>
                                </div>
                            </article>
                        );
                    })}
                </section>
            )}

            {showForm && (
                <div className="profiles-modal-backdrop">
                    <div className="profiles-modal">
                        <div className="profiles-modal-header">
                            <div>
                                <span className="nsikay-eyebrow">
                                    NSIKAY · PROFIL SPÉCIALISÉ
                                </span>

                                <h2>
                                    {editingId
                                        ? "Modifier le profil"
                                        : "Créer un profil"}
                                </h2>
                            </div>

                            <button
                                className="profiles-close"
                                onClick={closeForm}
                                disabled={saving}
                            >
                                ×
                            </button>
                        </div>

                        <div className="profile-type-preview">
                            <span>{currentType.icon}</span>
                            <div>
                                <strong>{currentType.label}</strong>
                                <small>{currentType.description}</small>
                            </div>
                        </div>

                        <form onSubmit={saveProfile}>
                            <div className="profile-form-grid">
                                <label>
                                    Type de profil
                                    <select
                                        value={form.profile_type}
                                        onChange={(event) => {
                                            const type =
                                                event.target.value;

                                            updateField(
                                                "profile_type",
                                                type
                                            );

                                            updateField(
                                                "specialized_data",
                                                {}
                                            );
                                        }}
                                        disabled={Boolean(editingId)}
                                    >
                                        {PROFILE_TYPES.map((type) => (
                                            <option
                                                key={type.value}
                                                value={type.value}
                                            >
                                                {type.label}
                                            </option>
                                        ))}
                                    </select>
                                </label>

                                <label>
                                    Nom du profil *
                                    <input
                                        value={form.display_name}
                                        onChange={(event) =>
                                            updateField(
                                                "display_name",
                                                event.target.value
                                            )
                                        }
                                        required
                                    />
                                </label>

                                <label>
                                    Dénomination légale
                                    <input
                                        value={form.legal_name}
                                        onChange={(event) =>
                                            updateField(
                                                "legal_name",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Titre professionnel
                                    <input
                                        value={form.professional_title}
                                        onChange={(event) =>
                                            updateField(
                                                "professional_title",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Pays
                                    <input
                                        value={form.country}
                                        onChange={(event) =>
                                            updateField(
                                                "country",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Ville
                                    <input
                                        value={form.city}
                                        onChange={(event) =>
                                            updateField(
                                                "city",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Téléphone
                                    <input
                                        value={form.phone}
                                        onChange={(event) =>
                                            updateField(
                                                "phone",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Site web
                                    <input
                                        type="url"
                                        value={form.website}
                                        onChange={(event) =>
                                            updateField(
                                                "website",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Secteur général
                                    <input
                                        value={form.sector}
                                        onChange={(event) =>
                                            updateField(
                                                "sector",
                                                event.target.value
                                            )
                                        }
                                    />
                                </label>

                                <label>
                                    Visibilité
                                    <select
                                        value={form.visibility}
                                        onChange={(event) =>
                                            updateField(
                                                "visibility",
                                                event.target.value
                                            )
                                        }
                                    >
                                        <option value="public">
                                            Public
                                        </option>
                                        <option value="private">
                                            Privé
                                        </option>
                                    </select>
                                </label>
                            </div>

                            <label className="profile-form-full">
                                Description
                                <textarea
                                    rows="4"
                                    value={form.description}
                                    onChange={(event) =>
                                        updateField(
                                            "description",
                                            event.target.value
                                        )
                                    }
                                />
                            </label>

                            {fields.length > 0 && (
                                <section className="specialized-section">
                                    <div className="specialized-section-title">
                                        <span>⚙</span>
                                        <div>
                                            <h3>
                                                Informations spécialisées
                                            </h3>
                                            <p>
                                                Ces informations dépendent du
                                                type de profil sélectionné.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="profile-form-grid">
                                        {fields.map(([key, label]) => (
                                            <label key={key}>
                                                {label}
                                                <input
                                                    value={
                                                        form
                                                            .specialized_data[
                                                            key
                                                        ] || ""
                                                    }
                                                    onChange={(event) =>
                                                        updateSpecialField(
                                                            key,
                                                            event.target.value
                                                        )
                                                    }
                                                />
                                            </label>
                                        ))}
                                    </div>
                                </section>
                            )}

                            <section className="profile-options">
                                <label className="profile-checkbox">
                                    <input
                                        type="checkbox"
                                        checked={form.is_primary}
                                        onChange={(event) =>
                                            updateField(
                                                "is_primary",
                                                event.target.checked
                                            )
                                        }
                                    />
                                    <span>
                                        Définir comme profil principal
                                    </span>
                                </label>

                                <label className="profile-checkbox">
                                    <input
                                        type="checkbox"
                                        checked={form.certification_required}
                                        onChange={(event) =>
                                            updateField(
                                                "certification_required",
                                                event.target.checked
                                            )
                                        }
                                    />
                                    <span>
                                        Activité nécessitant une certification
                                    </span>
                                </label>
                            </section>

                            {error && (
                                <div className="nsikay-alert nsikay-alert-error">
                                    {error}
                                </div>
                            )}

                            {success && (
                                <div className="nsikay-alert nsikay-alert-success">
                                    {success}
                                </div>
                            )}

                            <div className="profiles-modal-actions">
                                <button
                                    type="button"
                                    className="nsikay-secondary-btn"
                                    onClick={closeForm}
                                    disabled={saving}
                                >
                                    Annuler
                                </button>

                                <button
                                    type="submit"
                                    className="nsikay-primary-btn"
                                    disabled={saving}
                                >
                                    {saving
                                        ? "Enregistrement..."
                                        : editingId
                                          ? "Enregistrer les modifications"
                                          : "Créer le profil"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
