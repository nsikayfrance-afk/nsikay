import { useEffect, useState } from "react";
import { getTVChannels } from "../services/tv";

const CATEGORIES = [
    {
        key: "economie",
        title: "Économie",
        icon: "💼",
    },
    {
        key: "sport",
        title: "Sport & Loisirs",
        icon: "⚽",
    },
    {
        key: "culture",
        title: "Culture & Art",
        icon: "🎭",
    },
    {
        key: "technologie",
        title: "Technologie & Innovation",
        icon: "💡",
    },
    {
        key: "agriculture",
        title: "Agriculture & Agronomie",
        icon: "🌾",
    },
    {
        key: "social",
        title: "Social",
        icon: "🤝",
    },
    {
        key: "religion",
        title: "Religion & Histoire",
        icon: "📚",
    },
    {
        key: "adult",
        title: "+18",
        icon: "🔞",
    },
];

function normalizeResponse(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (Array.isArray(data?.results)) {
        return data.results;
    }

    if (Array.isArray(data?.channels)) {
        return data.channels;
    }

    if (Array.isArray(data?.data)) {
        return data.data;
    }

    return [];
}

function channelName(channel) {
    return (
        channel?.title ||
        channel?.name ||
        channel?.channel_name ||
        channel?.display_name ||
        "Chaîne NSIKAY"
    );
}

function channelDescription(channel) {
    return (
        channel?.description ||
        channel?.bio ||
        channel?.summary ||
        "Contenu audiovisuel NSIKAY."
    );
}

function channelImage(channel) {
    return (
        channel?.thumbnail ||
        channel?.logo ||
        channel?.logo_url ||
        channel?.image ||
        channel?.image_url ||
        channel?.cover ||
        null
    );
}

function channelStream(channel) {
    return (
        channel?.video_url ||
        channel?.stream_url ||
        channel?.streamUrl ||
        channel?.live_url ||
        channel?.liveUrl ||
        channel?.url ||
        null
    );
}

function channelCategory(channel) {
    return String(channel?.category || "").toLowerCase();
}

function isLive(channel) {
    return Boolean(channel?.is_live);
}

