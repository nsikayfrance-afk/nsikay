import React, {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    listActivityCertifications,
    getActivityCertification,
    getActivityCertificationHistory,
    changeActivityCertification,
} from "../services/activities";

const STATUS_LABELS = {
    pending: "En attente",
    approved: "Approuvée",
    rejected: "Refusée",
    expired: "Expirée",
};

const STATUS_CLASS = {
    pending: "pending",
    approved: "approved",
    rejected: "rejected",
    expired: "expired",
};

const ACTION_LABELS = {
    approve: "Approuver",
    reject: "Refuser",
    reopen: "Remettre en attente",
    expire: "Expirer",
};

function formatDate(value) {
    if (!value) {
        return "—";
    }

    try {
        return new Date(value).toLocaleString("fr-FR");
    } catch {
        return value;
    }
}

function statusLabel(status) {
    return STATUS_LABELS[status] || status || "—";
}

export default function ActivityCertificationAuthority() {

    const [certifications, setCertifications] = useState([]);
    const [selectedId, setSelectedId] = useState(null);
    const [selectedCertification, setSelectedCertification] = useState(null);
    const [history, setHistory] = useState([]);

    const [statusFilter, setStatusFilter] = useState("all");
    const [search, setSearch] = useState("");

    const [loading, setLoading] = useState(true);
    const [detailLoading, setDetailLoading] = useState(false);
    const [actionLoading, setActionLoading] = useState(false);

    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const loadCertifications = async () => {

        setLoading(true);
        setError("");

        try {

            const data =
                await listActivityCertifications();

            setCertifications(
                Array.isArray(data)
                    ? data
                    : data?.results || []
            );

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de charger les certifications."
            );

        } finally {

            setLoading(false);
        }
    };

    const loadCertificationDetail = async (id) => {

        if (!id) {
            return;
        }

        setDetailLoading(true);
        setError("");

        try {

            const [
                certification,
                certificationHistory,
            ] = await Promise.all([
                getActivityCertification(id),
                getActivityCertificationHistory(id),
            ]);

            setSelectedCertification(
                certification
            );

            setHistory(
                Array.isArray(certificationHistory)
                    ? certificationHistory
                    : certificationHistory?.results || []
            );

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de charger la certification."
            );

        } finally {

            setDetailLoading(false);
        }
    };

    useEffect(() => {
        loadCertifications();
    }, []);

    useEffect(() => {

        if (selectedId) {
            loadCertificationDetail(
                selectedId
            );
        } else {
            setSelectedCertification(null);
            setHistory([]);
        }

    }, [selectedId]);

    const filteredCertifications = useMemo(() => {

        const normalizedSearch =
            search.trim().toLowerCase();

        return certifications.filter(
            (item) => {

                const matchesStatus =
                    statusFilter === "all" ||
                    item.status === statusFilter;

                if (!matchesStatus) {
                    return false;
                }

                if (!normalizedSearch) {
                    return true;
                }

                const haystack = [
                    item.activity_name,
                    item.activity,
                    item.activity_type,
                    item.document_reference,
                    String(item.id),
                    String(item.owner_id),
                ]
                    .filter(Boolean)
                    .join(" ")
                    .toLowerCase();

                return haystack.includes(
                    normalizedSearch
                );
            }
        );

    }, [
        certifications,
        statusFilter,
        search,
    ]);

    const counts = useMemo(() => {

        return {
            all: certifications.length,
            pending: certifications.filter(
                item => item.status === "pending"
            ).length,
            approved: certifications.filter(
                item => item.status === "approved"
            ).length,
            rejected: certifications.filter(
                item => item.status === "rejected"
            ).length,
            expired: certifications.filter(
                item => item.status === "expired"
            ).length,
        };

    }, [certifications]);

    const handleAction = async (action) => {

        if (!selectedCertification) {
            return;
        }

        const id =
            selectedCertification.id;

        let comment =
            "Action effectuée depuis l'espace Autorité Certification.";

        if (action === "approve") {
            comment =
                "Certification approuvée par l'Autorité Certification.";
        }

        if (action === "reject") {
            comment =
                "Certification refusée par l'Autorité Certification.";
        }

        if (action === "reopen") {
            comment =
                "Certification remise en attente par l'Autorité Certification.";
        }

        if (action === "expire") {
            comment =
                "Certification expirée par l'Autorité Certification.";
        }

        setActionLoading(true);
        setError("");
        setMessage("");

        try {

            await changeActivityCertification(
                id,
                action,
                comment
            );

            setMessage(
                `Action « ${ACTION_LABELS[action]} » exécutée avec succès.`
            );

            await loadCertifications();
            await loadCertificationDetail(id);

        } catch (err) {

            setError(
                err?.message ||
                "L'action de certification a échoué."
            );

        } finally {

            setActionLoading(false);
        }
    };

    return (
        <div style={styles.page}>

            <div style={styles.header}>

                <div>
                    <div style={styles.eyebrow}>
                        NSIKAY • CERTIFICATION
                    </div>

                    <h1 style={styles.title}>
                        Autorité Certification
                    </h1>

                    <p style={styles.subtitle}>
                        Contrôle, validation et suivi des
                        certifications d'activités.
                    </p>
                </div>

                <button
                    type="button"
                    onClick={loadCertifications}
                    disabled={loading}
                    style={styles.refreshButton}
                >
                    {loading
                        ? "Actualisation..."
                        : "Actualiser"}
                </button>

            </div>

            {error && (
                <div style={styles.error}>
                    {error}
                </div>
            )}

            {message && (
                <div style={styles.success}>
                    {message}
                </div>
            )}

            <div style={styles.statsGrid}>

                {[
                    ["all", "Toutes"],
                    ["pending", "En attente"],
                    ["approved", "Approuvées"],
                    ["rejected", "Refusées"],
                    ["expired", "Expirées"],
                ].map(([key, label]) => (

                    <button
                        key={key}
                        type="button"
                        onClick={() =>
                            setStatusFilter(key)
                        }
                        style={{
                            ...styles.statCard,
                            ...(statusFilter === key
                                ? styles.statCardActive
                                : {}),
                        }}
                    >
                        <span style={styles.statLabel}>
                            {label}
                        </span>

                        <strong style={styles.statValue}>
                            {counts[key]}
                        </strong>
                    </button>

                ))}

            </div>

            <div style={styles.workspace}>

                <section style={styles.listPanel}>

                    <div style={styles.panelHeader}>
                        <div>
                            <h2 style={styles.panelTitle}>
                                Demandes de certification
                            </h2>

                            <span style={styles.panelCount}>
                                {filteredCertifications.length}
                                {" "}résultat(s)
                            </span>
                        </div>
                    </div>

                    <div style={styles.searchBox}>

                        <input
                            type="search"
                            value={search}
                            onChange={(event) =>
                                setSearch(
                                    event.target.value
                                )
                            }
                            placeholder="Rechercher une activité..."
                            style={styles.input}
                        />

                    </div>

                    <div style={styles.list}>

                        {loading && (
                            <div style={styles.empty}>
                                Chargement des certifications...
                            </div>
                        )}

                        {!loading &&
                            filteredCertifications.length === 0 && (
                                <div style={styles.empty}>
                                    Aucune certification
                                    correspondant aux critères.
                                </div>
                            )}

                        {!loading &&
                            filteredCertifications.map(
                                (item) => (

                                    <button
                                        key={item.id}
                                        type="button"
                                        onClick={() =>
                                            setSelectedId(
                                                item.id
                                            )
                                        }
                                        style={{
                                            ...styles.listItem,
                                            ...(selectedId === item.id
                                                ? styles.listItemActive
                                                : {}),
                                        }}
                                    >

                                        <div style={styles.itemTop}>

                                            <strong>
                                                {item.activity_name ||
                                                    item.activity ||
                                                    "Activité sans nom"}
                                            </strong>

                                            <span
                                                style={{
                                                    ...styles.badge,
                                                    ...(
                                                        styles.badges[
                                                            STATUS_CLASS[
                                                                item.status
                                                            ] || "pending"
                                                        ]
                                                    ),
                                                }}
                                            >
                                                {statusLabel(
                                                    item.status
                                                )}
                                            </span>

                                        </div>

                                        <div style={styles.itemMeta}>
                                            Type :
                                            {" "}
                                            {item.activity_type || "—"}
                                            {" • "}
                                            ID :
                                            {" "}
                                            {item.activity_id || "—"}
                                        </div>

                                        <div style={styles.itemDate}>
                                            Créée le{" "}
                                            {formatDate(
                                                item.created_at
                                            )}
                                        </div>

                                    </button>

                                )
                            )}

                    </div>

                </section>

                <section style={styles.detailPanel}>

                    {!selectedId && (
                        <div style={styles.detailEmpty}>
                            <div style={styles.detailIcon}>
                                ✓
                            </div>

                            <h2>
                                Sélectionnez une certification
                            </h2>

                            <p>
                                Choisissez une demande dans la
                                liste pour consulter l'activité,
                                son statut et son historique.
                            </p>
                        </div>
                    )}

                    {selectedId &&
                        detailLoading && (
                            <div style={styles.detailEmpty}>
                                Chargement...
                            </div>
                        )}

                    {selectedCertification &&
                        !detailLoading && (

                            <div>

                                <div style={styles.detailHeader}>

                                    <div>
                                        <div style={styles.eyebrow}>
                                            ACTIVITÉ #{selectedCertification.activity_id}
                                        </div>

                                        <h2 style={styles.detailTitle}>
                                            {selectedCertification.activity_name ||
                                                selectedCertification.activity ||
                                                "Activité"}
                                        </h2>

                                        <div style={styles.detailType}>
                                            {selectedCertification.activity_type ||
                                                "Type non renseigné"}
                                        </div>
                                    </div>

                                    <span
                                        style={{
                                            ...styles.largeBadge,
                                            ...(
                                                styles.badges[
                                                    STATUS_CLASS[
                                                        selectedCertification.status
                                                    ] || "pending"
                                                ]
                                            ),
                                        }}
                                    >
                                        {statusLabel(
                                            selectedCertification.status
                                        )}
                                    </span>

                                </div>

                                <div style={styles.infoGrid}>

                                    <Info
                                        label="Propriétaire"
                                        value={
                                            selectedCertification.owner_id
                                        }
                                    />

                                    <Info
                                        label="Certification"
                                        value={
                                            selectedCertification.certification_type
                                        }
                                    />

                                    <Info
                                        label="Référence"
                                        value={
                                            selectedCertification.document_reference ||
                                            "—"
                                        }
                                    />

                                    <Info
                                        label="Créée le"
                                        value={
                                            formatDate(
                                                selectedCertification.created_at
                                            )
                                        }
                                    />

                                </div>

                                <div style={styles.actionsSection}>

                                    <h3 style={styles.sectionTitle}>
                                        Actions de certification
                                    </h3>

                                    <div style={styles.actions}>

                                        {selectedCertification.status === "pending" && (
                                            <>
                                                <button
                                                    type="button"
                                                    disabled={actionLoading}
                                                    onClick={() =>
                                                        handleAction(
                                                            "approve"
                                                        )
                                                    }
                                                    style={styles.approve}
                                                >
                                                    {actionLoading
                                                        ? "Traitement..."
                                                        : "Approuver"}
                                                </button>

                                                <button
                                                    type="button"
                                                    disabled={actionLoading}
                                                    onClick={() =>
                                                        handleAction(
                                                            "reject"
                                                        )
                                                    }
                                                    style={styles.reject}
                                                >
                                                    Refuser
                                                </button>
                                            </>
                                        )}

                                        {(
                                            selectedCertification.status ===
                                                "rejected" ||
                                            selectedCertification.status ===
                                                "expired"
                                        ) && (
                                            <button
                                                type="button"
                                                disabled={actionLoading}
                                                onClick={() =>
                                                    handleAction(
                                                        "reopen"
                                                    )
                                                }
                                                style={styles.secondaryAction}
                                            >
                                                Remettre en attente
                                            </button>
                                        )}

                                        {selectedCertification.status === "approved" && (
                                            <button
                                                type="button"
                                                disabled={actionLoading}
                                                onClick={() =>
                                                    handleAction(
                                                        "expire"
                                                    )
                                                }
                                                style={styles.secondaryAction}
                                            >
                                                Expirer
                                            </button>
                                        )}

                                    </div>

                                </div>

                                <div style={styles.historySection}>

                                    <h3 style={styles.sectionTitle}>
                                        Historique
                                    </h3>

                                    {history.length === 0 ? (
                                        <div style={styles.emptyHistory}>
                                            Aucun événement.
                                        </div>
                                    ) : (
                                        <div style={styles.timeline}>

                                            {history.map(
                                                (event) => (

                                                    <div
                                                        key={event.id}
                                                        style={styles.historyItem}
                                                    >

                                                        <div style={styles.timelineDot} />

                                                        <div>
                                                            <strong>
                                                                {statusLabel(
                                                                    event.new_status
                                                                )}
                                                            </strong>

                                                            <div
                                                                style={
                                                                    styles.historyMeta
                                                                }
                                                            >
                                                                {event.old_status
                                                                    ? `${statusLabel(event.old_status)} → `
                                                                    : ""}
                                                                {formatDate(
                                                                    event.created_at
                                                                )}
                                                            </div>

                                                            {event.comment && (
                                                                <p
                                                                    style={
                                                                        styles.historyComment
                                                                    }
                                                                >
                                                                    {event.comment}
                                                                </p>
                                                            )}
                                                        </div>

                                                    </div>

                                                )
                                            )}

                                        </div>
                                    )}

                                </div>

                            </div>

                        )}

                </section>

            </div>

        </div>
    );
}

