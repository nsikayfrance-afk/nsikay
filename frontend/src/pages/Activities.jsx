import React, { useEffect, useMemo, useState } from "react";

import {
    listActivities,
    createActivity,
    updateActivity,
    listActivityCertifications,
    getActivityCertification,
    getActivityCertificationHistory,
} from "../services/activities";

const ACTIVITY_TYPES = [
    ["professional", "Professionnel"],
    ["company", "Entreprise"],
    ["bank", "Banque"],
    ["service", "Service"],
    ["shop", "Commerce / WENZE"],
    ["creator", "Créateur"],
    ["artist", "Artiste"],
    ["sport", "Sport"],
    ["training", "Formation"],
    ["school", "École"],
    ["health", "Santé"],
    ["association", "Association"],
    ["institution", "Institution"],
    ["agent", "Agent / Expert"],
    ["media", "Média"],
    ["agriculture", "Agriculture"],
    ["technology", "Technologie"],
    ["gift_reseller", "Revendeur de cadeaux"],
    ["logistics", "Logistique"],
    ["other", "Autre"],
];

const TYPE_LABELS = Object.fromEntries(ACTIVITY_TYPES);

const CERTIFICATION_LABELS = {
    not_required: "Non requise",
    pending: "En attente",
    certified: "Certifiée",
    rejected: "Refusée",
    expired: "Expirée",
};

const STATUS_LABELS = {
    draft: "Brouillon",
    active: "Active",
    suspended: "Suspendue",
};

const REQUIRED_RULES = {
    professional: ["name", "sector"],
    company: ["name", "country", "city", "sector"],
    bank: ["name", "country", "city"],
    service: ["name", "sector"],
    shop: ["name", "country", "city"],
    creator: ["name"],
    artist: ["name", "sector"],
    sport: ["name", "sector"],
    training: ["name", "sector"],
    school: ["name", "country", "city"],
    health: ["name", "country", "city", "sector"],
    association: ["name", "country", "city"],
    institution: ["name", "country", "city"],
    agent: ["name", "sector"],
    media: ["name", "country", "city"],
    agriculture: ["name", "country", "city", "sector"],
    technology: ["name", "sector"],
    gift_reseller: ["name", "country", "city"],
    logistics: ["name", "country", "city"],
    other: ["name", "sector"],
};

function extractResults(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (Array.isArray(data?.results)) {
        return data.results;
    }

    return [];
}

function statusClass(status) {
    if (status === "active") {
        return "activity-status activity-status-active";
    }

    if (status === "suspended") {
        return "activity-status activity-status-suspended";
    }

    return "activity-status activity-status-draft";
}

function certificationClass(status) {
    if (status === "certified") {
        return "activity-certification activity-certification-ok";
    }

    if (status === "rejected" || status === "expired") {
        return "activity-certification activity-certification-error";
    }

    return "activity-certification activity-certification-pending";
}

function initialForm() {
    return {
        name: "",
        activity_type: "professional",
        description: "",
        sector: "",
        country: "",
        city: "",
        phone: "",
        website: "",
        status: "draft",
        visibility: "public",
    };
}