export default function TV() {
    const [channels, setChannels] = useState([]);
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let mounted = true;

        async function load() {
            try {
                setLoading(true);
                setError("");

                const data = await getTVChannels();
                const items = normalizeResponse(data);

                if (!mounted) return;

                setChannels(items);
                setSelected(items.length > 0 ? items[0] : null);
            } catch (err) {
                if (!mounted) return;

                setError(
                    err?.message ||
                    "Impossible de charger NSIKAY TV."
                );
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        }

        load();

        return () => {
            mounted = false;
        };
    }, []);

    return (
        <div style={styles.page}>

            <header style={styles.hero}>
                <div>
                    <div style={styles.brand}>📺 NSIKAY TV</div>

                    <h1 style={styles.title}>
                        Télévision NSIKAY
                    </h1>

                    <p style={styles.subtitle}>
                        Actualités, économie, culture, sport,
                        technologie, agriculture, social et histoire.
                    </p>
                </div>

                <div style={styles.liveBadge}>
                    <span style={styles.liveDot}></span>
                    NSIKAY TV
                </div>
            </header>

            <section style={styles.categories}>
                {CATEGORIES.map((category) => (
                    <button
                        key={category.key}
                        type="button"
                        style={styles.category}
                        onClick={() => {
                            const match = channels.find(
                                (channel) =>
                                    channelCategory(channel).includes(
                                        category.key
                                    )
                            );

                            if (match) {
                                setSelected(match);
                            }
                        }}
                    >
                        <span style={styles.categoryIcon}>
                            {category.icon}
                        </span>

                        <span>{category.title}</span>
                    </button>
                ))}
            </section>

            {loading && (
                <div style={styles.message}>
                    Chargement de NSIKAY TV...
                </div>
            )}

            {!loading && error && (
                <div style={styles.error}>
                    <strong>NSIKAY TV</strong>
                    <br />
                    {error}
                    <br />
                    <small>
                        API utilisée : /api/tv/channels/
                    </small>
                </div>
            )}

            {!loading && !error && channels.length === 0 && (
                <div style={styles.empty}>
                    <div style={styles.emptyIcon}>📺</div>

                    <h2>
                        Aucune chaîne disponible
                    </h2>

                    <p>
                        Le module TV Django est accessible,
                        mais aucune chaîne active n'est actuellement publiée.
                    </p>
                </div>
            )}

            {!loading && !error && channels.length > 0 && (
                <main className="nsikay-tv-page" style={styles.content}>

                    <section style={styles.playerPanel}>

                        {selected && (
                            <>
                                <div style={styles.player}>

                                    {channelStream(selected) ? (
                                        <video
                                            src={channelStream(selected)}
                                            controls
                                            style={styles.video}
                                        />
                                    ) : (
                                        <div style={styles.noStream}>
                                            <div style={styles.bigTv}>
                                                📺
                                            </div>

                                            <h2>
                                                {channelName(selected)}
                                            </h2>

                                            <p>
                                                Chaîne disponible.
                                                Le flux vidéo n'est pas encore renseigné.
                                            </p>
                                        </div>
                                    )}

                                </div>

                                <div style={styles.playerInfo}>

                                    <div>
                                        <h2 style={styles.channelTitle}>
                                            {channelName(selected)}
                                        </h2>

                                        <p style={styles.description}>
                                            {channelDescription(selected)}
                                        </p>
                                    </div>

                                    {isLive(selected) && (
                                        <span style={styles.livePill}>
                                            ● EN DIRECT
                                        </span>
                                    )}

                                </div>
                            </>
                        )}

                    </section>

                    <aside style={styles.channelPanel}>

                        <div style={styles.panelHeader}>
                            <h2>Chaînes</h2>
                            <span>{channels.length}</span>
                        </div>

                        <div style={styles.channelList}>

                            {channels.map((channel, index) => {

                                const active =
                                    selected === channel ||
                                    selected?.id === channel?.id;

                                const image =
                                    channelImage(channel);

                                return (
                                    <button
                                        key={
                                            channel?.id ??
                                            channel?.pk ??
                                            index
                                        }
                                        type="button"
                                        onClick={() =>
                                            setSelected(channel)
                                        }
                                        style={{
                                            ...styles.channelItem,
                                            ...(active
                                                ? styles.channelItemActive
                                                : {}),
                                        }}
                                    >

                                        <div style={styles.channelLogo}>

                                            {image ? (
                                                <img
                                                    src={image}
                                                    alt={channelName(channel)}
                                                    style={styles.logoImage}
                                                />
                                            ) : (
                                                "📺"
                                            )}

                                        </div>

                                        <div style={styles.channelText}>

                                            <strong>
                                                {channelName(channel)}
                                            </strong>

                                            <span>
                                                {channelDescription(channel)}
                                            </span>

                                        </div>

                                        {isLive(channel) && (
                                            <span style={styles.liveMini}>
                                                LIVE
                                            </span>
                                        )}

                                    </button>
                                );
                            })}

                        </div>

                    </aside>

                </main>
            )}

            <section style={styles.footerSections}>

                <div style={styles.footerCard}>
                    <span>📅</span>

                    <div>
                        <strong>Événements</strong>

                        <p>
                            Conférences, émissions et programmes NSIKAY.
                        </p>
                    </div>
                </div>

                <div style={styles.footerCard}>
                    <span>📢</span>

                    <div>
                        <strong>Publicité</strong>

                        <p>
                            Espaces publicitaires intégrés à l'écosystème TV.
                        </p>
                    </div>
                </div>

                <div style={styles.footerCard}>
                    <span>🎥</span>

                    <div>
                        <strong>Lives</strong>

                        <p>
                            Diffusions en direct lorsque le flux est disponible.
                        </p>
                    </div>
                </div>

            </section>

        </div>
    );
}

