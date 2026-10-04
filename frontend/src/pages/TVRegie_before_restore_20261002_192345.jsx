import React, { useEffect, useMemo, useState } from "react";
import LocalCameraSource from "../components/LocalCameraSource";
import {
    getCameras,
    createCamera,
    updateCamera,
    deleteCamera,
    getStreams,
    createStream,
    deleteStream,
    publishStream,
    unpublishStream,
    getEffects,
    createEffect,
    deleteEffect,
    getAnimations,
    createAnimation,
    deleteAnimation,
    getAudioControls,
    createAudioControl,
    deleteAudioControl,
    getScenes,
    createScene,
    deleteScene,
    getSchedules,
    createSchedule,
    deleteSchedule,
    getCentralBroadcasts,
    getCentralBroadcast,
    createCentralBroadcast,
    updateCentralBroadcast,
    startCentralBroadcast,
    stopCentralBroadcast,
    deleteCentralBroadcast,
} from "../services/tvRegie";
import { getTVChannels } from "../services/tv";
import { getMediaAsset, getMediaAssets, getMediaDestinations } from "../services/mediaLibrary";

const CATEGORY = {
    background: "#07111f",
    panel: "#0d1b2a",
    panel2: "#101f31",
    border: "#23364b",
    text: "#eef5ff",
    muted: "#91a4b8",
    accent: "#2f80ed",
    danger: "#d64545",
    success: "#27ae60",
    warning: "#f2a93b",
};

function unwrap(response) {
    if (!response) return [];
    if (Array.isArray(response)) return response;
    if (Array.isArray(response.data)) return response.data;
    if (Array.isArray(response.results)) return response.results;
    if (Array.isArray(response.data?.results)) return response.data.results;
    return [];
}

function sourceName(source) {
    return source?.name || source?.title || `SOURCE ${source?.id ?? ""}`;
}

function getVideoUrl(source) {
    if (!source) return "";
    return source.stream_url || source.source_url || "";
}

function isBrowserVideo(url) {
    if (!url) return false;
    const value = url.toLowerCase();
    return (
        value.startsWith("http://") ||
        value.startsWith("https://") ||
        value.startsWith("blob:")
    );
}

function SourcePreview({ source, label, compact = false }) {
    const url = getVideoUrl(source);

    return (
        <div
            style={{
                position: "relative",
                width: "100%",
                height: compact ? 115 : "100%",
                minHeight: compact ? 115 : 280,
                background: "#02070d",
                border: `1px solid ${CATEGORY.border}`,
                overflow: "hidden",
                borderRadius: 8,
            }}
        >
            {url && isBrowserVideo(url) ? (
                <video
                    src={url}
                    muted
                    autoPlay
                    playsInline
                    controls={false}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        display: "block",
                    }}
                />
            ) : (
                <div
                    style={{
                        height: "100%",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        flexDirection: "column",
                        color: CATEGORY.muted,
                        padding: 15,
                        textAlign: "center",
                    }}
                >
                    <div style={{ fontSize: 30, marginBottom: 8 }}>▣</div>
                    <strong style={{ color: CATEGORY.text }}>
                        {sourceName(source)}
                    </strong>
                    <small style={{ marginTop: 5 }}>
                        Aperçu vidéo non disponible
                    </small>
                    {url && (
                        <small style={{ marginTop: 4 }}>
                            Source enregistrée
                        </small>
                    )}
                </div>
            )}

            <div
                style={{
                    position: "absolute",
                    left: 8,
                    top: 8,
                    background: "rgba(0,0,0,.72)",
                    borderRadius: 5,
                    padding: "4px 7px",
                    fontSize: 11,
                    fontWeight: 700,
                }}
            >
                {label}
            </div>
        </div>
    );
}

function ControlButton({
    children,
    onClick,
    active = false,
    danger = false,
    success = false,
    disabled = false,
}) {
    return (
        <button
            type="button"
            disabled={disabled}
            onClick={onClick}
            style={{
                border: `1px solid ${
                    danger
                        ? CATEGORY.danger
                        : success
                          ? CATEGORY.success
                          : active
                            ? CATEGORY.accent
                            : CATEGORY.border
                }`,
                background: danger
                    ? "rgba(214,69,69,.18)"
                    : success
                      ? "rgba(39,174,96,.18)"
                      : active
                        ? "rgba(47,128,237,.24)"
                        : CATEGORY.panel2,
                color: CATEGORY.text,
                borderRadius: 7,
                padding: "9px 13px",
                cursor: disabled ? "not-allowed" : "pointer",
                opacity: disabled ? 0.5 : 1,
                fontWeight: 700,
                fontSize: 12,
                whiteSpace: "nowrap",
            }}
        >
            {children}
        </button>
    );
}