export default function Activities() {

    const [activities, setActivities] = useState([]);
    const [activityCertifications, setActivityCertifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [selectedId, setSelectedId] = useState(null);

    const [form, setForm] = useState(initialForm());

    const loadActivityCertifications = async () => {
        try {
            const data = await listActivityCertifications();

            const results = Array.isArray(data)
                ? data
                : (data?.results || []);

            setActivityCertifications(results);
        } catch (error) {
            console.error(
                "Erreur chargement certifications activités:",
                error
            );

            setActivityCertifications([]);
        }
    };
    const loadActivities = async () => {

        setLoading(true);
        setError("");

        try {

            const data = await listActivities();

            setActivities(extractResults(data));

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de charger les activités."
            );

        } finally {

            setLoading(false);
        }
    };

    useEffect(() => {
        loadActivities();
        loadActivityCertifications();
    }, []);

    const selectedActivity = useMemo(
        () =>
            activities.find(
                (activity) =>
                    activity.id === selectedId
            ) || null,
        [activities, selectedId]
    );

    const requiredFields =
        REQUIRED_RULES[form.activity_type] || ["name"];

    const updateForm = (field, value) => {

        setForm((current) => ({
            ...current,
            [field]: value,
        }));
    };

    const resetForm = () => {

        setForm(initialForm());
        setSelectedId(null);
        setShowForm(false);
    };

    const getCertificationForActivity = (activity) => {
        if (!activity) {
            return null;
        }

        const activityId = Number(activity.id);

        return (
            activityCertifications.find(
                (certification) =>
                    Number(certification.activity_id) === activityId
            ) || null
        );
    };
    const handleCreate = async (event) => {

        event.preventDefault();

        setError("");
        setMessage("");

        const missing = requiredFields.filter(
            (field) =>
                !String(form[field] || "").trim()
        );

        if (missing.length > 0) {

            setError(
                `Champs obligatoires : ${missing.join(", ")}`
            );

            return;
        }

        setSaving(true);

        try {

            const payload = {
                ...form,
                status: "draft",
            };

            const created =
                await createActivity(payload);
                await loadActivityCertifications();

            setMessage(
                "Activité créée. Elle reste en brouillon jusqu'à la certification NSIKAY."
            );

            setActivities((current) => [
                created,
                ...current,
            ]);

            setSelectedId(created?.id || null);
            setForm(initialForm());
            setShowForm(false);

            await loadActivities();

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de créer l'activité."
            );

        } finally {

            setSaving(false);
        }
    };

    const handleActivate = async (activity) => {

        setError("");
        setMessage("");

        try {

            const updated =
                await updateActivity(
                    activity.id,
                    {
                        status: "active",
                    }
                );

            setActivities((current) =>
                current.map((item) =>
                    item.id === updated.id
                        ? updated
                        : item
                )
            );

            setMessage(
                "Activité activée."
            );

        } catch (err) {

            setError(
                err?.message ||
                "L'activation est impossible avant certification."
            );

            await loadActivities();
        }
    };

    return (
        <div className="activities-page">

            <style>{`
                .activities-page {
                    min-height: 100%;
                    padding: 28px;
                    background: #f5f7fb;
                    color: #172033;
                }

                .activities-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    gap: 20px;
                    margin-bottom: 24px;
                }

                .activities-title {
                    margin: 0;
                    font-size: 30px;
                    font-weight: 800;
                }

                .activities-subtitle {
                    margin: 8px 0 0;
                    color: #667085;
                    max-width: 760px;
                    line-height: 1.5;
                }

                .activities-primary-button {
                    border: 0;
                    border-radius: 10px;
                    padding: 12px 18px;
                    background: #173b75;
                    color: white;
                    font-weight: 700;
                    cursor: pointer;
                }

                .activities-primary-button:hover {
                    opacity: .92;
                }

                .activities-message {
                    margin-bottom: 18px;
                    padding: 12px 14px;
                    border-radius: 10px;
                    background: #e9f8ef;
                    color: #146c37;
                    border: 1px solid #b9e4c8;
                }

                .activities-error {
                    margin-bottom: 18px;
                    padding: 12px 14px;
                    border-radius: 10px;
                    background: #fff0f0;
                    color: #a12828;
                    border: 1px solid #efc2c2;
                }

                .activities-form {
                    margin-bottom: 24px;
                    padding: 22px;
                    border-radius: 14px;
                    background: white;
                    border: 1px solid #e4e7ec;
                    box-shadow: 0 4px 14px rgba(16, 24, 40, .05);
                }

                .activities-form h2 {
                    margin-top: 0;
                    margin-bottom: 18px;
                }

                .activities-form-grid {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 15px;
                }

                .activities-field {
                    display: flex;
                    flex-direction: column;
                    gap: 7px;
                }

                .activities-field-full {
                    grid-column: 1 / -1;
                }

                .activities-field label {
                    font-weight: 700;
                    font-size: 13px;
                }

                .activities-field input,
                .activities-field select,
                .activities-field textarea {
                    width: 100%;
                    box-sizing: border-box;
                    padding: 10px 12px;
                    border: 1px solid #d0d5dd;
                    border-radius: 8px;
                    background: white;
                    font: inherit;
                }

                .activities-field textarea {
                    min-height: 100px;
                    resize: vertical;
                }

                .activities-form-actions {
                    display: flex;
                    gap: 10px;
                    margin-top: 18px;
                }

                .activities-secondary-button {
                    border: 1px solid #d0d5dd;
                    border-radius: 9px;
                    padding: 10px 16px;
                    background: white;
                    cursor: pointer;
                    font-weight: 600;
                }

                .activities-grid {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 18px;
                }

                .activity-card {
                    background: white;
                    border: 1px solid #e4e7ec;
                    border-radius: 14px;
                    padding: 20px;
                    box-shadow: 0 4px 14px rgba(16, 24, 40, .05);
                }

                .activity-card-selected {
                    border-color: #173b75;
                    box-shadow: 0 0 0 2px rgba(23, 59, 117, .08);
                }

                .activity-card-top {
                    display: flex;
                    justify-content: space-between;
                    gap: 12px;
                    align-items: flex-start;
                }

                .activity-card h3 {
                    margin: 0;
                    font-size: 19px;
                }

                .activity-type {
                    margin-top: 5px;
                    color: #667085;
                    font-size: 13px;
                }

                .activity-status,
                .activity-certification {
                    display: inline-block;
                    margin-top: 12px;
                    padding: 5px 9px;
                    border-radius: 999px;
                    font-size: 12px;
                    font-weight: 700;
                }

                .activity-status-draft {
                    background: #f2f4f7;
                    color: #475467;
                }

                .activity-status-active {
                    background: #e9f8ef;
                    color: #146c37;
                }

                .activity-status-suspended {
                    background: #fff4e5;
                    color: #9a5b00;
                }

                .activity-certification-pending {
                    background: #fff4e5;
                    color: #9a5b00;
                }

                .activity-certification-ok {
                    background: #e9f8ef;
                    color: #146c37;
                }

                .activity-certification-error {
                    background: #fff0f0;
                    color: #a12828;
                }

                .activity-card-description {
                    margin: 15px 0;
                    color: #475467;
                    line-height: 1.45;
                    min-height: 42px;
                }

                .activity-card-meta {
                    display: grid;
                    gap: 7px;
                    margin-top: 15px;
                    font-size: 13px;
                    color: #667085;
                }

                .activity-card-actions {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 18px;
                }

                .activity-card-actions button {
                    border: 1px solid #d0d5dd;
                    border-radius: 8px;
                    padding: 8px 11px;
                    background: white;
                    cursor: pointer;
                    font-weight: 600;
                }

                .activity-card-actions button:disabled {
                    opacity: .5;
                    cursor: not-allowed;
                }

                .activities-empty,
                .activities-loading {
                    padding: 45px;
                    text-align: center;
                    background: white;
                    border: 1px solid #e4e7ec;
                    border-radius: 14px;
                    color: #667085;
                }

                .activity-detail {
                    margin-bottom: 24px;
                    padding: 18px;
                    border-radius: 12px;
                    background: #eef4ff;
                    border: 1px solid #cbdaf5;
                }

                @media (max-width: 1000px) {
                    .activities-grid {
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                    }
                }

                @media (max-width: 700px) {
                    .activities-page {
                        padding: 16px;
                    }

                    .activities-header {
                        flex-direction: column;
                    }

                    .activities-form-grid,
                    .activities-grid {
                        grid-template-columns: 1fr;
                    }

                    .activities-field-full {
                        grid-column: auto;
                    }
                }
            `}</style>

            <header className="activities-header">

                <div>
                    <h1 className="activities-title">
                        Mes activités
                    </h1>

                    <p className="activities-subtitle">
                        Gérez vos activités professionnelles,
                        commerciales, artistiques, associatives
                        et autres activités NSIKAY depuis votre
                        identité personnelle.
                    </p>
                </div>

                <button
                    type="button"
                    className="activities-primary-button"
                    onClick={() => {
                        setShowForm(true);
                        setError("");
                        setMessage("");
                    }}
                >
                    + Nouvelle activité
                </button>

            </header>

            {message && (
                <div className="activities-message">
                    {message}
                </div>
            )}

            {error && (
                <div className="activities-error">
                    {error}
                </div>
            )}

            {selectedActivity && (
                <div className="activity-detail">
                    <strong>
                        Activité sélectionnée :
                    </strong>{" "}
                    {selectedActivity.name}
                    {" — "}
                    {TYPE_LABELS[
                        selectedActivity.activity_type
                    ] || selectedActivity.activity_type}
                </div>
            )}

            {showForm && (
                <form
                    className="activities-form"
                    onSubmit={handleCreate}
                >

                    <h2>
                        Créer une activité
                    </h2>

                    <div className="activities-form-grid">

                        <div className="activities-field">
                            <label>
                                Type d'activité
                            </label>

                            <select
                                value={form.activity_type}
                                onChange={(event) =>
                                    updateForm(
                                        "activity_type",
                                        event.target.value
                                    )
                                }
                            >
                                {ACTIVITY_TYPES.map(
                                    ([value, label]) => (
                                        <option
                                            key={value}
                                            value={value}
                                        >
                                            {label}
                                        </option>
                                    )
                                )}
                            </select>
                        </div>

                        <div className="activities-field">
                            <label>
                                Nom de l'activité *
                            </label>

                            <input
                                value={form.name}
                                onChange={(event) =>
                                    updateForm(
                                        "name",
                                        event.target.value
                                    )
                                }
                                placeholder="Nom de l'activité"
                            />
                        </div>

                        {(requiredFields.includes("sector") ||
                            form.sector) && (
                            <div className="activities-field">
                                <label>
                                    Secteur
                                    {requiredFields.includes(
                                        "sector"
                                    ) ? " *" : ""}
                                </label>

                                <input
                                    value={form.sector}
                                    onChange={(event) =>
                                        updateForm(
                                            "sector",
                                            event.target.value
                                        )
                                    }
                                    placeholder="Secteur d'activité"
                                />
                            </div>
                        )}

                        {(requiredFields.includes("country") ||
                            form.country) && (
                            <div className="activities-field">
                                <label>
                                    Pays
                                    {requiredFields.includes(
                                        "country"
                                    ) ? " *" : ""}
                                </label>

                                <input
                                    value={form.country}
                                    onChange={(event) =>
                                        updateForm(
                                            "country",
                                            event.target.value
                                        )
                                    }
                                    placeholder="Pays"
                                />
                            </div>
                        )}

                        {(requiredFields.includes("city") ||
                            form.city) && (
                            <div className="activities-field">
                                <label>
                                    Ville
                                    {requiredFields.includes(
                                        "city"
                                    ) ? " *" : ""}
                                </label>

                                <input
                                    value={form.city}
                                    onChange={(event) =>
                                        updateForm(
                                            "city",
                                            event.target.value
                                        )
                                    }
                                    placeholder="Ville"
                                />
                            </div>
                        )}

                        <div className="activities-field">
                            <label>
                                Téléphone
                            </label>

                            <input
                                value={form.phone}
                                onChange={(event) =>
                                    updateForm(
                                        "phone",
                                        event.target.value
                                    )
                                }
                                placeholder="Téléphone"
                            />
                        </div>

                        <div className="activities-field">
                            <label>
                                Site web
                            </label>

                            <input
                                value={form.website}
                                onChange={(event) =>
                                    updateForm(
                                        "website",
                                        event.target.value
                                    )
                                }
                                placeholder="https://..."
                            />
                        </div>

                        <div className="activities-field activities-field-full">
                            <label>
                                Description
                            </label>

                            <textarea
                                value={form.description}
                                onChange={(event) =>
                                    updateForm(
                                        "description",
                                        event.target.value
                                    )
                                }
                                placeholder="Présentez brièvement cette activité."
                            />
                        </div>

                    </div>

                    <div className="activities-form-actions">

                        <button
                            type="submit"
                            className="activities-primary-button"
                            disabled={saving}
                        >
                            {saving
                                ? "Création..."
                                : "Créer l'activité"}
                        </button>

                        <button
                            type="button"
                            className="activities-secondary-button"
                            onClick={resetForm}
                            disabled={saving}
                        >
                            Annuler
                        </button>

                    </div>

                </form>
            )}

            {loading ? (

                <div className="activities-loading">
                    Chargement des activités...
                </div>

            ) : activities.length === 0 ? (

                <div className="activities-empty">
                    <h2>
                        Aucune activité
                    </h2>

                    <p>
                        Votre profil personnel est prêt.
                        Créez maintenant votre première activité NSIKAY.
                    </p>
                </div>

            ) : (

                <section className="activities-grid">

                    {activities.map((activity) => {

                        const certification =
                            activity.certification_status ||
                            "not_required";

                        const canTryActivate =
                            certification === "certified" &&
                            activity.status !== "active";

                        return (
                            <article
                                key={activity.id}
                                className={
                                    activity.id === selectedId
                                        ? "activity-card activity-card-selected"
                                        : "activity-card"
                                }
                            >

                                <div className="activity-card-top">

                                    <div>
                                        <h3>
                                            {activity.name}
                                        </h3>

                                        <div className="activity-type">
                                            {TYPE_LABELS[
                                                activity.activity_type
                                            ] ||
                                                activity.activity_type}
                                        </div>
                                    </div>

                                </div>

                                <span
                                    className={statusClass(
                                        activity.status
                                    )}
                                >
                                    {STATUS_LABELS[
                                        activity.status
                                    ] ||
                                        activity.status}
                                </span>

                                <span
                                    className={certificationClass(
                                        certification
                                    )}
                                >
                                    Certification :{" "}
                                    {CERTIFICATION_LABELS[
                                        certification
                                    ] ||
                                        certification}
                                </span>

                                <p className="activity-card-description">
                                    {activity.description ||
                                        "Aucune description renseignée."}
                                </p>

                                <div className="activity-card-meta">

                                    {activity.sector && (
                                        <div>
                                            <strong>
                                                Secteur :
                                            </strong>{" "}
                                            {activity.sector}
                                        </div>
                                    )}

                                    {activity.country && (
                                        <div>
                                            <strong>
                                                Pays :
                                            </strong>{" "}
                                            {activity.country}
                                        </div>
                                    )}

                                    {activity.city && (
                                        <div>
                                            <strong>
                                                Ville :
                                            </strong>{" "}
                                            {activity.city}
                                        </div>
                                    )}

                                    <div>
                                        <strong>
                                            Services :
                                        </strong>{" "}
                                        {activity.service_count ?? 0}
                                    </div>

                                    <div>
                                        <strong>
                                            Projets :
                                        </strong>{" "}
                                        {activity.project_count ?? 0}
                                    </div>

                                </div>

                                <div className="activity-card-actions">

                                    <button
                                        type="button"
                                        onClick={() =>
                                            setSelectedId(
                                                activity.id
                                            )
                                        }
                                    >
                                        Voir
                                    </button>

                                    {activity.status !== "active" && (
                                        <button
                                            type="button"
                                            disabled={!canTryActivate}
                                            title={
                                                certification !==
                                                "certified"
                                                    ? "La certification NSIKAY doit être approuvée avant activation."
                                                    : ""
                                            }
                                            onClick={() =>
                                                handleActivate(
                                                    activity
                                                )
                                            }
                                        >
                                            Activer
                                        </button>
                                    )}

                                </div>

                            </article>
                        );
                    })}

                </section>
            )}

        </div>
    );
}