const styles = {
    page: {
        minHeight: "100vh",
        background:
            "linear-gradient(180deg, #07111f 0%, #0c1728 45%, #f5f7fa 45%, #f5f7fa 100%)",
        color: "#172033",
        paddingBottom: "50px",
    },

    hero: {
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "55px 28px 45px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "30px",
        color: "white",
    },

    brand: {
        fontSize: "16px",
        fontWeight: 800,
        letterSpacing: "2px",
        marginBottom: "10px",
    },

    title: {
        margin: 0,
        fontSize: "clamp(32px, 5vw, 58px)",
        fontWeight: 900,
    },

    subtitle: {
        maxWidth: "760px",
        fontSize: "18px",
        lineHeight: 1.6,
        opacity: 0.82,
    },

    liveBadge: {
        border: "1px solid rgba(255,255,255,.35)",
        borderRadius: "999px",
        padding: "12px 18px",
        whiteSpace: "nowrap",
        fontWeight: 800,
    },

    liveDot: {
        display: "inline-block",
        width: "9px",
        height: "9px",
        borderRadius: "50%",
        background: "#e31b23",
        marginRight: "8px",
    },

    categories: {
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "0 28px 35px",
        display: "grid",
        gridTemplateColumns:
            "repeat(auto-fit, minmax(150px, 1fr))",
        gap: "12px",
    },

    category: {
        border: "1px solid rgba(255,255,255,.18)",
        borderRadius: "14px",
        background: "rgba(255,255,255,.08)",
        color: "white",
        padding: "16px 12px",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "8px",
        fontWeight: 700,
    },

    categoryIcon: {
        fontSize: "25px",
    },

    content: {
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "30px 28px",
        display: "grid",
        gridTemplateColumns:
            "minmax(0, 1fr) 360px",
        gap: "22px",
    },

    playerPanel: {
        background: "white",
        borderRadius: "20px",
        overflow: "hidden",
        boxShadow:
            "0 15px 45px rgba(0,0,0,.12)",
    },

    player: {
        aspectRatio: "16 / 9",
        background: "#02060b",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },

    video: {
        width: "100%",
        height: "100%",
        objectFit: "contain",
    },

    noStream: {
        width: "100%",
        minHeight: "320px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        padding: "30px",
        color: "white",
        background: "#0b1320",
    },

    bigTv: {
        fontSize: "60px",
        marginBottom: "15px",
    },

    playerInfo: {
        padding: "22px",
        display: "flex",
        justifyContent: "space-between",
        gap: "20px",
        alignItems: "flex-start",
    },

    channelTitle: {
        margin: 0,
        fontSize: "25px",
    },

    description: {
        margin: "8px 0 0",
        color: "#667085",
        lineHeight: 1.5,
    },

    livePill: {
        background: "#e31b23",
        color: "white",
        padding: "8px 12px",
        borderRadius: "999px",
        fontWeight: 800,
        fontSize: "12px",
        whiteSpace: "nowrap",
    },

    channelPanel: {
        background: "white",
        borderRadius: "20px",
        padding: "18px",
        boxShadow:
            "0 15px 45px rgba(0,0,0,.12)",
    },

    panelHeader: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "12px",
    },

    channelList: {
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        maxHeight: "620px",
        overflowY: "auto",
    },

    channelItem: {
        width: "100%",
        border: "1px solid #e5e7eb",
        borderRadius: "12px",
        background: "white",
        padding: "10px",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: "10px",
        textAlign: "left",
    },

    channelItemActive: {
        border: "2px solid #172033",
        background: "#f5f7fa",
    },

    channelLogo: {
        width: "48px",
        height: "48px",
        borderRadius: "10px",
        background: "#edf1f5",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
        overflow: "hidden",
        fontSize: "22px",
    },

    logoImage: {
        width: "100%",
        height: "100%",
        objectFit: "cover",
    },

    channelText: {
        minWidth: 0,
        display: "flex",
        flexDirection: "column",
        gap: "3px",
        flex: 1,
    },

    liveMini: {
        fontSize: "10px",
        fontWeight: 900,
        color: "#e31b23",
    },

    message: {
        maxWidth: "900px",
        margin: "30px auto",
        background: "white",
        borderRadius: "16px",
        padding: "30px",
        textAlign: "center",
    },

    error: {
        maxWidth: "900px",
        margin: "30px auto",
        background: "#fff1f2",
        color: "#9f1239",
        border: "1px solid #fecdd3",
        borderRadius: "16px",
        padding: "25px",
        lineHeight: 1.7,
    },

    empty: {
        maxWidth: "900px",
        margin: "30px auto",
        background: "white",
        borderRadius: "20px",
        padding: "50px",
        textAlign: "center",
        boxShadow:
            "0 15px 45px rgba(0,0,0,.08)",
    },

    emptyIcon: {
        fontSize: "65px",
    },

    footerSections: {
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "0 28px",
        display: "grid",
        gridTemplateColumns:
            "repeat(auto-fit, minmax(250px, 1fr))",
        gap: "15px",
    },

    footerCard: {
        background: "white",
        borderRadius: "16px",
        padding: "20px",
        display: "flex",
        gap: "15px",
        boxShadow:
            "0 8px 30px rgba(0,0,0,.07)",
    },
};
