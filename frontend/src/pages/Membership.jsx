import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { QRCodeSVG } from "qrcode.react";
import membershipApi from "../services/membership";

function formatAmount(amount) {
    if (amount === null || amount === undefined) {
        return "—";
    }

    return `${Number(amount).toLocaleString("fr-FR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })} €`;
}

function statusLabel(status) {
    const labels = {
        pending: "En attente",
        approved_pending_payment: "Cotisation attendue",
        approved: "Validée",
        refused: "Refusée",
        cancelled: "Annulée",
        active: "Actif",
        suspended: "Suspendu",
        expired: "Expirée",
    };

    return labels[status] || status || "—";
}

function getVerificationUrl(path) {
    if (!path) {
        return "";
    }

    if (/^https?:\/\//i.test(path)) {
        return path;
    }

    return `${window.location.origin}${path}`;
}

export default function Membership() {
    const [types, setTypes] = useState([]);
    const [membership, setMembership] = useState(null);
    const [applications, setApplications] = useState([]);
    const [card, setCard] = useState(null);

    const [loading, setLoading] = useState(true);
    const [applying, setApplying] = useState(false);

    const [selectedType, setSelectedType] = useState("");
    const [message, setMessage] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function loadMembership() {
        setLoading(true);
        setError("");

        try {
            const [
                typesResponse,
                membershipResponse,
                applicationsResponse,
                cardResponse,
            ] = await Promise.all([
                membershipApi.types(),
                membershipApi.me(),
                membershipApi.applications(),
                membershipApi.card(),
            ]);

            const loadedTypes =
                Array.isArray(typesResponse)
                    ? typesResponse
                    : typesResponse?.results ||
                      typesResponse?.types ||
                      [];

            setTypes(loadedTypes);

            setMembership(
                membershipResponse?.member ||
                membershipResponse?.membership ||
                membershipResponse ||
                null
            );

            const loadedApplications =
                Array.isArray(applicationsResponse)
                    ? applicationsResponse
                    : applicationsResponse?.results ||
                      applicationsResponse?.applications ||
                      [];

            setApplications(loadedApplications);

            setCard(
                cardResponse?.card ||
                (
                    cardResponse?.member_number
                        ? cardResponse
                        : null
                )
            );

            if (
                !selectedType &&
                loadedTypes.length > 0
            ) {
                setSelectedType(
                    String(loadedTypes[0].id)
                );
            }
        } catch (err) {
            setError(
                err?.message ||
                "Impossible de charger les informations d’adhésion."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadMembership();
    }, []);

    async function handleApply(event) {
        event.preventDefault();

        if (!selectedType) {
            setError(
                "Sélectionnez une catégorie d’adhésion."
            );
            return;
        }

        setApplying(true);
        setError("");
        setSuccess("");

        try {
            await membershipApi.apply(
                Number(selectedType),
                message
            );

            setMessage("");

            setSuccess(
                "Votre demande d’adhésion a été enregistrée. " +
                "Elle doit maintenant être traitée par l’administration."
            );

            await loadMembership();
        } catch (err) {
            setError(
                err?.message ||
                "Impossible d’enregistrer la demande d’adhésion."
            );
        } finally {
            setApplying(false);
        }
    }

    const hasPendingApplication =
        applications.some(
            (item) =>
                item.status === "pending" ||
                item.status === "approved_pending_payment"
        );

    const isActive =
        membership?.status === "active" ||
        membership?.member_status === "active";

    const verificationUrl =
        getVerificationUrl(card?.verification_path);

    return (
        <div className="ns-app">
            <header className="simple-header">
                <Link
                    to="/mon-profil"
                    className="ns-logo"
                >
                    <span className="logo-symbol">
                        N
                    </span>

                    <span>
                        <strong>NSIKAY</strong>
                        <small>Adhésion</small>
                    </span>
                </Link>

                <Link
                    to="/mon-profil"
                    className="back-link"
                >
                    ← Mon profil
                </Link>
            </header>

            <main className="content-page">
                <div className="profile-cover">
                    <div className="profile-avatar">
                        NS
                    </div>

                    <div>
                        <span className="eyebrow">
                            ASSOCIATION NSIKAY
                        </span>

                        <h1>
                            Adhésion et carte membre
                        </h1>

                        <p>
                            Gérez votre demande d’adhésion,
                            votre statut et votre carte officielle.
                        </p>
                    </div>
                </div>

                {error && (
                    <div className="info-card">
                        <strong>Erreur</strong>
                        <p>{error}</p>
                    </div>
                )}

                {success && (
                    <div className="info-card">
                        <strong>Demande enregistrée</strong>
                        <p>{success}</p>
                    </div>
                )}

                {loading ? (
                    <section className="three-space">
                        <article>
                            <h2>Chargement...</h2>
                            <p>
                                Récupération de vos informations
                                d’adhésion.
                            </p>
                        </article>
                    </section>
                ) : (
                    <>
                        <section className="profile-information">
                            <div className="info-card">
                                <span>Statut</span>
                                <strong>
                                    {isActive
                                        ? "Membre actif"
                                        : membership
                                            ? statusLabel(
                                                membership.status
                                            )
                                            : "Non membre"}
                                </strong>
                            </div>

                            <div className="info-card">
                                <span>Catégorie</span>
                                <strong>
                                    {
                                        membership
                                            ?.membership_type_detail
                                            ?.name ||
                                        membership
                                            ?.membership_type_name ||
                                        "Aucune"
                                    }
                                </strong>
                            </div>

                            <div className="info-card">
                                <span>Numéro membre</span>
                                <strong>
                                    {card?.member_number ||
                                        "Non attribué"}
                                </strong>
                            </div>

                            <div className="info-card">
                                <span>Carte</span>
                                <strong>
                                    {card
                                        ? statusLabel(card.status)
                                        : "Non disponible"}
                                </strong>
                            </div>
                        </section>

                        {card && (
                            <section
                                className="profile-information"
                            >
                                <div
                                    className="info-card"
                                    style={{
                                        gridColumn: "1 / -1",
                                        maxWidth: "720px",
                                        margin: "0 auto",
                                        width: "100%",
                                    }}
                                >
                                    <div
                                        style={{
                                            border: "1px solid rgba(0,0,0,.12)",
                                            borderRadius: "18px",
                                            padding: "24px",
                                            background: "#fff",
                                        }}
                                    >
                                        <div
                                            style={{
                                                display: "flex",
                                                justifyContent: "space-between",
                                                gap: "24px",
                                                flexWrap: "wrap",
                                                alignItems: "flex-start",
                                            }}
                                        >
                                            <div>
                                                <span
                                                    className="eyebrow"
                                                >
                                                    NSIKAY
                                                </span>

                                                <h2>
                                                    CARTE DE MEMBRE
                                                </h2>

                                                <p>
                                                    Association déclarée
                                                    en France
                                                </p>

                                                <p>
                                                    <strong>
                                                        RNA :
                                                    </strong>{" "}
                                                    W442031317
                                                </p>

                                                <p>
                                                    <strong>
                                                        SIREN :
                                                    </strong>{" "}
                                                    995 089 711
                                                </p>

                                                <p>
                                                    <strong>
                                                        SIRET :
                                                    </strong>{" "}
                                                    995 089 711 00015
                                                </p>
                                            </div>

                                            {verificationUrl && (
                                                <div
                                                    style={{
                                                        textAlign: "center",
                                                    }}
                                                >
                                                    <QRCodeSVG
                                                        value={
                                                            verificationUrl
                                                        }
                                                        size={170}
                                                        level="H"
                                                        includeMargin={true}
                                                    />

                                                    <small
                                                        style={{
                                                            display: "block",
                                                            marginTop: "8px",
                                                        }}
                                                    >
                                                        Scanner pour
                                                        vérifier la carte
                                                    </small>
                                                </div>
                                            )}
                                        </div>

                                        <hr />

                                        <div
                                            className="profile-information"
                                            style={{
                                                marginTop: "16px",
                                            }}
                                        >
                                            <div className="info-card">
                                                <span>
                                                    Numéro membre
                                                </span>

                                                <strong>
                                                    {
                                                        card.member_number
                                                    }
                                                </strong>
                                            </div>

                                            <div className="info-card">
                                                <span>
                                                    Catégorie
                                                </span>

                                                <strong>
                                                    {
                                                        membership
                                                            ?.membership_type_detail
                                                            ?.name ||
                                                        membership
                                                            ?.membership_type_name ||
                                                        "Membre"
                                                    }
                                                </strong>
                                            </div>

                                            <div className="info-card">
                                                <span>
                                                    Statut
                                                </span>

                                                <strong>
                                                    {statusLabel(
                                                        card.status
                                                    )}
                                                </strong>
                                            </div>

                                            <div className="info-card">
                                                <span>
                                                    Émise le
                                                </span>

                                                <strong>
                                                    {card.issued_at
                                                        ? new Date(
                                                            card.issued_at
                                                        ).toLocaleDateString(
                                                            "fr-FR"
                                                        )
                                                        : "—"}
                                                </strong>
                                            </div>
                                        </div>

                                        {verificationUrl && (
                                            <div
                                                style={{
                                                    marginTop: "20px",
                                                }}
                                            >
                                                <a
                                                    href={
                                                        verificationUrl
                                                    }
                                                    target="_blank"
                                                    rel="noreferrer"
                                                >
                                                    Vérifier cette carte
                                                    →
                                                </a>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </section>
                        )}

                        {!isActive &&
                            !hasPendingApplication && (
                                <section
                                    className="profile-information"
                                >
                                    <div
                                        className="info-card"
                                        style={{
                                            gridColumn: "1 / -1",
                                        }}
                                    >
                                        <span>
                                            DEMANDE D’ADHÉSION
                                        </span>

                                        <h2>
                                            Choisissez votre catégorie
                                        </h2>

                                        <p>
                                            La création d’un compte NSIKAY
                                            ne crée pas automatiquement
                                            une adhésion.
                                        </p>

                                        <form
                                            onSubmit={handleApply}
                                        >
                                            <div
                                                style={{
                                                    display: "grid",
                                                    gap: "12px",
                                                    marginTop: "18px",
                                                }}
                                            >
                                                {types.map(
                                                    (type) => (
                                                        <label
                                                            key={type.id}
                                                            style={{
                                                                display:
                                                                    "flex",
                                                                gap: "12px",
                                                                alignItems:
                                                                    "center",
                                                                cursor:
                                                                    "pointer",
                                                            }}
                                                        >
                                                            <input
                                                                type="radio"
                                                                name="membership_type"
                                                                value={
                                                                    type.id
                                                                }
                                                                checked={
                                                                    String(
                                                                        selectedType
                                                                    ) ===
                                                                    String(
                                                                        type.id
                                                                    )
                                                                }
                                                                onChange={() =>
                                                                    setSelectedType(
                                                                        String(
                                                                            type.id
                                                                        )
                                                                    )
                                                                }
                                                            />

                                                            <span>
                                                                <strong>
                                                                    {
                                                                        type.name
                                                                    }
                                                                </strong>

                                                                {" — "}

                                                                {formatAmount(
                                                                    type.contribution_required
                                                                )}
                                                            </span>
                                                        </label>
                                                    )
                                                )}
                                            </div>

                                            <textarea
                                                value={message}
                                                onChange={(
                                                    event
                                                ) =>
                                                    setMessage(
                                                        event.target
                                                            .value
                                                    )
                                                }
                                                placeholder="Message facultatif pour l’administration"
                                                rows={4}
                                                style={{
                                                    width: "100%",
                                                    marginTop: "18px",
                                                }}
                                            />

                                            <button
                                                type="submit"
                                                disabled={applying}
                                                style={{
                                                    marginTop: "18px",
                                                }}
                                            >
                                                {applying
                                                    ? "Enregistrement..."
                                                    : "Demander l’adhésion"}
                                            </button>
                                        </form>
                                    </div>
                                </section>
                            )}

                        {hasPendingApplication && (
                            <section className="three-space">
                                <article>
                                    <span>📋</span>

                                    <h2>
                                        Demande en cours
                                    </h2>

                                    <p>
                                        Une demande d’adhésion est
                                        actuellement en cours de traitement.
                                    </p>
                                </article>
                            </section>
                        )}

                        {applications.length > 0 && (
                            <section
                                className="profile-information"
                            >
                                <div
                                    className="info-card"
                                    style={{
                                        gridColumn: "1 / -1",
                                    }}
                                >
                                    <span>
                                        HISTORIQUE DES DEMANDES
                                    </span>

                                    {applications.map(
                                        (application) => (
                                            <div
                                                key={
                                                    application.id
                                                }
                                                style={{
                                                    padding:
                                                        "12px 0",
                                                    borderBottom:
                                                        "1px solid rgba(0,0,0,.08)",
                                                }}
                                            >
                                                <strong>
                                                    {
                                                        application
                                                            .membership_type_detail
                                                            ?.name
                                                    }
                                                </strong>

                                                <p>
                                                    Statut :{" "}
                                                    {statusLabel(
                                                        application.status
                                                    )}
                                                </p>

                                                <small>
                                                    {application.created_at
                                                        ? new Date(
                                                            application.created_at
                                                        ).toLocaleString(
                                                            "fr-FR"
                                                        )
                                                        : ""}
                                                </small>
                                            </div>
                                        )
                                    )}
                                </div>
                            </section>
                        )}
                    </>
                )}
            </main>
        </div>
    );
}
