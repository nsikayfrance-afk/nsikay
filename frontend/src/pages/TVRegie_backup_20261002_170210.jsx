import { useEffect, useMemo, useState } from "react";

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
} from "../services/tvRegie";

import { getTVChannels } from "../services/tv";


const CAMERA_TYPES = [
    {
        value: "IP",
        label: "Caméra IP",
    },
    {
        value: "RTMP",
        label: "Source RTMP",
    },
    {
        value: "HDMI",
        label: "Capture HDMI",
    },
    {
        value: "SDI",
        label: "Broadcast SDI",
    },
    {
        value: "WEBRTC",
        label: "WebRTC Live",
    },
];


function normalize(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (Array.isArray(data?.results)) {
        return data.results;
    }

    if (Array.isArray(data?.data)) {
        return data.data;
    }

    if (Array.isArray(data?.channels)) {
        return data.channels;
    }

    return [];
}


function cameraTypeLabel(type) {
    return (
        CAMERA_TYPES.find(
            (item) => item.value === type
        )?.label || type
    );
}


export default function TVRegie() {

    const [cameras, setCameras] = useState([]);
    const [streams, setStreams] = useState([]);
    const [channels, setChannels] = useState([]);

    const [selectedCamera, setSelectedCamera] =
        useState(null);

    const [selectedStream, setSelectedStream] =
        useState(null);

    const [selectedChannel, setSelectedChannel] =
        useState("");

    const [loading, setLoading] =
        useState(true);

    const [saving, setSaving] =
        useState(false);

    const [message, setMessage] =
        useState("");

    const [error, setError] =
        useState("");

    const [cameraForm, setCameraForm] = useState({
        name: "",
        source_type: "IP",
        source_url: "",
        resolution: "4K",
        frame_rate: 60,
        description: "",
    });

    const [streamForm, setStreamForm] = useState({
        title: "",
        camera: "",
        stream_url: "",
        quality: "4K Ultra HD",
        recording_enabled: true,
    });


    async function loadData() {

        try {

            setLoading(true);
            setError("");

            const [
                camerasData,
                streamsData,
                channelsData,
            ] = await Promise.all([
                getCameras(),
                getStreams(),
                getTVChannels(),
            ]);

            const cameraItems =
                normalize(camerasData);

            const streamItems =
                normalize(streamsData);

            const channelItems =
                normalize(channelsData);

            setCameras(cameraItems);
            setStreams(streamItems);
            setChannels(channelItems);

            if (
                selectedCamera &&
                !cameraItems.some(
                    (camera) =>
                        camera.id === selectedCamera.id
                )
            ) {
                setSelectedCamera(null);
            }

            if (
                selectedStream &&
                !streamItems.some(
                    (stream) =>
                        stream.id === selectedStream.id
                )
            ) {
                setSelectedStream(null);
            }

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de charger la régie TV."
            );

        } finally {

            setLoading(false);

        }
    }


    useEffect(() => {
        loadData();
    }, []);


    function updateCameraField(field, value) {

        setCameraForm(
            (current) => ({
                ...current,
                [field]: value,
            })
        );

    }


    function updateStreamField(field, value) {

        setStreamForm(
            (current) => ({
                ...current,
                [field]: value,
            })
        );

    }


    async function handleCreateCamera(event) {

        event.preventDefault();

        try {

            setSaving(true);
            setError("");
            setMessage("");

            const payload = {
                ...cameraForm,
                frame_rate:
                    Number(cameraForm.frame_rate),
            };

            const created =
                await createCamera(payload);

            setMessage(
                `Caméra "${created.name}" créée avec succès.`
            );

            setCameraForm({
                name: "",
                source_type: "IP",
                source_url: "",
                resolution: "4K",
                frame_rate: 60,
                description: "",
            });

            await loadData();

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de créer la caméra."
            );

        } finally {

            setSaving(false);

        }
    }


    async function handleToggleCamera(camera) {

        try {

            setError("");
            setMessage("");

            const updated =
                await updateCamera(
                    camera.id,
                    {
                        is_live: !camera.is_live,
                    }
                );

            setCameras(
                (current) =>
                    current.map(
                        (item) =>
                            item.id === updated.id
                                ? updated
                                : item
                    )
            );

            setSelectedCamera(updated);

            setMessage(
                updated.is_live
                    ? `Caméra "${updated.name}" activée.`
                    : `Caméra "${updated.name}" arrêtée.`
            );

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de modifier la caméra."
            );

        }
    }


    async function handleDeleteCamera(camera) {

        const confirmed =
            window.confirm(
                `Supprimer la caméra "${camera.name}" ?`
            );

        if (!confirmed) {
            return;
        }

        try {

            setError("");
            setMessage("");

            await deleteCamera(camera.id);

            if (
                selectedCamera?.id === camera.id
            ) {
                setSelectedCamera(null);
            }

            await loadData();

            setMessage(
                `Caméra "${camera.name}" supprimée.`
            );

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de supprimer la caméra."
            );

        }
    }


    async function handleCreateStream(event) {

        event.preventDefault();

        if (!streamForm.camera) {

            setError(
                "Sélectionne une caméra pour créer le LiveStream."
            );

            return;
        }

        try {

            setSaving(true);
            setError("");
            setMessage("");

            const payload = {
                ...streamForm,
                camera: Number(streamForm.camera),
            };

            const created =
                await createStream(payload);

            setMessage(
                `LiveStream "${created.title}" créé.`
            );

            setStreamForm({
                title: "",
                camera: "",
                stream_url: "",
                quality: "4K Ultra HD",
                recording_enabled: true,
            });

            await loadData();

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de créer le LiveStream."
            );

        } finally {

            setSaving(false);

        }
    }


    async function handlePublish() {

        if (!selectedStream) {

            setError(
                "Sélectionne d'abord un LiveStream."
            );

            return;
        }

        if (!selectedChannel) {

            setError(
                "Sélectionne d'abord une chaîne TV."
            );

            return;
        }

        try {

            setSaving(true);
            setError("");
            setMessage("");

            const result =
                await publishStream(
                    selectedStream.id,
                    Number(selectedChannel)
                );

            setMessage(
                result?.message ||
                "LiveStream publié sur la chaîne TV."
            );

            await loadData();

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de publier le LiveStream."
            );

        } finally {

            setSaving(false);

        }
    }


    async function handleUnpublish() {

        if (!selectedStream) {

            setError(
                "Sélectionne d'abord un LiveStream."
            );

            return;
        }

        try {

            setSaving(true);
            setError("");
            setMessage("");

            const result =
                await unpublishStream(
                    selectedStream.id
                );

            setMessage(
                result?.message ||
                "Diffusion arrêtée."
            );

            await loadData();

        } catch (err) {

            setError(
                err?.message ||
                "Impossible d'arrêter la diffusion."
            );

        } finally {

            setSaving(false);

        }
    }


    async function handleDeleteStream(stream) {

        const confirmed =
            window.confirm(
                `Supprimer le LiveStream "${stream.title}" ?`
            );

        if (!confirmed) {
            return;
        }

        try {

            setError("");
            setMessage("");

            await deleteStream(stream.id);

            if (
                selectedStream?.id === stream.id
            ) {
                setSelectedStream(null);
            }

            await loadData();

            setMessage(
                `LiveStream "${stream.title}" supprimé.`
            );

        } catch (err) {

            setError(
                err?.message ||
                "Impossible de supprimer le LiveStream."
            );

        }
    }


    const selectedCameraStream =
        selectedCamera?.source_url || "";


    const selectedStreamData =
        useMemo(
            () =>
                streams.find(
                    (stream) =>
                        stream.id ===
                        selectedStream?.id
                ) || selectedStream,
            [streams, selectedStream]
        );


    if (loading) {

        return (
            <div style={styles.loading}>
                <div style={styles.loadingIcon}>
                    📺
                </div>

                <h2>
                    Chargement de la Régie TV...
                </h2>

                <p>
                    Connexion aux systèmes NSIKAY TV.
                </p>
            </div>
        );

    }


    return (
        <div style={styles.page}>

            <header style={styles.header}>

                <div>
                    <div style={styles.eyebrow}>
                        NSIKAY TV
                    </div>

                    <h1 style={styles.title}>
                        Régie audiovisuelle
                    </h1>

                    <p style={styles.subtitle}>
                        Caméras, sources, LiveStreams et
                        diffusion des chaînes NSIKAY.
                    </p>
                </div>

                <button
                    type="button"
                    onClick={loadData}
                    style={styles.refresh}
                >
                    ↻ Actualiser
                </button>

            </header>


            {error && (
                <div style={styles.error}>
                    <strong>Erreur</strong>
                    <div>{error}</div>
                </div>
            )}


            {message && (
                <div style={styles.success}>
                    <strong>NSIKAY TV</strong>
                    <div>{message}</div>
                </div>
            )}


            <main style={styles.container}>

                {/* =================================================
                    MONITEUR
                ================================================= */}

                <section style={styles.monitorSection}>

                    <div style={styles.sectionHeader}>

                        <div>
                            <h2 style={styles.sectionTitle}>
                                Moniteur de régie
                            </h2>

                            <p style={styles.sectionText}>
                                Prévisualisation de la caméra ou
                                du flux sélectionné.
                            </p>
                        </div>

                        {selectedCamera?.is_live && (
                            <span style={styles.liveBadge}>
                                ● CAMÉRA ACTIVE
                            </span>
                        )}

                    </div>


                    <div style={styles.monitor}>

                        {selectedStreamData?.stream_url ? (

                            <video
                                src={
                                    selectedStreamData.stream_url
                                }
                                controls
                                autoPlay
                                muted
                                style={styles.video}
                            />

                        ) : selectedCameraStream ? (

                            <video
                                src={selectedCameraStream}
                                controls
                                muted
                                style={styles.video}
                            />

                        ) : (

                            <div style={styles.noSignal}>

                                <div style={styles.noSignalIcon}>
                                    📹
                                </div>

                                <h2>
                                    Aucun signal sélectionné
                                </h2>

                                <p>
                                    Sélectionne une caméra ou
                                    un LiveStream.
                                </p>

                            </div>

                        )}

                    </div>

                </section>


                {/* =================================================
                    CAMERAS
                ================================================= */}

                <section style={styles.grid}>

                    <div style={styles.card}>

                        <div style={styles.cardHeader}>
                            <div>
                                <h2 style={styles.cardTitle}>
                                    Caméras
                                </h2>

                                <span style={styles.count}>
                                    {cameras.length} source(s)
                                </span>
                            </div>
                        </div>


                        <div style={styles.cameraList}>

                            {cameras.length === 0 && (
                                <div style={styles.empty}>
                                    Aucune caméra enregistrée.
                                </div>
                            )}


                            {cameras.map((camera) => {

                                const active =
                                    selectedCamera?.id ===
                                    camera.id;

                                return (
                                    <button
                                        key={camera.id}
                                        type="button"
                                        onClick={() =>
                                            setSelectedCamera(camera)
                                        }
                                        style={{
                                            ...styles.cameraItem,
                                            ...(active
                                                ? styles.cameraItemActive
                                                : {}),
                                        }}
                                    >

                                        <div style={styles.cameraIcon}>
                                            📹
                                        </div>

                                        <div style={styles.itemText}>

                                            <strong>
                                                {camera.name}
                                            </strong>

                                            <span>
                                                {cameraTypeLabel(
                                                    camera.source_type
                                                )}
                                                {" • "}
                                                {camera.resolution}
                                                {" • "}
                                                {camera.frame_rate} FPS
                                            </span>

                                        </div>

                                        <span
                                            style={
                                                camera.is_live
                                                    ? styles.statusLive
                                                    : styles.statusOff
                                            }
                                        >
                                            {camera.is_live
                                                ? "LIVE"
                                                : "OFF"}
                                        </span>

                                    </button>
                                );

                            })}

                        </div>

                    </div>


                    {/* =================================================
                        AJOUT CAMERA
                    ================================================= */}

                    <div style={styles.card}>

                        <div style={styles.cardHeader}>
                            <div>
                                <h2 style={styles.cardTitle}>
                                    Ajouter une caméra
                                </h2>

                                <span style={styles.count}>
                                    Source audiovisuelle
                                </span>
                            </div>
                        </div>


                        <form
                            onSubmit={handleCreateCamera}
                            style={styles.form}
                        >

                            <label style={styles.label}>
                                Nom

                                <input
                                    value={cameraForm.name}
                                    onChange={(event) =>
                                        updateCameraField(
                                            "name",
                                            event.target.value
                                        )
                                    }
                                    placeholder="Caméra principale"
                                    required
                                    style={styles.input}
                                />
                            </label>


                            <label style={styles.label}>
                                Type de source

                                <select
                                    value={
                                        cameraForm.source_type
                                    }
                                    onChange={(event) =>
                                        updateCameraField(
                                            "source_type",
                                            event.target.value
                                        )
                                    }
                                    style={styles.input}
                                >

                                    {CAMERA_TYPES.map(
                                        (type) => (
                                            <option
                                                key={type.value}
                                                value={type.value}
                                            >
                                                {type.label}
                                            </option>
                                        )
                                    )}

                                </select>

                            </label>


                            <label style={styles.label}>
                                URL de la source

                                <input
                                    type="url"
                                    value={
                                        cameraForm.source_url
                                    }
                                    onChange={(event) =>
                                        updateCameraField(
                                            "source_url",
                                            event.target.value
                                        )
                                    }
                                    placeholder="https://..."
                                    style={styles.input}
                                />

                                <small style={styles.help}>
                                    Pour une caméra IP/RTMP/WebRTC,
                                    indique l'URL réellement fournie
                                    par ton système de diffusion.
                                </small>
                            </label>


                            <div style={styles.twoColumns}>

                                <label style={styles.label}>
                                    Résolution

                                    <select
                                        value={
                                            cameraForm.resolution
                                        }
                                        onChange={(event) =>
                                            updateCameraField(
                                                "resolution",
                                                event.target.value
                                            )
                                        }
                                        style={styles.input}
                                    >
                                        <option>4K</option>
                                        <option>1080p</option>
                                        <option>720p</option>
                                        <option>480p</option>
                                    </select>
                                </label>


                                <label style={styles.label}>
                                    FPS

                                    <input
                                        type="number"
                                        min="1"
                                        max="240"
                                        value={
                                            cameraForm.frame_rate
                                        }
                                        onChange={(event) =>
                                            updateCameraField(
                                                "frame_rate",
                                                event.target.value
                                            )
                                        }
                                        style={styles.input}
                                    />
                                </label>

                            </div>


                            <label style={styles.label}>
                                Description

                                <textarea
                                    value={
                                        cameraForm.description
                                    }
                                    onChange={(event) =>
                                        updateCameraField(
                                            "description",
                                            event.target.value
                                        )
                                    }
                                    rows="3"
                                    style={styles.textarea}
                                    placeholder="Description de la caméra..."
                                />

                            </label>


                            <button
                                type="submit"
                                disabled={saving}
                                style={styles.primaryButton}
                            >
                                {saving
                                    ? "Enregistrement..."
                                    : "＋ Ajouter la caméra"}
                            </button>

                        </form>

                    </div>

                </section>


                {/* =================================================
                    ACTION CAMERA
                ================================================= */}

                {selectedCamera && (
                    <section style={styles.card}>

                        <div style={styles.sectionHeader}>

                            <div>
                                <h2 style={styles.cardTitle}>
                                    Caméra sélectionnée
                                </h2>

                                <p style={styles.sectionText}>
                                    {selectedCamera.name}
                                    {" • "}
                                    {cameraTypeLabel(
                                        selectedCamera.source_type
                                    )}
                                </p>
                            </div>

                            <div style={styles.actions}>

                                <button
                                    type="button"
                                    onClick={() =>
                                        handleToggleCamera(
                                            selectedCamera
                                        )
                                    }
                                    style={
                                        selectedCamera.is_live
                                            ? styles.warningButton
                                            : styles.primaryButton
                                    }
                                >
                                    {selectedCamera.is_live
                                        ? "■ Arrêter caméra"
                                        : "▶ Activer caméra"}
                                </button>


                                <button
                                    type="button"
                                    onClick={() =>
                                        handleDeleteCamera(
                                            selectedCamera
                                        )
                                    }
                                    style={styles.dangerButton}
                                >
                                    Supprimer
                                </button>

                            </div>

                        </div>

                    </section>
                )}


                {/* =================================================
                    LIVE STREAM
                ================================================= */}

                <section style={styles.grid}>

                    <div style={styles.card}>

                        <div style={styles.cardHeader}>

                            <div>
                                <h2 style={styles.cardTitle}>
                                    LiveStreams
                                </h2>

                                <span style={styles.count}>
                                    {streams.length} flux
                                </span>
                            </div>

                        </div>


                        <div style={styles.streamList}>

                            {streams.length === 0 && (
                                <div style={styles.empty}>
                                    Aucun LiveStream.
                                </div>
                            )}


                            {streams.map((stream) => {

                                const active =
                                    selectedStream?.id ===
                                    stream.id;

                                const camera =
                                    cameras.find(
                                        (item) =>
                                            item.id ===
                                            stream.camera
                                    );

                                return (
                                    <button
                                        key={stream.id}
                                        type="button"
                                        onClick={() =>
                                            setSelectedStream(
                                                stream
                                            )
                                        }
                                        style={{
                                            ...styles.streamItem,
                                            ...(active
                                                ? styles.streamItemActive
                                                : {}),
                                        }}
                                    >

                                        <div style={styles.streamIcon}>
                                            ▶
                                        </div>

                                        <div style={styles.itemText}>

                                            <strong>
                                                {stream.title}
                                            </strong>

                                            <span>
                                                Caméra :{" "}
                                                {camera?.name ||
                                                    `#${stream.camera}`}
                                            </span>

                                            <span>
                                                {stream.quality}
                                            </span>

                                        </div>

                                        <span style={styles.streamStatus}>
                                            STREAM
                                        </span>

                                    </button>
                                );

                            })}

                        </div>

                    </div>


                    {/* =================================================
                        CREATION STREAM
                    ================================================= */}

                    <div style={styles.card}>

                        <div style={styles.cardHeader}>
                            <div>
                                <h2 style={styles.cardTitle}>
                                    Créer un LiveStream
                                </h2>

                                <span style={styles.count}>
                                    Flux de diffusion
                                </span>
                            </div>
                        </div>


                        <form
                            onSubmit={handleCreateStream}
                            style={styles.form}
                        >

                            <label style={styles.label}>
                                Titre

                                <input
                                    value={streamForm.title}
                                    onChange={(event) =>
                                        updateStreamField(
                                            "title",
                                            event.target.value
                                        )
                                    }
                                    placeholder="NSIKAY Live"
                                    required
                                    style={styles.input}
                                />

                            </label>


                            <label style={styles.label}>
                                Caméra

                                <select
                                    value={streamForm.camera}
                                    onChange={(event) =>
                                        updateStreamField(
                                            "camera",
                                            event.target.value
                                        )
                                    }
                                    required
                                    style={styles.input}
                                >

                                    <option value="">
                                        Sélectionner une caméra
                                    </option>

                                    {cameras.map(
                                        (camera) => (
                                            <option
                                                key={camera.id}
                                                value={camera.id}
                                            >
                                                {camera.name}
                                            </option>
                                        )
                                    )}

                                </select>

                            </label>


                            <label style={styles.label}>
                                URL du flux

                                <input
                                    type="url"
                                    value={
                                        streamForm.stream_url
                                    }
                                    onChange={(event) =>
                                        updateStreamField(
                                            "stream_url",
                                            event.target.value
                                        )
                                    }
                                    placeholder="https://..."
                                    required
                                    style={styles.input}
                                />

                                <small style={styles.help}>
                                    URL du flux réellement produit
                                    par le serveur ou l'encodeur.
                                </small>

                            </label>


                            <label style={styles.label}>
                                Qualité

                                <select
                                    value={
                                        streamForm.quality
                                    }
                                    onChange={(event) =>
                                        updateStreamField(
                                            "quality",
                                            event.target.value
                                        )
                                    }
                                    style={styles.input}
                                >
                                    <option>
                                        4K Ultra HD
                                    </option>
                                    <option>
                                        Full HD 1080p
                                    </option>
                                    <option>
                                        HD 720p
                                    </option>
                                    <option>
                                        SD
                                    </option>
                                </select>

                            </label>


                            <label style={styles.checkbox}>
                                <input
                                    type="checkbox"
                                    checked={
                                        streamForm.recording_enabled
                                    }
                                    onChange={(event) =>
                                        updateStreamField(
                                            "recording_enabled",
                                            event.target.checked
                                        )
                                    }
                                />

                                Enregistrer le direct
                            </label>


                            <button
                                type="submit"
                                disabled={saving}
                                style={styles.primaryButton}
                            >
                                {saving
                                    ? "Création..."
                                    : "＋ Créer le LiveStream"}
                            </button>

                        </form>

                    </div>

                </section>


                {/* =================================================
                    PUBLICATION
                ================================================= */}

                {selectedStream && (
                    <section style={styles.card}>

                        <div style={styles.sectionHeader}>

                            <div>
                                <h2 style={styles.cardTitle}>
                                    Diffusion TV
                                </h2>

                                <p style={styles.sectionText}>
                                    LiveStream sélectionné :{" "}
                                    <strong>
                                        {selectedStream.title}
                                    </strong>
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={() =>
                                    handleDeleteStream(
                                        selectedStream
                                    )
                                }
                                style={styles.dangerButton}
                            >
                                Supprimer le flux
                            </button>

                        </div>


                        <div style={styles.broadcastGrid}>

                            <label style={styles.label}>
                                Chaîne NSIKAY TV

                                <select
                                    value={selectedChannel}
                                    onChange={(event) =>
                                        setSelectedChannel(
                                            event.target.value
                                        )
                                    }
                                    style={styles.input}
                                >

                                    <option value="">
                                        Sélectionner une chaîne
                                    </option>

                                    {channels.map(
                                        (channel) => (
                                            <option
                                                key={channel.id}
                                                value={channel.id}
                                            >
                                                {channel.title}
                                            </option>
                                        )
                                    )}

                                </select>

                            </label>


                            <div style={styles.actions}>

                                <button
                                    type="button"
                                    onClick={handlePublish}
                                    disabled={saving}
                                    style={styles.primaryButton}
                                >
                                    🚀 Publier sur NSIKAY TV
                                </button>


                                <button
                                    type="button"
                                    onClick={handleUnpublish}
                                    disabled={saving}
                                    style={styles.warningButton}
                                >
                                    ■ Arrêter diffusion
                                </button>

                            </div>

                        </div>

                    </section>
                )}

            </main>

        </div>
    );
}