function Panel({ title, children, right }) {
    return (
        <section
            style={{
                background: CATEGORY.panel,
                border: `1px solid ${CATEGORY.border}`,
                borderRadius: 10,
                overflow: "hidden",
            }}
        >
            <div
                style={{
                    minHeight: 42,
                    padding: "10px 13px",
                    borderBottom: `1px solid ${CATEGORY.border}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: 10,
                }}
            >
                <strong>{title}</strong>
                {right}
            </div>
            <div style={{ padding: 12 }}>{children}</div>
        </section>
    );
}


function NSIKAYRealCameraPanel() {
    const [stream, setStream] = React.useState(null);

    return (
        <div
            style={{
                margin: "12px 0",
                padding: 10,
                border: "1px solid #29435f",
                borderRadius: 9,
                background: "#081321",
            }}
        >
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    marginBottom: 8,
                }}
            >
                <div>
                    <div
                        style={{
                            fontWeight: 900,
                            fontSize: 13,
                        }}
                    >
                        SOURCES RÉELLES
                    </div>

                    <div
                        style={{
                            color: "#8295aa",
                            fontSize: 10,
                            marginTop: 2,
                        }}
                    >
                        Webcam PC disponible pour la production
                    </div>
                </div>

                <div
                    style={{
                        padding: "4px 7px",
                        borderRadius: 4,
                        background: stream
                            ? "rgba(35,170,95,.16)"
                            : "rgba(120,140,160,.10)",
                        color: stream
                            ? "#65dc9a"
                            : "#8194a8",
                        fontSize: 9,
                        fontWeight: 900,
                    }}
                >
                    {stream
                        ? "● CAM PC PRÊTE"
                        : "○ CAM PC OFF"}
                </div>
            </div>

            <LocalCameraSource
                sourceName="CAM PC 1"
                compact={true}
                onStreamReady={setStream}
            />

            <div
                style={{
                    marginTop: 7,
                    fontSize: 10,
                    color: "#8194a8",
                }}
            >
                {stream
                    ? "La source caméra locale est active dans cette Régie."
                    : "Connectez la webcam pour la rendre disponible comme source locale."}
            </div>
        </div>
    );
}

/* ============================================================
   NSIKAY_EDITORIAL_BROADCAST
   Moteur de destinations éditoriales de la Régie
   ============================================================ */

const NSIKAY_EDITORIAL_BROADCAST = [
    {
        id: "tv",
        label: "NSIKAY TV",
        short: "TV",
        type: "tv",
    },
    {
        id: "economie",
        label: "Économie",
        short: "ECO",
        type: "editorial",
    },
    {
        id: "sport",
        label: "Sport & Loisirs",
        short: "SPORT",
        type: "editorial",
    },
    {
        id: "culture",
        label: "Culture & Art",
        short: "CULTURE",
        type: "editorial",
    },
    {
        id: "technologie",
        label: "Technologie & Innovation",
        short: "TECH",
        type: "editorial",
    },
    {
        id: "agriculture",
        label: "Agriculture & Agronomie",
        short: "AGRI",
        type: "editorial",
    },
    {
        id: "social",
        label: "Social",
        short: "SOCIAL",
        type: "editorial",
    },
    {
        id: "religion",
        label: "Religion & Histoire",
        short: "HIST",
        type: "editorial",
    },
    {
        id: "adult",
        label: "+18",
        short: "+18",
        type: "editorial",
    },
    {
        id: "evenements",
        label: "Événements",
        short: "EVENT",
        type: "event",
    },
    {
        id: "publicite",
        label: "Publicité",
        short: "PUB",
        type: "advertising",
    },
];

function NSIKAYEditorialBroadcastPanel() {
    const [onAir, setOnAir] = React.useState(false);

    const [selectedDestinations, setSelectedDestinations] =
        React.useState(["tv"]);
    const [djangoDestinations, setDjangoDestinations] =
        React.useState([]);

    const [destinationsLoading, setDestinationsLoading] =
        React.useState(false);

    const [destinationsError, setDestinationsError] =
        React.useState("");


    const [broadcastTitle, setBroadcastTitle] =
        React.useState("Programme NSIKAY");

    const [sourceUrl, setSourceUrl] =
        React.useState("");

    const [broadcastId, setBroadcastId] =
        React.useState(null);

    const [broadcastStatus, setBroadcastStatus] =
        React.useState("DRAFT");

    const [broadcastBusy, setBroadcastBusy] =
        React.useState(false);

    const [broadcastMessage, setBroadcastMessage] =
        React.useState(
            "Sélectionnez les destinations puis lancez la diffusion."
        );
    // ========================================================
    // BIBLIOTHEQUE MEDIA
    // ========================================================

    const [mediaLoading, setMediaLoading] =
        React.useState(false);

    const [loadedMediaId, setLoadedMediaId] =
        React.useState(null);

    const [loadedMediaTitle, setLoadedMediaTitle] =
        React.useState("");
    // ========================================================
    // SELECTEUR BIBLIOTHEQUE MEDIA DANS LA REGIE
    // ========================================================

    const [libraryAssets, setLibraryAssets] =
        React.useState([]);

    const [libraryLoading, setLibraryLoading] =
        React.useState(false);

    const [librarySearch, setLibrarySearch] =
        React.useState("");

    const [libraryType, setLibraryType] =
        React.useState("ALL");

    const [librarySelectedId, setLibrarySelectedId] =
        React.useState(null);

    const [libraryMessage, setLibraryMessage] =
        React.useState("");




    // ========================================================
    // DESTINATIONS DJANGO -> REGIE
    // ========================================================

    useEffect(() => {
        let cancelled = false;

        async function loadDestinations() {
            try {
                setDestinationsLoading(true);
                setDestinationsError("");

                const response =
                    await getMediaDestinations();

                const payload =
                    response?.data || response || {};

                const items = Array.isArray(payload)
                    ? payload
                    : Array.isArray(payload.results)
                        ? payload.results
                        : Array.isArray(payload.destinations)
                            ? payload.destinations
                            : [];

                const activeItems = items.filter(
                    (item) => item.active !== false
                );

                if (!cancelled) {
                    setDjangoDestinations(activeItems);

                    if (activeItems.length > 0) {
                        const hasCurrentTV =
                            activeItems.some(
                                (item) =>
                                    item.code === "nsikay_tv"
                            );

                        if (hasCurrentTV) {
                            setSelectedDestinations(
                                (current) =>
                                    current.length > 0
                                        ? current
                                        : ["nsikay_tv"]
                            );
                        }
                    }
                }
            } catch (error) {
                console.error(
                    "Erreur destinations Django -> Régie :",
                    error
                );

                if (!cancelled) {
                    setDestinationsError(
                        "Les destinations Django sont momentanément indisponibles."
                    );
                }
            } finally {
                if (!cancelled) {
                    setDestinationsLoading(false);
                }
            }
        }

        loadDestinations();

        return () => {
            cancelled = true;
        };
    }, []);
    // ========================================================
    // BIBLIOTHEQUE MEDIA DANS LA REGIE
    // ========================================================

    useEffect(() => {
        let cancelled = false;

        async function loadLibraryAssets() {
            try {
                setLibraryLoading(true);

                const response = await getMediaAssets({
                    search: librarySearch || undefined,
                    asset_type:
                        libraryType !== "ALL"
                            ? libraryType
                            : undefined,
                });

                const payload =
                    response?.data || response || {};

                const items = Array.isArray(payload)
                    ? payload
                    : Array.isArray(payload.results)
                        ? payload.results
                        : Array.isArray(payload.assets)
                            ? payload.assets
                            : [];

                if (!cancelled) {
                    setLibraryAssets(items);
                }
            } catch (error) {
                console.error(
                    "Erreur chargement Bibliothèque Média dans Régie :",
                    error
                );

                if (!cancelled) {
                    setLibraryAssets([]);
                    setLibraryMessage(
                        "Impossible de charger la Bibliothèque Média."
                    );
                }
            } finally {
                if (!cancelled) {
                    setLibraryLoading(false);
                }
            }
        }

        loadLibraryAssets();

        return () => {
            cancelled = true;
        };
    }, [librarySearch, libraryType]);

    function loadLibraryAssetIntoRegie(asset) {
        if (!asset) {
            return;
        }

        const mediaUrl =
            asset.file_url ||
            asset.file ||
            "";

        setLibrarySelectedId(asset.id || null);

        if (mediaUrl) {
            setSourceUrl(mediaUrl);
        }

        if (asset.title) {
            setBroadcastTitle(asset.title);
            setLoadedMediaTitle(asset.title);
        }

        setLoadedMediaId(asset.id || null);

        setLibraryMessage(
            mediaUrl
                ? `Média chargé dans la Régie : ${asset.title || `#${asset.id}`}`
                : `Média sélectionné : ${asset.title || `#${asset.id}`} — aucun fichier disponible.`
        );

        setBroadcastMessage(
            mediaUrl
                ? `Média chargé depuis la Bibliothèque : ${asset.title || `#${asset.id}`}`
                : `Média trouvé : ${asset.title || `#${asset.id}`} — aucune URL de fichier disponible.`
        );
    }
    // ========================================================
    // BIBLIOTHEQUE MEDIA -> REGIE
    // /tv-regie?media=ID
    // ========================================================

    useEffect(() => {

        const params =
            new URLSearchParams(window.location.search);

        const mediaId =
            params.get("media");

        if (!mediaId) {
            return;
        }

        let cancelled = false;

        async function loadMediaFromLibrary() {

            try {

                setMediaLoading(true);

                setBroadcastMessage(
                    `Chargement du média #${mediaId} depuis la Bibliothèque Média...`
                );

                const response =
                    await getMediaAsset(mediaId);

                const media =
                    response?.data || response;

                if (cancelled || !media) {
                    return;
                }

                const mediaUrl =
                    media.file_url ||
                    media.file ||
                    "";

                if (mediaUrl) {
                    setSourceUrl(mediaUrl);
                }

                if (media.title) {

                    setBroadcastTitle(
                        media.title
                    );

                    setLoadedMediaTitle(
                        media.title
                    );
                }

                setLoadedMediaId(
                    media.id || mediaId
                );

                if (mediaUrl) {

                    setBroadcastMessage(
                        `Média chargé depuis la Bibliothèque : ${media.title || `#${mediaId}`}`
                    );

                } else {

                    setBroadcastMessage(
                        `Média trouvé : ${media.title || `#${mediaId}`} — aucune URL de fichier disponible.`
                    );
                }

            } catch (error) {

                console.error(
                    "Erreur Bibliothèque Média -> Régie :",
                    error
                );

                if (!cancelled) {

                    setBroadcastMessage(
                        "Impossible de charger le média depuis la Bibliothèque."
                    );
                }

            } finally {

                if (!cancelled) {
                    setMediaLoading(false);
                }
            }
        }

        loadMediaFromLibrary();

        return () => {
            cancelled = true;
        };

    }, []);
    const fallbackDestinations = [
        // DESTINATIONS INTERNES
        {
            id: "nsikay_tv",
            label: "NSIKAY TV",
            destinationType: "INTERNAL",
        },
        {
            id: "economie",
            label: "Économie",
            destinationType: "INTERNAL",
        },
        {
            id: "sport",
            label: "Sport & Loisirs",
            destinationType: "INTERNAL",
        },
        {
            id: "culture",
            label: "Culture & Art",
            destinationType: "INTERNAL",
        },
        {
            id: "technologie",
            label: "Technologie & Innovation",
            destinationType: "INTERNAL",
        },
        {
            id: "agriculture",
            label: "Agriculture & Agronomie",
            destinationType: "INTERNAL",
        },
        {
            id: "environnement",
            label: "Environnement",
            destinationType: "INTERNAL",
        },
        {
            id: "social",
            label: "Social",
            destinationType: "INTERNAL",
        },
        {
            id: "religion_histoire",
            label: "Religion & Histoire",
            destinationType: "INTERNAL",
        },
        {
            id: "adult",
            label: "+18",
            destinationType: "INTERNAL",
        },
        {
            id: "evenements",
            label: "Événements",
            destinationType: "INTERNAL",
        },
        {
            id: "publicite",
            label: "Publicité",
            destinationType: "INTERNAL",
        },

        // DESTINATIONS EXTERNES
        {
            id: "youtube",
            label: "YouTube",
            destinationType: "EXTERNAL",
        },
        {
            id: "facebook",
            label: "Facebook",
            destinationType: "EXTERNAL",
        },
        {
            id: "instagram",
            label: "Instagram",
            destinationType: "EXTERNAL",
        },
        {
            id: "tiktok",
            label: "TikTok",
            destinationType: "EXTERNAL",
        },
        {
            id: "twitch",
            label: "Twitch",
            destinationType: "EXTERNAL",
        },
        {
            id: "linkedin",
            label: "LinkedIn",
            destinationType: "EXTERNAL",
        },
        {
            id: "rtmp_custom",
            label: "RTMP personnalisé",
            destinationType: "EXTERNAL",
        },
        {
            id: "srt_custom",
            label: "SRT personnalisé",
            destinationType: "EXTERNAL",
        },
        {
            id: "hls_custom",
            label: "HLS personnalisé",
            destinationType: "EXTERNAL",
        },
    ];

    const destinations =
        djangoDestinations.length > 0
            ? djangoDestinations.map((destination) => ({
                id: destination.code,
                label: destination.name,
                type: destination.destination_type,
                channelType: destination.channel_type,
                description: destination.description,
                endpointUrl: destination.endpoint_url,
                active: destination.active,
            }))
            : fallbackDestinations;

    const toggleDestination = (id) => {
        setSelectedDestinations((current) => {
            if (current.includes(id)) {
                return current.filter((item) => item !== id);
            }

            return [...current, id];
        });
    };

    const resetDestinations = () => {
        setSelectedDestinations([
            destinations[0]?.id || "tv"
        ]);
    };

    const startBroadcast = async () => {
        if (broadcastBusy) {
            return;
        }

        if (selectedDestinations.length === 0) {
            setBroadcastMessage(
                "Sélectionnez au moins une destination."
            );
            return;
        }

        if (!sourceUrl.trim()) {
            setBroadcastMessage(
                "Renseignez la source du programme avant de diffuser."
            );
            return;
        }

        setBroadcastBusy(true);
        setBroadcastMessage("Connexion au Broadcast Central...");

        try {
            let id = broadcastId;

            if (!id) {
                const payload = {
                    title: broadcastTitle.trim() || "Programme NSIKAY",
                    source_url: sourceUrl.trim(),
                    thumbnail: "",
                    destinations: selectedDestinations,
                };

                const response =
                    await createCentralBroadcast(payload);

                const created =
                    response?.data || response;

                id = created?.id;

                if (!id) {
                    throw new Error(
                        "Le Broadcast Central n'a pas retourné d'identifiant."
                    );
                }

                setBroadcastId(id);
            }

            const response =
                await startCentralBroadcast(id);

            const started =
                response?.data || response;

            setBroadcastStatus(
                started?.status || "LIVE"
            );

            setOnAir(true);

            setBroadcastMessage(
                "Diffusion centrale démarrée."
            );
        } catch (error) {
            console.error(
                "NSIKAY Broadcast Central start error:",
                error
            );

            const message =
                error?.response?.data?.detail ||
                error?.response?.data?.error ||
                error?.message ||
                "Erreur lors du démarrage de la diffusion.";

            setBroadcastMessage(message);
            setOnAir(false);
        } finally {
            setBroadcastBusy(false);
        }
    };

    const stopBroadcast = async () => {
        if (broadcastBusy) {
            return;
        }

        if (!broadcastId) {
            setOnAir(false);
            setBroadcastStatus("STOPPED");
            setBroadcastMessage(
                "Aucun Broadcast Central actif."
            );
            return;
        }

        setBroadcastBusy(true);
        setBroadcastMessage("Arrêt de la diffusion...");

        try {
            const response =
                await stopCentralBroadcast(broadcastId);

            const stopped =
                response?.data || response;

            setBroadcastStatus(
                stopped?.status || "STOPPED"
            );

            setOnAir(false);

            setBroadcastMessage(
                "Diffusion centrale arrêtée."
            );
        } catch (error) {
            console.error(
                "NSIKAY Broadcast Central stop error:",
                error
            );

            const message =
                error?.response?.data?.detail ||
                error?.response?.data?.error ||
                error?.message ||
                "Erreur lors de l'arrêt de la diffusion.";

            setBroadcastMessage(message);
        } finally {
            setBroadcastBusy(false);
        }
    };

    return (
        <section
            style={{
                marginTop: 24,
                padding: 20,
                borderRadius: 16,
                border: "1px solid rgba(255,255,255,0.12)",
                background: "rgba(10,15,25,0.82)",
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 16,
                    flexWrap: "wrap",
                }}
            >
                <div>
                    <div
                        style={{
                            marginBottom: 18,
                            padding: 16,
                            borderRadius: 16,
                            border: "1px solid rgba(255,255,255,0.12)",
                            background: "rgba(10,15,25,0.82)",
                        }}
                    >
                        <div
                            style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                gap: 12,
                                flexWrap: "wrap",
                            }}
                        >
                            <div>
                                <h3 style={{ margin: 0 }}>
                                    BIBLIOTHÈQUE MÉDIA
                                </h3>

                                <div
                                    style={{
                                        marginTop: 5,
                                        opacity: 0.7,
                                        fontSize: 12,
                                    }}
                                >
                                    STOCKAGE → MÉDIA → RÉGIE → DIFFUSION
                                </div>
                            </div>

                            <div
                                style={{
                                    fontSize: 12,
                                    opacity: 0.7,
                                }}
                            >
                                {libraryAssets.length} média(s)
                            </div>
                        </div>

                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns:
                                    "minmax(220px, 2fr) minmax(150px, 1fr)",
                                gap: 10,
                                marginTop: 14,
                            }}
                        >
                            <input
                                value={librarySearch}
                                onChange={(event) =>
                                    setLibrarySearch(event.target.value)
                                }
                                placeholder="Rechercher un média..."
                                style={{
                                    padding: "10px 12px",
                                    borderRadius: 8,
                                    border:
                                        "1px solid rgba(255,255,255,0.14)",
                                    background:
                                        "rgba(255,255,255,0.05)",
                                    color: "inherit",
                                }}
                            />

                            <select
                                value={libraryType}
                                onChange={(event) =>
                                    setLibraryType(event.target.value)
                                }
                                style={{
                                    padding: "10px 12px",
                                    borderRadius: 8,
                                    border:
                                        "1px solid rgba(255,255,255,0.14)",
                                    background:
                                        "rgba(10,15,25,0.95)",
                                    color: "inherit",
                                }}
                            >
                                <option value="ALL">
                                    Tous les médias
                                </option>
                                <option value="VIDEO">Vidéo</option>
                                <option value="FILM">Film</option>
                                <option value="AUDIO">Audio</option>
                                <option value="PROGRAM">
                                    Programme TV
                                </option>
                                <option value="MUSIC">
                                    Musique
                                </option>
                                <option value="JINGLE">
                                    Jingle
                                </option>
                                <option value="ADVERTISING">
                                    Publicité
                                </option>
                                <option value="REPORTAGE">
                                    Reportage
                                </option>
                                <option value="INTERVIEW">
                                    Interview
                                </option>
                                <option value="ARCHIVE">
                                    Archive
                                </option>
                                <option value="DOCUMENT">
                                    Document
                                </option>
                            </select>
                        </div>

                        {libraryMessage && (
                            <div
                                style={{
                                    marginTop: 10,
                                    padding: "8px 10px",
                                    borderRadius: 8,
                                    background:
                                        "rgba(0,200,120,0.10)",
                                    border:
                                        "1px solid rgba(0,200,120,0.25)",
                                    fontSize: 12,
                                }}
                            >
                                {libraryMessage}
                            </div>
                        )}

                        <div
                            style={{
                                marginTop: 12,
                                display: "grid",
                                gridTemplateColumns:
                                    "repeat(auto-fit,minmax(230px,1fr))",
                                gap: 10,
                                maxHeight: 360,
                                overflowY: "auto",
                            }}
                        >
                            {libraryLoading ? (
                                <div
                                    style={{
                                        padding: 20,
                                        opacity: 0.7,
                                    }}
                                >
                                    Chargement de la Bibliothèque Média...
                                </div>
                            ) : libraryAssets.length === 0 ? (
                                <div
                                    style={{
                                        padding: 20,
                                        opacity: 0.7,
                                    }}
                                >
                                    Aucun média trouvé.
                                </div>
                            ) : (
                                libraryAssets.map((asset) => {
                                    const selected =
                                        librarySelectedId === asset.id;

                                    const assetUrl =
                                        asset.file_url ||
                                        asset.file ||
                                        "";

                                    return (
                                        <div
                                            key={asset.id}
                                            style={{
                                                padding: 12,
                                                borderRadius: 10,
                                                border: selected
                                                    ? "1px solid rgba(0,220,130,0.65)"
                                                    : "1px solid rgba(255,255,255,0.10)",
                                                background: selected
                                                    ? "rgba(0,200,120,0.10)"
                                                    : "rgba(255,255,255,0.035)",
                                            }}
                                        >
                                            <div
                                                style={{
                                                    fontWeight: 700,
                                                    fontSize: 13,
                                                }}
                                            >
                                                {asset.title ||
                                                    `Média #${asset.id}`}
                                            </div>

                                            <div
                                                style={{
                                                    marginTop: 5,
                                                    fontSize: 11,
                                                    opacity: 0.65,
                                                }}
                                            >
                                                {asset.asset_type ||
                                                    "MEDIA"}
                                                {" • "}
                                                ID {asset.id}
                                            </div>

                                            <button
                                                type="button"
                                                onClick={() =>
                                                    loadLibraryAssetIntoRegie(
                                                        asset
                                                    )
                                                }
                                                disabled={
                                                    broadcastBusy ||
                                                    onAir
                                                }
                                                style={{
                                                    width: "100%",
                                                    marginTop: 10,
                                                    padding: "9px 10px",
                                                    borderRadius: 8,
                                                    border:
                                                        "1px solid rgba(0,200,120,0.45)",
                                                    background:
                                                        "rgba(0,200,120,0.12)",
                                                    color: "inherit",
                                                    cursor:
                                                        broadcastBusy ||
                                                        onAir
                                                            ? "not-allowed"
                                                            : "pointer",
                                                }}
                                            >
                                                {selected
                                                    ? "✓ CHARGÉ EN RÉGIE"
                                                    : "CHARGER EN RÉGIE"}
                                            </button>

                                            {selected &&
                                                assetUrl &&
                                                /\.(mp4|webm|ogg|mov|m4v)(\?.*)?$/i.test(
                                                    assetUrl
                                                ) && (
                                                    <video
                                                        src={assetUrl}
                                                        controls
                                                        preload="metadata"
                                                        style={{
                                                            width: "100%",
                                                            marginTop: 10,
                                                            borderRadius: 7,
                                                            background:
                                                                "#000",
                                                        }}
                                                    />
                                                )}
                                        </div>
                                    );
                                })
                            )}
                        </div>
                    </div>

                    <h3 style={{ margin: 0 }}>
                        DIFFUSION CENTRALE NSIKAY
                    </h3>

                    <div
                        style={{
                            marginTop: 6,
                            opacity: 0.75,
                            fontSize: 13,
                        }}
                    >
                        Un programme central vers plusieurs destinations
                        éditoriales.
                    </div>
                </div>

                <div
                    style={{
                        padding: "7px 12px",
                        borderRadius: 999,
                        fontSize: 12,
                        fontWeight: 700,
                        background: onAir
                            ? "rgba(0,180,90,0.18)"
                            : "rgba(255,255,255,0.08)",
                        border: onAir
                            ? "1px solid rgba(0,220,110,0.45)"
                            : "1px solid rgba(255,255,255,0.12)",
                    }}
                >
                    {onAir ? "● ON AIR" : "○ HORS AIR"} — {broadcastStatus}
                </div>
            </div>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(260px,1fr))",
                    gap: 12,
                    marginTop: 18,
                }}
            >
                <label style={{ display: "grid", gap: 6 }}>
                    <span style={{ fontSize: 12, opacity: 0.7 }}>
                        TITRE DU PROGRAMME
                    </span>

                    <input
                        value={broadcastTitle}
                        onChange={(event) =>
                            setBroadcastTitle(event.target.value)
                        }
                        disabled={broadcastBusy || onAir}
                        style={{
                            padding: "10px 12px",
                            borderRadius: 8,
                            border: "1px solid rgba(255,255,255,0.14)",
                            background: "rgba(255,255,255,0.05)",
                            color: "inherit",
                        }}
                    />
                </label>

                <label style={{ display: "grid", gap: 6 }}>
                    <span style={{ fontSize: 12, opacity: 0.7 }}>
                        SOURCE PROGRAMME
                    </span>

                    <input
                        value={sourceUrl}
                        onChange={(event) =>
                            setSourceUrl(event.target.value)
                        }
                        disabled={broadcastBusy || onAir}
                        placeholder="https://..."
                        style={{
                            padding: "10px 12px",
                            borderRadius: 8,
                            border: "1px solid rgba(255,255,255,0.14)",
                            background: "rgba(255,255,255,0.05)",
                            color: "inherit",
                        }}
                    />
                </label>
            </div>

            <div style={{ marginTop: 18 }}>
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        gap: 12,
                        marginBottom: 10,
                    }}
                >
                    <div>
                        <strong>
                            DESTINATIONS ({selectedDestinations.length})
                        </strong>

                        {destinationsLoading && (
                            <div
                                style={{
                                    marginTop: 4,
                                    fontSize: 10,
                                    opacity: 0.6,
                                }}
                            >
                                Synchronisation avec Django...
                            </div>
                        )}

                        {destinationsError && (
                            <div
                                style={{
                                    marginTop: 4,
                                    fontSize: 10,
                                    opacity: 0.7,
                                }}
                            >
                                {destinationsError}
                            </div>
                        )}
                    </div>

                    <button
                        type="button"
                        onClick={resetDestinations}
                        disabled={broadcastBusy || onAir}
                    >
                        Réinitialiser
                    </button>
                </div>

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fit,minmax(180px,1fr))",
                        gap: 8,
                    }}
                >
                    {destinations.map((destination, index) => {

    const selected =
        selectedDestinations.includes(
            destination.id
        );

    const isInternal =
        destination.destinationType === "INTERNAL" ||
        destination.type === "INTERNAL";

    const previous =
        index > 0
            ? destinations[index - 1]
            : null;

    const previousIsInternal =
        previous &&
        (
            previous.destinationType === "INTERNAL" ||
            previous.type === "INTERNAL"
        );

    return (
        <React.Fragment key={destination.id}>

            {index === 0 && isInternal && (
                <div
                    style={{
                        gridColumn: "1 / -1",
                        padding: "8px 10px",
                        marginBottom: 4,
                        fontSize: 12,
                        fontWeight: 800,
                        opacity: 0.9,
                    }}
                >
                    DESTINATIONS INTERNES (12)
                </div>
            )}

            {!isInternal && previousIsInternal && (
                <div
                    style={{
                        gridColumn: "1 / -1",
                        padding: "8px 10px",
                        marginTop: 16,
                        marginBottom: 4,
                        fontSize: 12,
                        fontWeight: 800,
                        opacity: 0.9,
                    }}
                >
                    DESTINATIONS EXTERNES (9)
                </div>
            )}
                        const selected =
                            selectedDestinations.includes(
                                destination.id
                            );

                        return (
                            <button
                                key={destination.id}
                                type="button"
                                onClick={() =>
                                    toggleDestination(
                                        destination.id
                                    )
                                }
                                disabled={broadcastBusy || onAir}
                                style={{
                                    textAlign: "left",
                                    padding: "10px 12px",
                                    borderRadius: 8,
                                    cursor:
                                        broadcastBusy || onAir
                                            ? "not-allowed"
                                            : "pointer",
                                    border: selected
                                        ? "1px solid rgba(0,200,120,0.65)"
                                        : "1px solid rgba(255,255,255,0.12)",
                                    background: selected
                                        ? "rgba(0,200,120,0.14)"
                                        : "rgba(255,255,255,0.04)",
                                    color: "inherit",
                                }}
                            >
                                {selected ? "✓ " : "○ "}
                                {destination.label}
                            </button>
                        );
                    })}
                </div>
            </div>

            <div
                style={{
                    marginTop: 16,
                    padding: 12,
                    borderRadius: 8,
                    background: "rgba(255,255,255,0.04)",
                    fontSize: 13,
                }}
            >
                {broadcastMessage}
            </div>

            <div
                style={{
                    display: "flex",
                    gap: 10,
                    flexWrap: "wrap",
                    marginTop: 16,
                }}
            >
                <button
                    type="button"
                    onClick={startBroadcast}
                    disabled={broadcastBusy || onAir}
                    style={{
                        padding: "11px 18px",
                        borderRadius: 8,
                        fontWeight: 800,
                        cursor:
                            broadcastBusy || onAir
                                ? "not-allowed"
                                : "pointer",
                    }}
                >
                    {broadcastBusy
                        ? "CONNEXION..."
                        : "● DIFFUSER"}
                </button>

                <button
                    type="button"
                    onClick={stopBroadcast}
                    disabled={broadcastBusy || !onAir}
                    style={{
                        padding: "11px 18px",
                        borderRadius: 8,
                        fontWeight: 800,
                        cursor:
                            broadcastBusy || !onAir
                                ? "not-allowed"
                                : "pointer",
                    }}
                >
                    {broadcastBusy
                        ? "ARRÊT..."
                        : "■ ARRÊTER"}
                </button>
            </div>
        </section>
    );
}
export default function TVRegie() {
    const [cameras, setCameras] = useState([]);
    const [streams, setStreams] = useState([]);
    const [channels, setChannels] = useState([]);
    const [effects, setEffects] = useState([]);
    const [animations, setAnimations] = useState([]);
    const [audio, setAudio] = useState([]);
    const [scenes, setScenes] = useState([]);
    const [schedules, setSchedules] = useState([]);

    const [previewId, setPreviewId] = useState(null);
    const [programId, setProgramId] = useState(null);

    const [layout, setLayout] = useState(1);
    const [transition, setTransition] = useState("CUT");
    const [onAir, setOnAir] = useState(false);
    const [recording, setRecording] = useState(false);
    const [activeTab, setActiveTab] = useState("sources");
    const [message, setMessage] = useState("");
    const [busy, setBusy] = useState(false);

    const [selectedChannel, setSelectedChannel] = useState("");
    const [selectedStream, setSelectedStream] = useState("");

    const [cameraForm, setCameraForm] = useState({
        name: "",
        source_type: "WEBRTC",
        source_url: "",
        resolution: "1080p",
        frame_rate: 30,
        description: "",
    });

    const [streamForm, setStreamForm] = useState({
        title: "",
        camera: "",
        stream_url: "",
        quality: "1080p",
        recording_enabled: true,
    });

    const [effectForm, setEffectForm] = useState({
        name: "",
        effect_type: "FILTER",
        parameters: "{}",
    });

    const [animationForm, setAnimationForm] = useState({
        title: "",
        text: "",
        animation_type: "FADE",
        position: "BOTTOM",
        duration: 5,
    });

    const [audioForm, setAudioForm] = useState({
        name: "",
        volume: 100,
        audio_effect: "",
        muted: false,
    });

    const [scheduleForm, setScheduleForm] = useState({
        title: "",
        start_time: "",
        end_time: "",
        live: false,
    });

    const sourceList = useMemo(() => {
        const cameraItems = cameras.map((camera) => ({
            ...camera,
            sourceKind: "camera",
            sourceLabel: `CAM ${camera.id}`,
        }));

        const streamItems = streams.map((stream) => ({
            ...stream,
            sourceKind: "stream",
            sourceLabel: `LIVE ${stream.id}`,
        }));

        return [...cameraItems, ...streamItems];
    }, [cameras, streams]);

    const previewSource = sourceList.find(
        (item) => `${item.sourceKind}-${item.id}` === previewId
    );

    const programSource = sourceList.find(
        (item) => `${item.sourceKind}-${item.id}` === programId
    );

    async function loadAll() {
        setBusy(true);
        try {
            const [
                camerasResponse,
                streamsResponse,
                channelsResponse,
                effectsResponse,
                animationsResponse,
                audioResponse,
                scenesResponse,
                schedulesResponse,
            ] = await Promise.all([
                getCameras(),
                getStreams(),
                getTVChannels(),
                getEffects(),
                getAnimations(),
                getAudioControls(),
                getScenes(),
                getSchedules(),
            ]);

            setCameras(unwrap(camerasResponse));
            setStreams(unwrap(streamsResponse));
            setChannels(unwrap(channelsResponse));
            setEffects(unwrap(effectsResponse));
            setAnimations(unwrap(animationsResponse));
            setAudio(unwrap(audioResponse));
            setScenes(unwrap(scenesResponse));
            setSchedules(unwrap(schedulesResponse));

            setMessage("Régie connectée aux services Django.");
        } catch (error) {
            console.error(error);
            setMessage(
                "Erreur de connexion aux services de la Régie. Vérifiez Django et votre authentification."
            );
        } finally {
            setBusy(false);
        }
    }

    useEffect(() => {
        loadAll();
    }, []);

    useEffect(() => {
        if (!previewId && sourceList.length) {
            const first = sourceList[0];
            setPreviewId(`${first.sourceKind}-${first.id}`);
        }
    }, [sourceList, previewId]);

    async function handleCreateCamera(event) {
        event.preventDefault();
        try {
            await createCamera({
                ...cameraForm,
                frame_rate: Number(cameraForm.frame_rate),
            });
            setCameraForm({
                name: "",
                source_type: "WEBRTC",
                source_url: "",
                resolution: "1080p",
                frame_rate: 30,
                description: "",
            });
            await loadAll();
            setMessage("Caméra enregistrée.");
        } catch (error) {
            console.error(error);
            setMessage("Impossible d'enregistrer la caméra.");
        }
    }

    async function handleCameraLive(camera) {
        try {
            await updateCamera(camera.id, { is_live: !camera.is_live });
            await loadAll();
            setMessage(
                `${camera.name} : ${camera.is_live ? "arrêtée" : "activée"}.`
            );
        } catch (error) {
            console.error(error);
            setMessage("Modification de l'état de la caméra impossible.");
        }
    }

    async function handleDeleteCamera(id) {
        if (!window.confirm("Supprimer cette caméra ?")) return;

        try {
            await deleteCamera(id);
            if (previewId === `camera-${id}`) setPreviewId(null);
            if (programId === `camera-${id}`) setProgramId(null);
            await loadAll();
            setMessage("Caméra supprimée.");
        } catch (error) {
            console.error(error);
            setMessage("Suppression impossible.");
        }
    }

    async function handleCreateStream(event) {
        event.preventDefault();

        try {
            await createStream({
                ...streamForm,
                camera: Number(streamForm.camera),
            });

            setStreamForm({
                title: "",
                camera: "",
                stream_url: "",
                quality: "1080p",
                recording_enabled: true,
            });

            await loadAll();
            setMessage("LiveStream créé.");
        } catch (error) {
            console.error(error);
            setMessage("Impossible de créer le LiveStream.");
        }
    }

    async function handleDeleteStream(id) {
        if (!window.confirm("Supprimer ce LiveStream ?")) return;

        try {
            await deleteStream(id);
            if (previewId === `stream-${id}`) setPreviewId(null);
            if (programId === `stream-${id}`) setProgramId(null);
            await loadAll();
            setMessage("LiveStream supprimé.");
        } catch (error) {
            console.error(error);
            setMessage("Suppression du LiveStream impossible.");
        }
    }

    function selectPreview(source) {
        setPreviewId(`${source.sourceKind}-${source.id}`);
        setMessage(`${sourceName(source)} chargé dans PREVIEW.`);
    }

    function executeTransition() {
        if (!previewId) {
            setMessage("Sélectionnez d'abord une source dans PREVIEW.");
            return;
        }

        setProgramId(previewId);
        setMessage(
            `${transition} exécuté : PREVIEW → PROGRAM.`
        );
    }

    function executeCut() {
        if (!previewId) {
            setMessage("Aucune source sélectionnée.");
            return;
        }

        setProgramId(previewId);
        setTransition("CUT");
        setMessage("CUT exécuté.");
    }

    function executeFade() {
        if (!previewId) {
            setMessage("Aucune source sélectionnée.");
            return;
        }

        setTransition("FADE");
        setProgramId(previewId);
        setMessage("FADE exécuté.");
    }

    async function handlePublish() {
        if (!selectedStream || !selectedChannel) {
            setMessage("Sélectionnez un LiveStream et une chaîne TV.");
            return;
        }

        try {
            await publishStream(Number(selectedStream), Number(selectedChannel));
            await loadAll();
            setOnAir(true);
            setMessage("LiveStream publié sur la chaîne TV.");
        } catch (error) {
            console.error(error);
            setMessage("Publication impossible.");
        }
    }

    async function handleUnpublish() {
        if (!selectedStream) {
            setMessage("Sélectionnez un LiveStream.");
            return;
        }

        try {
            await unpublishStream(Number(selectedStream));
            await loadAll();
            setOnAir(false);
            setMessage("LiveStream retiré de la diffusion.");
        } catch (error) {
            console.error(error);
            setMessage("Dépublication impossible.");
        }
    }

    async function handleCreateEffect(event) {
        event.preventDefault();

        try {
            let parameters = {};

            try {
                parameters = JSON.parse(effectForm.parameters || "{}");
            } catch {
                setMessage("Les paramètres de l'effet doivent être du JSON valide.");
                return;
            }

            await createEffect({
                name: effectForm.name,
                effect_type: effectForm.effect_type,
                parameters,
                active: true,
            });

            setEffectForm({
                name: "",
                effect_type: "FILTER",
                parameters: "{}",
            });

            await loadAll();
            setMessage("Effet ajouté.");
        } catch (error) {
            console.error(error);
            setMessage("Création de l'effet impossible.");
        }
    }

    async function handleCreateAnimation(event) {
        event.preventDefault();

        try {
            await createAnimation({
                ...animationForm,
                duration: Number(animationForm.duration),
                active: true,
            });

            setAnimationForm({
                title: "",
                text: "",
                animation_type: "FADE",
                position: "BOTTOM",
                duration: 5,
            });

            await loadAll();
            setMessage("Animation ajoutée.");
        } catch (error) {
            console.error(error);
            setMessage("Création de l'animation impossible.");
        }
    }

    async function handleCreateAudio(event) {
        event.preventDefault();

        try {
            await createAudioControl({
                ...audioForm,
                volume: Number(audioForm.volume),
            });

            setAudioForm({
                name: "",
                volume: 100,
                audio_effect: "",
                muted: false,
            });

            await loadAll();
            setMessage("Contrôle audio ajouté.");
        } catch (error) {
            console.error(error);
            setMessage("Création du contrôle audio impossible.");
        }
    }

    async function handleCreateScene() {
        const name = window.prompt("Nom de la scène :");
        if (!name) return;

        try {
            await createScene({
                name,
                active: true,
                cameras: [],
                effects: [],
                texts: [],
                audio: [],
            });

            await loadAll();
            setMessage("Scène créée.");
        } catch (error) {
            console.error(error);
            setMessage("Création de scène impossible.");
        }
    }

    async function handleCreateSchedule(event) {
        event.preventDefault();

        try {
            await createSchedule({
                title: scheduleForm.title,
                start_time: scheduleForm.start_time,
                end_time: scheduleForm.end_time,
                live: scheduleForm.live,
            });

            setScheduleForm({
                title: "",
                start_time: "",
                end_time: "",
                live: false,
            });

            await loadAll();
            setMessage("Programmation ajoutée.");
        } catch (error) {
            console.error(error);
            setMessage("Création de la programmation impossible.");
        }
    }

    async function removeResource(removeFunction, id, label) {
        if (!window.confirm(`Supprimer ${label} ?`)) return;

        try {
            await removeFunction(id);
            await loadAll();
            setMessage(`${label} supprimé.`);
        } catch (error) {
            console.error(error);
            setMessage(`Impossible de supprimer ${label}.`);
        }
    }

    function renderComposition() {
        const sources = [];

        if (programSource) sources.push(programSource);

        const selected = sourceList.filter(
            (source) =>
                `${source.sourceKind}-${source.id}` === previewId
        );

        if (selected.length && !sources.find((x) => x.id === selected[0].id)) {
            sources.push(selected[0]);
        }

        const compositionSources = [
            ...sources,
            ...sourceList.filter(
                (source) =>
                    !sources.some(
                        (existing) =>
                            existing.sourceKind === source.sourceKind &&
                            existing.id === source.id
                    )
            ),
        ].slice(0, layout);

        if (!compositionSources.length) {
            return (
                <div
                    style={{
                        height: 300,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: CATEGORY.muted,
                    }}
                >
                    Sélectionnez des sources.
                </div>
            );
        }

        const columns = layout === 1 ? 1 : 2;

        return (
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: `repeat(${columns}, minmax(0,1fr))`,
                    gap: 4,
                    height: 300,
                }}
            >
                {compositionSources.map((source) => (
                    <SourcePreview
                        key={`${source.sourceKind}-${source.id}`}
                        source={source}
                        label={source.sourceLabel}
                        compact
                    />
                ))}
            </div>
        );
    }

    return (
        <div
            style={{
                minHeight: "100vh",
                background: CATEGORY.background,
                color: CATEGORY.text,
                padding: 14,
                fontFamily:
                    "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 15,
                    marginBottom: 14,
                    flexWrap: "wrap",
                }}
            >
                <div>
                    <div
                        style={{
                            fontSize: 23,
                            fontWeight: 900,
                            letterSpacing: ".5px",
                        }}
                    >
                        NSIKAY TV — RÉGIE
                    </div>
                    <div
                        style={{
                            color: CATEGORY.muted,
                            fontSize: 12,
                            marginTop: 3,
                        }}
                    >
                        Console de réalisation • Multiview • Montage • Direct
                    </div>
                </div>

                <div style={{ display: "flex", gap: 7, alignItems: "center" }}>
                    <span
                        style={{
                            padding: "6px 9px",
                            borderRadius: 6,
                            background: onAir
                                ? "rgba(214,69,69,.22)"
                                : "rgba(145,164,184,.12)",
                            color: onAir
                                ? "#ff7676"
                                : CATEGORY.muted,
                            fontWeight: 800,
                            fontSize: 11,
                        }}
                    >
                        {onAir ? "● ON AIR" : "○ OFF AIR"}
                    </span>

                    <ControlButton onClick={loadAll} disabled={busy}>
                        ↻ Actualiser
                    </ControlButton>

                    <ControlButton
                        success
                        active={recording}
                        onClick={() => {
                            setRecording(!recording);
                            setMessage(
                                !recording
                                    ? "Enregistrement activé."
                                    : "Enregistrement arrêté."
                            );
                        }}
                    >
                        {recording ? "■ STOP REC" : "● REC"}
                    </ControlButton>
                </div>
            </div>

            {message && (
                <div
                    style={{
                        background: "rgba(47,128,237,.10)",
                        border: `1px solid ${CATEGORY.border}`,
                        padding: "9px 12px",
                        borderRadius: 7,
                        marginBottom: 12,
                        color: CATEGORY.muted,
                        fontSize: 12,
                    }}
                >
                    {message}
                </div>
            )}

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "minmax(250px, .85fr) minmax(420px, 1.6fr) minmax(250px, .85fr)",
                    gap: 10,
                    marginBottom: 10,
                }}
            >
                <Panel
                    title="PREVIEW"
                    right={
                        <span
                            style={{
                                fontSize: 10,
                                color: CATEGORY.warning,
                                fontWeight: 800,
                            }}
                        >
                            PROCHAIN PLAN
                        </span>
                    }
                >
                    {previewSource ? (
                        <SourcePreview
                            source={previewSource}
                            label="PREVIEW"
                        />
                    ) : (
                        <div
                            style={{
                                height: 300,
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                color: CATEGORY.muted,
                            }}
                        >
                            Aucun plan
                        </div>
                    )}
                </Panel>

                <Panel
                    title="MULTIVIEW / PROGRAM"
                    right={
                        <span
                            style={{
                                color: onAir
                                    ? "#ff7676"
                                    : CATEGORY.muted,
                                fontSize: 11,
                                fontWeight: 800,
                            }}
                        >
                            {onAir ? "● DIRECT" : "PROGRAM"}
                        </span>
                    }
                >
                    <div
                        style={{
                            background: "#02070d",
                            borderRadius: 8,
                            overflow: "hidden",
                        }}
                    >
                        {programSource ? (
                            <SourcePreview
                                source={programSource}
                                label="PROGRAM"
                            />
                        ) : (
                            <div
                                style={{
                                    height: 300,
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    color: CATEGORY.muted,
                                }}
                            >
                                PROGRAM vide
                            </div>
                        )}
                    </div>

                    <div style={{ marginTop: 8 }}>
                        <div
                            style={{
                                fontSize: 10,
                                color: CATEGORY.muted,
                                marginBottom: 5,
                            }}
                        >
                            COMPOSITION
                        </div>

                        <div
                            style={{
                                display: "flex",
                                gap: 5,
                                flexWrap: "wrap",
                            }}
                        >
                            {[1, 2, 3, 4].map((value) => (
                                <ControlButton
                                    key={value}
                                    active={layout === value}
                                    onClick={() => setLayout(value)}
                                >
                                    {value} CAM
                                </ControlButton>
                            ))}

                            <ControlButton
                                active={layout === 2}
                                onClick={() => setLayout(2)}
                            >
                                PIP / 2
                            </ControlButton>
                        </div>
                    </div>
                </Panel>

                <Panel
                    title="PREVIEW MULTI-SOURCES"
                    right={
                        <span
                            style={{
                                color: CATEGORY.success,
                                fontSize: 10,
                                fontWeight: 800,
                            }}
                        >
                            SOURCES
                        </span>
                    }
                >
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(2, minmax(0,1fr))",
                            gap: 7,
                            maxHeight: 390,
                            overflowY: "auto",
                        }}
                    >
                        {sourceList.length === 0 && (
                            <div
                                style={{
                                    gridColumn: "1 / -1",
                                    color: CATEGORY.muted,
                                    padding: 20,
                                    textAlign: "center",
                                }}
                            >
                                Aucune source.
                            </div>
                        )}

                        {sourceList.map((source) => {
                            const key = `${source.sourceKind}-${source.id}`;

                            return (
                                <button
                                    type="button"
                                    key={key}
                                    onClick={() => selectPreview(source)}
                                    style={{
                                        textAlign: "left",
                                        padding: 0,
                                        border: `2px solid ${
                                            previewId === key
                                                ? CATEGORY.warning
                                                : CATEGORY.border
                                        }`,
                                        background: "#02070d",
                                        borderRadius: 7,
                                        overflow: "hidden",
                                        cursor: "pointer",
                                    }}
                                >
                                    <SourcePreview
                                        source={source}
                                        label={
                                            source.sourceLabel ||
                                            sourceName(source)
                                        }
                                        compact
                                    />
                                    <div
                                        style={{
                                            padding: "6px 7px",
                                            color: CATEGORY.text,
                                            fontSize: 10,
                                        }}
                                    >
                                        {sourceName(source)}
                                    </div>
                                </button>
                            );
                        )}
                    </React.Fragment>
                );
            })}
                    </div>
                </Panel>
            </div>

            <Panel
                title="CONSOLE DE RÉALISATION"
                right={
                    <div style={{ display: "flex", gap: 5 }}>
                        <span
                            style={{
                                fontSize: 10,
                                color: CATEGORY.warning,
                            }}
                        >
                            PREVIEW
                        </span>
                        <span style={{ color: CATEGORY.muted }}>→</span>
                        <span
                            style={{
                                fontSize: 10,
                                color: CATEGORY.success,
                            }}
                        >
                            PROGRAM
                        </span>
                    </div>
                }
            >
                <div
                    style={{
                        display: "flex",
                        gap: 8,
                        flexWrap: "wrap",
                        marginBottom: 10,
                    }}
                >
                    <ControlButton
                        success
                        onClick={executeCut}
                        disabled={!previewId}
                    >
                        CUT
                    </ControlButton>

                    <ControlButton
                        active={transition === "FADE"}
                        onClick={executeFade}
                        disabled={!previewId}
                    >
                        FADE
                    </ControlButton>

                    {["DISSOLVE", "WIPE", "SLIDE", "ZOOM"].map(
                        (item) => (
                            <ControlButton
                                key={item}
                                active={transition === item}
                                onClick={() => {
                                    setTransition(item);
                                    executeTransition();
                                }}
                                disabled={!previewId}
                            >
                                {item}
                            </ControlButton>
                        )
                    )}

                    <div
                        style={{
                            marginLeft: "auto",
                            display: "flex",
                            gap: 7,
                        }}
                    >
                        <ControlButton
                            danger
                            active={onAir}
                            onClick={() => setOnAir(!onAir)}
                        >
                            {onAir ? "● ON AIR" : "○ ON AIR"}
                        </ControlButton>
                    </div>
                </div>

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fit,minmax(105px,1fr))",
                        gap: 7,
                    }}
                >
                    {sourceList.map((source) => {
                        const key = `${source.sourceKind}-${source.id}`;
                        const isPreview = previewId === key;
                        const isProgram = programId === key;

                        return (
                            <ControlButton
                                key={key}
                                active={isPreview}
                                success={isProgram}
                                onClick={() => selectPreview(source)}
                            >
                                {source.sourceLabel ||
                                    sourceName(source)}
                                {isProgram ? " • PGM" : ""}
                            </ControlButton>
                        );
                    })}
                </div>
            </Panel>

            <div style={{ height: 10 }} />

            <div
                style={{
                    display: "flex",
                    gap: 5,
                    flexWrap: "wrap",
                    marginBottom: 10,
                }}
            >
                {[
                    ["sources", "SOURCES"],
                    ["montage", "MONTAGE"],
                    ["effects", "EFFETS"],
                    ["animations", "ANIMATIONS"],
                    ["audio", "AUDIO"],
                    ["scenes", "SCÈNES"],
                    ["schedule", "PROGRAMMATION"],
                    ["broadcast", "DIFFUSION"],
                ].map(([key, label]) => (
                    <ControlButton
                        key={key}
                        active={activeTab === key}
                        onClick={() => setActiveTab(key)}
                    >
                        {label}
                    </ControlButton>
                ))}
            </div>

            {activeTab === "sources" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="AJOUTER UNE CAMÉRA">
                        <form
                            onSubmit={handleCreateCamera}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Nom de la caméra"
                                value={cameraForm.name}
                                onChange={(e) =>
                                    setCameraForm({
                                        ...cameraForm,
                                        name: e.target.value,
                                    })
                                }
                                required
                            />

                            <select
                                value={cameraForm.source_type}
                                onChange={(e) =>
                                    setCameraForm({
                                        ...cameraForm,
                                        source_type: e.target.value,
                                    })
                                }
                            >
                                <option value="WEBRTC">WebRTC</option>
                                <option value="IP">IP Camera</option>
                                <option value="RTMP">RTMP</option>
                                <option value="HDMI">HDMI</option>
                                <option value="SDI">SDI</option>
                            </select>

                            <input
                                placeholder="URL source"
                                value={cameraForm.source_url}
                                onChange={(e) =>
                                    setCameraForm({
                                        ...cameraForm,
                                        source_url: e.target.value,
                                    })
                                }
                            />

                            <div
                                style={{
                                    display: "grid",
                                    gridTemplateColumns: "1fr 1fr",
                                    gap: 8,
                                }}
                            >
                                <input
                                    placeholder="Résolution"
                                    value={cameraForm.resolution}
                                    onChange={(e) =>
                                        setCameraForm({
                                            ...cameraForm,
                                            resolution: e.target.value,
                                        })
                                    }
                                />

                                <input
                                    type="number"
                                    min="1"
                                    placeholder="FPS"
                                    value={cameraForm.frame_rate}
                                    onChange={(e) =>
                                        setCameraForm({
                                            ...cameraForm,
                                            frame_rate: e.target.value,
                                        })
                                    }
                                />
                            </div>

                            <textarea
                                placeholder="Description"
                                value={cameraForm.description}
                                onChange={(e) =>
                                    setCameraForm({
                                        ...cameraForm,
                                        description: e.target.value,
                                    })
                                }
                                rows={3}
                            />

                            <ControlButton success>
                                + AJOUTER CAMÉRA
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="CAMÉRAS CONNECTÉES">
                        <div
                            style={{
                                display: "grid",
                                gap: 7,
                            }}
                        >
                            {cameras.map((camera) => (
                                <div
                                    key={camera.id}
                                    style={{
                                        display: "flex",
                                        justifyContent:
                                            "space-between",
                                        alignItems: "center",
                                        gap: 8,
                                        padding: 9,
                                        background:
                                            CATEGORY.panel2,
                                        borderRadius: 7,
                                    }}
                                >
                                    <div>
                                        <strong>
                                            {camera.name}
                                        </strong>
                                        <div
                                            style={{
                                                color:
                                                    CATEGORY.muted,
                                                fontSize: 10,
                                            }}
                                        >
                                            {camera.source_type} •{" "}
                                            {camera.resolution} •{" "}
                                            {camera.frame_rate} FPS
                                        </div>
                                    </div>

                                    <div
                                        style={{
                                            display: "flex",
                                            gap: 5,
                                        }}
                                    >
                                        <ControlButton
                                            success={
                                                camera.is_live
                                            }
                                            active={
                                                camera.is_live
                                            }
                                            onClick={() =>
                                                handleCameraLive(
                                                    camera
                                                )
                                            }
                                        >
                                            {camera.is_live
                                                ? "LIVE"
                                                : "OFF"}
                                        </ControlButton>

                                        <ControlButton
                                            danger
                                            onClick={() =>
                                                handleDeleteCamera(
                                                    camera.id
                                                )
                                            }
                                        >
                                            SUPPR.
                                        </ControlButton>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Panel>

                    <Panel title="CRÉER UN LIVE STREAM">
                        <form
                            onSubmit={handleCreateStream}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Titre du Live"
                                value={streamForm.title}
                                onChange={(e) =>
                                    setStreamForm({
                                        ...streamForm,
                                        title: e.target.value,
                                    })
                                }
                                required
                            />

                            <select
                                value={streamForm.camera}
                                onChange={(e) =>
                                    setStreamForm({
                                        ...streamForm,
                                        camera: e.target.value,
                                    })
                                }
                                required
                            >
                                <option value="">
                                    Choisir une caméra
                                </option>
                                {cameras.map((camera) => (
                                    <option
                                        key={camera.id}
                                        value={camera.id}
                                    >
                                        {camera.name}
                                    </option>
                                ))}
                            </select>

                            <input
                                placeholder="URL du flux vidéo"
                                value={streamForm.stream_url}
                                onChange={(e) =>
                                    setStreamForm({
                                        ...streamForm,
                                        stream_url: e.target.value,
                                    })
                                }
                                required
                            />

                            <select
                                value={streamForm.quality}
                                onChange={(e) =>
                                    setStreamForm({
                                        ...streamForm,
                                        quality: e.target.value,
                                    })
                                }
                            >
                                <option>720p</option>
                                <option>1080p</option>
                                <option>4K Ultra HD</option>
                            </select>

                            <label
                                style={{
                                    fontSize: 12,
                                    color: CATEGORY.muted,
                                }}
                            >
                                <input
                                    type="checkbox"
                                    checked={
                                        streamForm.recording_enabled
                                    }
                                    onChange={(e) =>
                                        setStreamForm({
                                            ...streamForm,
                                            recording_enabled:
                                                e.target.checked,
                                        })
                                    }
                                />{" "}
                                Enregistrement activé
                            </label>

                            <ControlButton success>
                                + CRÉER LIVE
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="LIVE STREAMS">
                        <div style={{ display: "grid", gap: 7 }}>
                            {streams.map((stream) => (
                                <div
                                    key={stream.id}
                                    style={{
                                        padding: 9,
                                        background:
                                            CATEGORY.panel2,
                                        borderRadius: 7,
                                    }}
                                >
                                    <div
                                        style={{
                                            display: "flex",
                                            justifyContent:
                                                "space-between",
                                            gap: 8,
                                        }}
                                    >
                                        <div>
                                            <strong>
                                                {stream.title}
                                            </strong>
                                            <div
                                                style={{
                                                    color:
                                                        CATEGORY.muted,
                                                    fontSize: 10,
                                                }}
                                            >
                                                {stream.quality}
                                            </div>
                                        </div>

                                        <ControlButton
                                            danger
                                            onClick={() =>
                                                handleDeleteStream(
                                                    stream.id
                                                )
                                            }
                                        >
                                            SUPPR.
                                        </ControlButton>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </div>
            )}

            {activeTab === "montage" && (
                <Panel
                    title="TIMELINE DE MONTAGE"
                    right={
                        <span
                            style={{
                                color: CATEGORY.muted,
                                fontSize: 10,
                            }}
                        >
                            ESPACE DE PRODUCTION
                        </span>
                    }
                >
                    <div
                        style={{
                            display: "grid",
                            gap: 5,
                        }}
                    >
                        {["VIDEO 1", "VIDEO 2", "AUDIO 1", "TITRES", "EFFETS"].map(
                            (track, index) => (
                                <div
                                    key={track}
                                    style={{
                                        display: "grid",
                                        gridTemplateColumns:
                                            "80px 1fr",
                                        gap: 5,
                                        alignItems: "center",
                                    }}
                                >
                                    <div
                                        style={{
                                            color:
                                                CATEGORY.muted,
                                            fontSize: 10,
                                        }}
                                    >
                                        {track}
                                    </div>

                                    <div
                                        style={{
                                            height: 40,
                                            background:
                                                CATEGORY.panel2,
                                            border:
                                                `1px solid ${CATEGORY.border}`,
                                            borderRadius: 5,
                                            position:
                                                "relative",
                                            overflow: "hidden",
                                        }}
                                    >
                                        <div
                                            style={{
                                                position:
                                                    "absolute",
                                                left:
                                                    index *
                                                    11 +
                                                    "%",
                                                top: 5,
                                                bottom: 5,
                                                width:
                                                    23 +
                                                    index *
                                                        5 +
                                                    "%",
                                                background:
                                                    "rgba(47,128,237,.25)",
                                                border:
                                                    `1px solid ${CATEGORY.accent}`,
                                                borderRadius: 4,
                                            }}
                                        />
                                    </div>
                                </div>
                            )
                        )}
                    </div>

                    <div
                        style={{
                            marginTop: 10,
                            display: "flex",
                            gap: 7,
                            flexWrap: "wrap",
                        }}
                    >
                        <ControlButton>✂ COUPER</ControlButton>
                        <ControlButton>▣ DUPLIQUER</ControlButton>
                        <ControlButton>↔ DÉPLACER</ControlButton>
                        <ControlButton>＋ MARQUEUR</ControlButton>
                        <ControlButton>▶ LECTURE</ControlButton>
                        <ControlButton>⏸ PAUSE</ControlButton>
                    </div>
                </Panel>
            )}

            {activeTab === "effects" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1.5fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="NOUVEL EFFET">
                        <form
                            onSubmit={handleCreateEffect}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Nom"
                                value={effectForm.name}
                                onChange={(e) =>
                                    setEffectForm({
                                        ...effectForm,
                                        name: e.target.value,
                                    })
                                }
                                required
                            />

                            <select
                                value={effectForm.effect_type}
                                onChange={(e) =>
                                    setEffectForm({
                                        ...effectForm,
                                        effect_type: e.target.value,
                                    })
                                }
                            >
                                <option>FILTER</option>
                                <option>BLUR</option>
                                <option>ZOOM</option>
                                <option>GRAYSCALE</option>
                                <option>BRIGHTNESS</option>
                                <option>CONTRAST</option>
                                <option>OVERLAY</option>
                            </select>

                            <textarea
                                rows={5}
                                value={effectForm.parameters}
                                onChange={(e) =>
                                    setEffectForm({
                                        ...effectForm,
                                        parameters:
                                            e.target.value,
                                    })
                                }
                            />

                            <ControlButton success>
                                + AJOUTER EFFET
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="BIBLIOTHÈQUE D'EFFETS">
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns:
                                    "repeat(auto-fit,minmax(150px,1fr))",
                                gap: 7,
                            }}
                        >
                            {effects.map((effect) => (
                                <div
                                    key={effect.id}
                                    style={{
                                        background:
                                            CATEGORY.panel2,
                                        borderRadius: 7,
                                        padding: 10,
                                    }}
                                >
                                    <strong>{effect.name}</strong>
                                    <div
                                        style={{
                                            color:
                                                CATEGORY.muted,
                                            fontSize: 10,
                                            margin:
                                                "4px 0 8px",
                                        }}
                                    >
                                        {effect.effect_type}
                                    </div>

                                    <ControlButton
                                        danger
                                        onClick={() =>
                                            removeResource(
                                                deleteEffect,
                                                effect.id,
                                                effect.name
                                            )
                                        }
                                    >
                                        SUPPRIMER
                                    </ControlButton>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </div>
            )}

            {activeTab === "animations" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1.5fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="ANIMATION TEXTE">
                        <form
                            onSubmit={handleCreateAnimation}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Titre"
                                value={animationForm.title}
                                onChange={(e) =>
                                    setAnimationForm({
                                        ...animationForm,
                                        title: e.target.value,
                                    })
                                }
                                required
                            />

                            <textarea
                                placeholder="Texte à afficher"
                                value={animationForm.text}
                                onChange={(e) =>
                                    setAnimationForm({
                                        ...animationForm,
                                        text: e.target.value,
                                    })
                                }
                                rows={3}
                                required
                            />

                            <select
                                value={animationForm.animation_type}
                                onChange={(e) =>
                                    setAnimationForm({
                                        ...animationForm,
                                        animation_type:
                                            e.target.value,
                                    })
                                }
                            >
                                <option>FADE</option>
                                <option>SLIDE</option>
                                <option>ZOOM</option>
                                <option>TYPEWRITER</option>
                                <option>MARQUEE</option>
                            </select>

                            <select
                                value={animationForm.position}
                                onChange={(e) =>
                                    setAnimationForm({
                                        ...animationForm,
                                        position:
                                            e.target.value,
                                    })
                                }
                            >
                                <option>TOP</option>
                                <option>CENTER</option>
                                <option>BOTTOM</option>
                            </select>

                            <input
                                type="number"
                                min="1"
                                value={animationForm.duration}
                                onChange={(e) =>
                                    setAnimationForm({
                                        ...animationForm,
                                        duration:
                                            e.target.value,
                                    })
                                }
                            />

                            <ControlButton success>
                                + AJOUTER ANIMATION
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="ANIMATIONS DISPONIBLES">
                        <div
                            style={{
                                display: "grid",
                                gap: 7,
                            }}
                        >
                            {animations.map((animation) => (
                                <div
                                    key={animation.id}
                                    style={{
                                        background:
                                            CATEGORY.panel2,
                                        borderRadius: 7,
                                        padding: 10,
                                        display: "flex",
                                        justifyContent:
                                            "space-between",
                                        gap: 10,
                                    }}
                                >
                                    <div>
                                        <strong>
                                            {animation.title}
                                        </strong>
                                        <div
                                            style={{
                                                fontSize: 11,
                                                color:
                                                    CATEGORY.muted,
                                            }}
                                        >
                                            {animation.text}
                                        </div>
                                    </div>

                                    <ControlButton
                                        danger
                                        onClick={() =>
                                            removeResource(
                                                deleteAnimation,
                                                animation.id,
                                                animation.title
                                            )
                                        }
                                    >
                                        SUPPR.
                                    </ControlButton>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </div>
            )}

            {activeTab === "audio" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1.5fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="CONTRÔLE AUDIO">
                        <form
                            onSubmit={handleCreateAudio}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Nom"
                                value={audioForm.name}
                                onChange={(e) =>
                                    setAudioForm({
                                        ...audioForm,
                                        name: e.target.value,
                                    })
                                }
                                required
                            />

                            <label
                                style={{
                                    fontSize: 11,
                                    color:
                                        CATEGORY.muted,
                                }}
                            >
                                Volume : {audioForm.volume}%
                            </label>

                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={audioForm.volume}
                                onChange={(e) =>
                                    setAudioForm({
                                        ...audioForm,
                                        volume:
                                            e.target.value,
                                    })
                                }
                            />

                            <input
                                placeholder="Effet audio"
                                value={audioForm.audio_effect}
                                onChange={(e) =>
                                    setAudioForm({
                                        ...audioForm,
                                        audio_effect:
                                            e.target.value,
                                    })
                                }
                            />

                            <label
                                style={{
                                    fontSize: 12,
                                }}
                            >
                                <input
                                    type="checkbox"
                                    checked={
                                        audioForm.muted
                                    }
                                    onChange={(e) =>
                                        setAudioForm({
                                            ...audioForm,
                                            muted:
                                                e.target.checked,
                                        })
                                    }
                                />{" "}
                                Muet
                            </label>

                            <ControlButton success>
                                + AJOUTER AUDIO
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="MIXAGE">
                        <div
                            style={{
                                display: "grid",
                                gap: 7,
                            }}
                        >
                            {audio.map((item) => (
                                <div
                                    key={item.id}
                                    style={{
                                        background:
                                            CATEGORY.panel2,
                                        padding: 10,
                                        borderRadius: 7,
                                        display: "flex",
                                        justifyContent:
                                            "space-between",
                                        alignItems:
                                            "center",
                                    }}
                                >
                                    <div>
                                        <strong>
                                            {item.name}
                                        </strong>
                                        <div
                                            style={{
                                                fontSize: 10,
                                                color:
                                                    CATEGORY.muted,
                                            }}
                                        >
                                            Volume :{" "}
                                            {item.volume}%
                                        </div>
                                    </div>

                                    <ControlButton
                                        danger
                                        onClick={() =>
                                            removeResource(
                                                deleteAudioControl,
                                                item.id,
                                                item.name
                                            )
                                        }
                                    >
                                        SUPPR.
                                    </ControlButton>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </div>
            )}

            {activeTab === "scenes" && (
                <Panel
                    title="SCÈNES DE RÉALISATION"
                    right={
                        <ControlButton
                            success
                            onClick={handleCreateScene}
                        >
                            + NOUVELLE SCÈNE
                        </ControlButton>
                    }
                >
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fit,minmax(190px,1fr))",
                            gap: 8,
                        }}
                    >
                        {scenes.map((scene) => (
                            <div
                                key={scene.id}
                                style={{
                                    padding: 12,
                                    background:
                                        CATEGORY.panel2,
                                    borderRadius: 7,
                                }}
                            >
                                <strong>{scene.name}</strong>
                                <div
                                    style={{
                                        color:
                                            CATEGORY.muted,
                                        fontSize: 10,
                                        marginTop: 4,
                                    }}
                                >
                                    Scène de production
                                </div>

                                <div style={{ marginTop: 8 }}>
                                    <ControlButton
                                        danger
                                        onClick={() =>
                                            removeResource(
                                                deleteScene,
                                                scene.id,
                                                scene.name
                                            )
                                        }
                                    >
                                        SUPPRIMER
                                    </ControlButton>
                                </div>
                            </div>
                        ))}
                    </div>
                </Panel>
            )}

            {activeTab === "schedule" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1.5fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="PROGRAMMER UNE ÉMISSION">
                        <form
                            onSubmit={handleCreateSchedule}
                            style={{
                                display: "grid",
                                gap: 8,
                            }}
                        >
                            <input
                                placeholder="Titre"
                                value={scheduleForm.title}
                                onChange={(e) =>
                                    setScheduleForm({
                                        ...scheduleForm,
                                        title: e.target.value,
                                    })
                                }
                                required
                            />

                            <label
                                style={{
                                    fontSize: 10,
                                    color:
                                        CATEGORY.muted,
                                }}
                            >
                                Début
                            </label>

                            <input
                                type="datetime-local"
                                value={scheduleForm.start_time}
                                onChange={(e) =>
                                    setScheduleForm({
                                        ...scheduleForm,
                                        start_time:
                                            e.target.value,
                                    })
                                }
                                required
                            />

                            <label
                                style={{
                                    fontSize: 10,
                                    color:
                                        CATEGORY.muted,
                                }}
                            >
                                Fin
                            </label>

                            <input
                                type="datetime-local"
                                value={scheduleForm.end_time}
                                onChange={(e) =>
                                    setScheduleForm({
                                        ...scheduleForm,
                                        end_time:
                                            e.target.value,
                                    })
                                }
                                required
                            />

                            <label
                                style={{
                                    fontSize: 12,
                                }}
                            >
                                <input
                                    type="checkbox"
                                    checked={
                                        scheduleForm.live
                                    }
                                    onChange={(e) =>
                                        setScheduleForm({
                                            ...scheduleForm,
                                            live:
                                                e.target.checked,
                                        })
                                    }
                                />{" "}
                                Direct
                            </label>

                            <ControlButton success>
                                + PROGRAMMER
                            </ControlButton>
                        </form>
                    </Panel>

                    <Panel title="PROGRAMMATION">
                        <div
                            style={{
                                display: "grid",
                                gap: 7,
                            }}
                        >
                            {schedules.map((schedule) => (
                                <div
                                    key={schedule.id}
                                    style={{
                                        background:
                                            CATEGORY.panel2,
                                        padding: 10,
                                        borderRadius: 7,
                                    }}
                                >
                                    <strong>
                                        {schedule.title}
                                    </strong>
                                    <div
                                        style={{
                                            color:
                                                CATEGORY.muted,
                                            fontSize: 10,
                                        }}
                                    >
                                        {schedule.start_time} →{" "}
                                        {schedule.end_time}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </div>
            )}

            {activeTab === "broadcast" && (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "minmax(280px,1fr) minmax(280px,1fr)",
                        gap: 10,
                    }}
                >
                    <Panel title="PUBLICATION DIRECTE">
                        <div
                            style={{
                                display: "grid",
                                gap: 9,
                            }}
                        >
                            <select
                                value={selectedStream}
                                onChange={(e) =>
                                    setSelectedStream(
                                        e.target.value
                                    )
                                }
                            >
                                <option value="">
                                    Choisir LiveStream
                                </option>
                                {streams.map((stream) => (
                                    <option
                                        key={stream.id}
                                        value={stream.id}
                                    >
                                        {stream.title}
                                    </option>
                                ))}
                            </select>

                            <select
                                value={selectedChannel}
                                onChange={(e) =>
                                    setSelectedChannel(
                                        e.target.value
                                    )
                                }
                            >
                                <option value="">
                                    Choisir chaîne TV
                                </option>
                                {channels.map((channel) => (
                                    <option
                                        key={channel.id}
                                        value={channel.id}
                                    >
                                        {channel.title}
                                    </option>
                                ))}
                            </select>

                            <div
                                style={{
                                    display: "flex",
                                    gap: 7,
                                    flexWrap: "wrap",
                                }}
                            >
                                <ControlButton
                                    danger
                                    onClick={handlePublish}
                                >
                                    🔴 PUBLIER
                                </ControlButton>

                                <ControlButton
                                    onClick={handleUnpublish}
                                >
                                    RETIRER DU DIRECT
                                </ControlButton>
                            </div>
                        </div>
                    </Panel>

                    <Panel title="ÉTAT DE LA DIFFUSION">
                        <div
                            style={{
                                padding: 20,
                                background:
                                    CATEGORY.panel2,
                                borderRadius: 8,
                                textAlign: "center",
                            }}
                        >
                            <div
                                style={{
                                    fontSize: 30,
                                    fontWeight: 900,
                                    color: onAir
                                        ? "#ff7676"
                                        : CATEGORY.muted,
                                }}
                            >
                                {onAir
                                    ? "● ON AIR"
                                    : "○ OFF AIR"}
                            </div>

                            <div
                                style={{
                                    color:
                                        CATEGORY.muted,
                                    marginTop: 7,
                                    fontSize: 11,
                                }}
                            >
                                {programSource
                                    ? `PROGRAM : ${sourceName(
                                          programSource
                                      )}`
                                    : "Aucun programme sélectionné"}
                            </div>
                        </div>
                    </Panel>
                </div>
            )}

            <div
                style={{
                    marginTop: 12,
                    padding: "8px 10px",
                    border: `1px solid ${CATEGORY.border}`,
                    borderRadius: 7,
                    color: CATEGORY.muted,
                    fontSize: 10,
                }}
            >
                NSIKAY TV Régie V2 • Les commandes PREVIEW/PROGRAM et les
                compositions sont préparées côté interface. Les flux
                physiques réels (RTSP, RTMP, HDMI, SDI, WebRTC, téléphones)
                nécessitent ensuite leur passerelle d'acquisition/diffusion
                appropriée.
            </div>
        </div>
    );
}