function Info({label, value}) {
    return (
        <div style={styles.infoCard}>
            <span style={styles.infoLabel}>
                {label}
            </span>

            <strong style={styles.infoValue}>
                {value || "—"}
            </strong>
        </div>
    );
}

const styles = {
    page: {
        minHeight: "100%",
        padding: "32px",
        background: "#f5f7fb",
        color: "#111827",
        boxSizing: "border-box",
    },

    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: "24px",
        marginBottom: "24px",
    },

    eyebrow: {
        fontSize: "12px",
        fontWeight: 800,
        letterSpacing: "0.12em",
        color: "#2563eb",
        marginBottom: "8px",
    },

    title: {
        margin: 0,
        fontSize: "30px",
        lineHeight: 1.15,
    },

    subtitle: {
        margin: "10px 0 0",
        color: "#64748b",
        fontSize: "15px",
    },

    refreshButton: {
        border: "1px solid #dbe2ea",
        background: "#ffffff",
        borderRadius: "10px",
        padding: "11px 16px",
        fontWeight: 700,
        cursor: "pointer",
    },

    error: {
        marginBottom: "16px",
        padding: "13px 16px",
        borderRadius: "10px",
        background: "#fef2f2",
        border: "1px solid #fecaca",
        color: "#991b1b",
    },

    success: {
        marginBottom: "16px",
        padding: "13px 16px",
        borderRadius: "10px",
        background: "#f0fdf4",
        border: "1px solid #bbf7d0",
        color: "#166534",
    },

    statsGrid: {
        display: "grid",
        gridTemplateColumns:
            "repeat(5, minmax(0, 1fr))",
        gap: "12px",
        marginBottom: "20px",
    },

    statCard: {
        textAlign: "left",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        padding: "16px",
        background: "#ffffff",
        cursor: "pointer",
    },

    statCardActive: {
        border: "2px solid #2563eb",
        padding: "15px",
    },

    statLabel: {
        display: "block",
        color: "#64748b",
        fontSize: "13px",
        marginBottom: "7px",
    },

    statValue: {
        fontSize: "25px",
    },

    workspace: {
        display: "grid",
        gridTemplateColumns:
            "minmax(320px, 0.9fr) minmax(500px, 1.5fr)",
        gap: "20px",
        alignItems: "start",
    },

    listPanel: {
        background: "#ffffff",
        border: "1px solid #e2e8f0",
        borderRadius: "14px",
        overflow: "hidden",
    },

    detailPanel: {
        background: "#ffffff",
        border: "1px solid #e2e8f0",
        borderRadius: "14px",
        minHeight: "620px",
        padding: "24px",
        boxSizing: "border-box",
    },

    panelHeader: {
        padding: "20px 20px 12px",
    },

    panelTitle: {
        margin: 0,
        fontSize: "18px",
    },

    panelCount: {
        display: "block",
        marginTop: "5px",
        color: "#64748b",
        fontSize: "13px",
    },

    searchBox: {
        padding: "0 20px 16px",
    },

    input: {
        width: "100%",
        boxSizing: "border-box",
        border: "1px solid #dbe2ea",
        borderRadius: "9px",
        padding: "11px 12px",
        outline: "none",
        fontSize: "14px",
    },

    list: {
        borderTop: "1px solid #edf1f5",
        maxHeight: "620px",
        overflowY: "auto",
    },

    listItem: {
        display: "block",
        width: "100%",
        textAlign: "left",
        border: 0,
        borderBottom: "1px solid #edf1f5",
        background: "#ffffff",
        padding: "16px 20px",
        cursor: "pointer",
    },

    listItemActive: {
        background: "#eff6ff",
        boxShadow: "inset 3px 0 0 #2563eb",
    },

    itemTop: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "12px",
    },

    itemMeta: {
        marginTop: "8px",
        color: "#475569",
        fontSize: "12px",
    },

    itemDate: {
        marginTop: "5px",
        color: "#94a3b8",
        fontSize: "11px",
    },

    badge: {
        display: "inline-flex",
        alignItems: "center",
        padding: "4px 8px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 800,
        whiteSpace: "nowrap",
    },

    largeBadge: {
        display: "inline-flex",
        alignItems: "center",
        padding: "7px 12px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: 800,
        whiteSpace: "nowrap",
    },

    badges: {
        pending: {
            background: "#fff7ed",
            color: "#9a3412",
        },
        approved: {
            background: "#f0fdf4",
            color: "#166534",
        },
        rejected: {
            background: "#fef2f2",
            color: "#991b1b",
        },
        expired: {
            background: "#f1f5f9",
            color: "#475569",
        },
    },

    detailEmpty: {
        minHeight: "570px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        color: "#64748b",
        padding: "30px",
    },

    detailIcon: {
        width: "52px",
        height: "52px",
        display: "grid",
        placeItems: "center",
        borderRadius: "50%",
        background: "#eff6ff",
        color: "#2563eb",
        fontSize: "24px",
        fontWeight: 900,
        marginBottom: "16px",
    },

    detailHeader: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: "20px",
        paddingBottom: "20px",
        borderBottom: "1px solid #edf1f5",
    },

    detailTitle: {
        margin: 0,
        fontSize: "24px",
    },

    detailType: {
        marginTop: "7px",
        color: "#64748b",
        fontSize: "13px",
    },

    infoGrid: {
        display: "grid",
        gridTemplateColumns:
            "repeat(2, minmax(0, 1fr))",
        gap: "10px",
        marginTop: "20px",
    },

    infoCard: {
        border: "1px solid #e2e8f0",
        borderRadius: "10px",
        padding: "12px",
    },

    infoLabel: {
        display: "block",
        color: "#64748b",
        fontSize: "11px",
        marginBottom: "5px",
    },

    infoValue: {
        fontSize: "13px",
        wordBreak: "break-word",
    },

    actionsSection: {
        marginTop: "24px",
        paddingTop: "20px",
        borderTop: "1px solid #edf1f5",
    },

    sectionTitle: {
        margin: "0 0 12px",
        fontSize: "15px",
    },

    actions: {
        display: "flex",
        flexWrap: "wrap",
        gap: "10px",
    },

    approve: {
        border: 0,
        borderRadius: "9px",
        padding: "11px 17px",
        background: "#166534",
        color: "#ffffff",
        fontWeight: 800,
        cursor: "pointer",
    },

    reject: {
        border: 0,
        borderRadius: "9px",
        padding: "11px 17px",
        background: "#991b1b",
        color: "#ffffff",
        fontWeight: 800,
        cursor: "pointer",
    },

    secondaryAction: {
        border: "1px solid #cbd5e1",
        borderRadius: "9px",
        padding: "10px 16px",
        background: "#ffffff",
        color: "#334155",
        fontWeight: 700,
        cursor: "pointer",
    },

    historySection: {
        marginTop: "28px",
        paddingTop: "20px",
        borderTop: "1px solid #edf1f5",
    },

    timeline: {
        display: "flex",
        flexDirection: "column",
        gap: "14px",
    },

    historyItem: {
        display: "flex",
        gap: "12px",
    },

    timelineDot: {
        width: "9px",
        height: "9px",
        marginTop: "6px",
        borderRadius: "50%",
        background: "#2563eb",
        flex: "0 0 auto",
    },

    historyMeta: {
        marginTop: "4px",
        color: "#64748b",
        fontSize: "11px",
    },

    historyComment: {
        margin: "5px 0 0",
        color: "#475569",
        fontSize: "12px",
        lineHeight: 1.5,
    },

    empty: {
        padding: "30px 20px",
        textAlign: "center",
        color: "#64748b",
        fontSize: "13px",
    },

    emptyHistory: {
        padding: "15px",
        borderRadius: "9px",
        background: "#f8fafc",
        color: "#64748b",
        fontSize: "13px",
    },
};