const styles = {

    page: {
        minHeight: "100vh",
        background: "#f4f7fb",
        color: "#172033",
        paddingBottom: "60px",
    },

    header: {
        background:
            "linear-gradient(135deg, #07111f, #102b4c)",
        color: "white",
        padding: "45px 28px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "20px",
    },

    eyebrow: {
        fontSize: "13px",
        fontWeight: 900,
        letterSpacing: "2px",
        opacity: 0.75,
    },

    title: {
        margin: "8px 0",
        fontSize: "clamp(30px, 5vw, 52px)",
        fontWeight: 900,
    },

    subtitle: {
        margin: 0,
        opacity: 0.8,
        fontSize: "17px",
    },

    refresh: {
        border: "1px solid rgba(255,255,255,.3)",
        background: "rgba(255,255,255,.08)",
        color: "white",
        borderRadius: "12px",
        padding: "12px 18px",
        cursor: "pointer",
        fontWeight: 800,
    },

    container: {
        maxWidth: "1450px",
        margin: "0 auto",
        padding: "28px",
    },

    monitorSection: {
        background: "white",
        borderRadius: "20px",
        padding: "20px",
        boxShadow:
            "0 12px 40px rgba(0,0,0,.08)",
        marginBottom: "22px",
    },

    sectionHeader: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "20px",
        flexWrap: "wrap",
    },

    sectionTitle: {
        margin: 0,
        fontSize: "24px",
    },

    sectionText: {
        margin: "5px 0 0",
        color: "#667085",
    },

    monitor: {
        marginTop: "18px",
        aspectRatio: "16 / 9",
        background: "#03070d",
        borderRadius: "16px",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },

    video: {
        width: "100%",
        height: "100%",
        objectFit: "contain",
    },

    noSignal: {
        color: "white",
        textAlign: "center",
        padding: "30px",
    },

    noSignalIcon: {
        fontSize: "65px",
        marginBottom: "10px",
    },

    grid: {
        display: "grid",
        gridTemplateColumns:
            "minmax(0, 1fr) minmax(0, 1fr)",
        gap: "22px",
        marginBottom: "22px",
    },

    card: {
        background: "white",
        borderRadius: "20px",
        padding: "22px",
        boxShadow:
            "0 10px 35px rgba(0,0,0,.07)",
        marginBottom: "22px",
    },

    cardHeader: {
        marginBottom: "18px",
    },

    cardTitle: {
        margin: 0,
        fontSize: "21px",
        fontWeight: 900,
    },

    count: {
        display: "block",
        marginTop: "4px",
        color: "#667085",
        fontSize: "13px",
    },

    cameraList: {
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        maxHeight: "400px",
        overflowY: "auto",
    },

    cameraItem: {
        width: "100%",
        border: "1px solid #e4e7ec",
        borderRadius: "12px",
        background: "white",
        padding: "12px",
        display: "flex",
        alignItems: "center",
        gap: "12px",
        cursor: "pointer",
        textAlign: "left",
    },

    cameraItemActive: {
        border: "2px solid #102b4c",
        background: "#f2f6fa",
    },

    cameraIcon: {
        width: "45px",
        height: "45px",
        borderRadius: "10px",
        background: "#edf2f7",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "22px",
        flexShrink: 0,
    },

    itemText: {
        minWidth: 0,
        flex: 1,
        display: "flex",
        flexDirection: "column",
        gap: "3px",
    },

    statusLive: {
        color: "#16803c",
        fontWeight: 900,
        fontSize: "11px",
    },

    statusOff: {
        color: "#98a2b3",
        fontWeight: 900,
        fontSize: "11px",
    },

    streamList: {
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        maxHeight: "400px",
        overflowY: "auto",
    },

    streamItem: {
        width: "100%",
        border: "1px solid #e4e7ec",
        borderRadius: "12px",
        background: "white",
        padding: "12px",
        display: "flex",
        alignItems: "center",
        gap: "12px",
        cursor: "pointer",
        textAlign: "left",
    },

    streamItemActive: {
        border: "2px solid #102b4c",
        background: "#f2f6fa",
    },

    streamIcon: {
        width: "45px",
        height: "45px",
        borderRadius: "10px",
        background: "#edf2f7",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "20px",
        flexShrink: 0,
    },

    streamStatus: {
        color: "#175cd3",
        fontSize: "10px",
        fontWeight: 900,
    },

    form: {
        display: "flex",
        flexDirection: "column",
        gap: "14px",
    },

    label: {
        display: "flex",
        flexDirection: "column",
        gap: "6px",
        fontWeight: 700,
        fontSize: "14px",
    },

    input: {
        width: "100%",
        boxSizing: "border-box",
        border: "1px solid #d0d5dd",
        borderRadius: "10px",
        padding: "12px 13px",
        background: "white",
        fontSize: "14px",
        outline: "none",
    },

    textarea: {
        width: "100%",
        boxSizing: "border-box",
        border: "1px solid #d0d5dd",
        borderRadius: "10px",
        padding: "12px 13px",
        resize: "vertical",
        fontFamily: "inherit",
        fontSize: "14px",
    },

    help: {
        color: "#667085",
        fontWeight: 400,
        lineHeight: 1.4,
    },

    twoColumns: {
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "12px",
    },

    broadcastGrid: {
        display: "grid",
        gridTemplateColumns:
            "minmax(250px, 1fr) auto",
        gap: "20px",
        alignItems: "end",
    },

    actions: {
        display: "flex",
        gap: "10px",
        flexWrap: "wrap",
    },

    primaryButton: {
        border: 0,
        borderRadius: "10px",
        background: "#102b4c",
        color: "white",
        padding: "12px 17px",
        cursor: "pointer",
        fontWeight: 800,
    },

    warningButton: {
        border: 0,
        borderRadius: "10px",
        background: "#d97706",
        color: "white",
        padding: "12px 17px",
        cursor: "pointer",
        fontWeight: 800,
    },

    dangerButton: {
        border: 0,
        borderRadius: "10px",
        background: "#b42318",
        color: "white",
        padding: "12px 17px",
        cursor: "pointer",
        fontWeight: 800,
    },

    checkbox: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        fontWeight: 700,
        fontSize: "14px",
    },

    liveBadge: {
        background: "#d92d20",
        color: "white",
        borderRadius: "999px",
        padding: "8px 13px",
        fontSize: "11px",
        fontWeight: 900,
    },

    error: {
        maxWidth: "1450px",
        margin: "20px auto 0",
        padding: "16px 28px",
        background: "#fff1f3",
        border: "1px solid #fecdca",
        borderRadius: "12px",
        color: "#b42318",
    },

    success: {
        maxWidth: "1450px",
        margin: "20px auto 0",
        padding: "16px 28px",
        background: "#ecfdf3",
        border: "1px solid #abefc6",
        borderRadius: "12px",
        color: "#067647",
    },

    empty: {
        padding: "30px",
        textAlign: "center",
        color: "#667085",
        background: "#f8fafc",
        borderRadius: "12px",
    },

    loading: {
        minHeight: "70vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        background: "#f4f7fb",
        color: "#172033",
        textAlign: "center",
    },

    loadingIcon: {
        fontSize: "60px",
        marginBottom: "15px",
    },
};
