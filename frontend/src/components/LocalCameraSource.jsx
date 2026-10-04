import React, { useEffect, useRef, useState } from "react";

export default function LocalCameraSource({
    sourceName = "CAM PC",
    onStreamReady,
    compact = false,
}) {
    const videoRef = useRef(null);
    const streamRef = useRef(null);

    const [running, setRunning] = useState(false);
    const [muted, setMuted] = useState(false);
    const [error, setError] = useState("");

    async function start() {
        setError("");

        try {
            if (!navigator.mediaDevices?.getUserMedia) {
                setError(
                    "La caméra navigateur n'est pas disponible."
                );
                return;
            }

            stop();

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 1920 },
                        height: { ideal: 1080 },
                        frameRate: { ideal: 30 },
                    },
                    audio: true,
                });

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            setRunning(true);

            if (onStreamReady) {
                onStreamReady(stream);
            }
        } catch (e) {
            console.error(e);

            if (e?.name === "NotAllowedError") {
                setError(
                    "Autorisation caméra/microphone refusée."
                );
            } else if (e?.name === "NotFoundError") {
                setError(
                    "Aucune caméra compatible n'a été trouvée."
                );
            } else {
                setError(
                    "Impossible de démarrer la caméra."
                );
            }
        }
    }

    function stop() {
        if (streamRef.current) {
            streamRef.current
                .getTracks()
                .forEach((track) => track.stop());
        }

        streamRef.current = null;

        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }

        setRunning(false);

        if (onStreamReady) {
            onStreamReady(null);
        }
    }

    function toggleMute() {
        if (!streamRef.current) return;

        const nextMuted = !muted;

        streamRef.current
            .getAudioTracks()
            .forEach((track) => {
                track.enabled = !nextMuted;
            });

        setMuted(nextMuted);
    }

    useEffect(() => {
        return () => stop();
    }, []);

    return (
        <div
            style={{
                border: "1px solid #2a4058",
                borderRadius: 8,
                overflow: "hidden",
                background: "#02070d",
            }}
        >
            <div
                style={{
                    position: "relative",
                    aspectRatio: "16 / 9",
                    minHeight: compact ? 100 : 180,
                    background: "#02070d",
                }}
            >
                <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        display: running
                            ? "block"
                            : "none",
                    }}
                />

                {!running && (
                    <div
                        style={{
                            position: "absolute",
                            inset: 0,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            flexDirection: "column",
                            color: "#8194a8",
                            gap: 5,
                        }}
                    >
                        <div style={{ fontSize: 30 }}>
                            📷
                        </div>

                        <strong
                            style={{
                                color: "#eef5ff",
                                fontSize: 12,
                            }}
                        >
                            {sourceName}
                        </strong>

                        <span
                            style={{
                                fontSize: 10,
                            }}
                        >
                            SOURCE OFF
                        </span>
                    </div>
                )}

                {running && (
                    <div
                        style={{
                            position: "absolute",
                            top: 6,
                            left: 6,
                            padding: "4px 7px",
                            borderRadius: 4,
                            background:
                                "rgba(20,150,80,.9)",
                            color: "#fff",
                            fontSize: 9,
                            fontWeight: 900,
                        }}
                    >
                        ● LIVE — {sourceName}
                    </div>
                )}
            </div>

            <div
                style={{
                    padding: 7,
                    display: "flex",
                    gap: 5,
                    flexWrap: "wrap",
                    background: "#0b1725",
                }}
            >
                {!running ? (
                    <button
                        type="button"
                        onClick={start}
                        style={{
                            border: "1px solid #2eaa67",
                            background:
                                "rgba(46,170,103,.15)",
                            color: "#eef5ff",
                            borderRadius: 5,
                            padding: "6px 9px",
                            fontSize: 10,
                            fontWeight: 800,
                            cursor: "pointer",
                        }}
                    >
                        ▶ CONNECTER
                    </button>
                ) : (
                    <button
                        type="button"
                        onClick={stop}
                        style={{
                            border: "1px solid #d65050",
                            background:
                                "rgba(214,80,80,.15)",
                            color: "#eef5ff",
                            borderRadius: 5,
                            padding: "6px 9px",
                            fontSize: 10,
                            fontWeight: 800,
                            cursor: "pointer",
                        }}
                    >
                        ■ DÉCONNECTER
                    </button>
                )}

                <button
                    type="button"
                    disabled={!running}
                    onClick={toggleMute}
                    style={{
                        border: "1px solid #2a4058",
                        background: "#101f31",
                        color: "#eef5ff",
                        borderRadius: 5,
                        padding: "6px 9px",
                        fontSize: 10,
                        cursor: running
                            ? "pointer"
                            : "not-allowed",
                    }}
                >
                    {muted
                        ? "🔇 AUDIO OFF"
                        : "🎙 AUDIO ON"}
                </button>
            </div>

            {error && (
                <div
                    style={{
                        padding: 7,
                        color: "#ff9b9b",
                        fontSize: 10,
                        background:
                            "rgba(180,40,40,.12)",
                    }}
                >
                    {error}
                </div>
            )}
        </div>
    );
}
