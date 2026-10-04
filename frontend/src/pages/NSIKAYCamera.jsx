import React, { useEffect, useRef, useState } from "react";

export default function NSIKAYCamera() {
    const videoRef = useRef(null);
    const streamRef = useRef(null);

    const [devices, setDevices] = useState([]);
    const [cameraId, setCameraId] = useState("");
    const [microphoneId, setMicrophoneId] = useState("");
    const [running, setRunning] = useState(false);
    const [muted, setMuted] = useState(false);
    const [message, setMessage] = useState(
        "Autorisez la caméra et le microphone pour commencer."
    );

    async function loadDevices() {
        try {
            const list = await navigator.mediaDevices.enumerateDevices();

            const cameras = list.filter(
                (device) => device.kind === "videoinput"
            );

            const microphones = list.filter(
                (device) => device.kind === "audioinput"
            );

            setDevices(list);

            if (!cameraId && cameras.length) {
                setCameraId(cameras[0].deviceId);
            }

            if (!microphoneId && microphones.length) {
                setMicrophoneId(microphones[0].deviceId);
            }
        } catch (error) {
            console.error(error);
            setMessage(
                "Impossible d'accéder aux périphériques multimédia."
            );
        }
    }

    useEffect(() => {
        loadDevices();

        return () => {
            if (streamRef.current) {
                streamRef.current.getTracks().forEach((track) => {
                    track.stop();
                });
            }
        };
    }, []);

    async function startCamera() {
        try {
            if (!navigator.mediaDevices?.getUserMedia) {
                setMessage(
                    "La caméra navigateur n'est pas disponible dans ce contexte."
                );
                return;
            }

            if (streamRef.current) {
                streamRef.current.getTracks().forEach((track) => {
                    track.stop();
                });
            }

            const constraints = {
                video: cameraId
                    ? {
                          deviceId: {
                              exact: cameraId,
                          },
                          width: {
                              ideal: 1920,
                          },
                          height: {
                              ideal: 1080,
                          },
                          frameRate: {
                              ideal: 30,
                          },
                      }
                    : {
                          width: {
                              ideal: 1920,
                          },
                          height: {
                              ideal: 1080,
                          },
                          frameRate: {
                              ideal: 30,
                          },
                      },
                audio: microphoneId
                    ? {
                          deviceId: {
                              exact: microphoneId,
                          },
                      }
                    : true,
            };

            const stream =
                await navigator.mediaDevices.getUserMedia(
                    constraints
                );

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            setRunning(true);
            setMessage(
                "Caméra connectée localement. Source prête pour la Régie."
            );

            await loadDevices();
        } catch (error) {
            console.error(error);

            setRunning(false);

            if (error.name === "NotAllowedError") {
                setMessage(
                    "Autorisation caméra/microphone refusée."
                );
            } else if (error.name === "NotFoundError") {
                setMessage(
                    "Aucune caméra ou aucun microphone compatible trouvé."
                );
            } else {
                setMessage(
                    "Impossible de démarrer la caméra."
                );
            }
        }
    }

    function stopCamera() {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => {
                track.stop();
            });
        }

        streamRef.current = null;

        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }

        setRunning(false);
        setMessage("Caméra arrêtée.");
    }

    function toggleMute() {
        const stream = streamRef.current;

        if (!stream) return;

        stream.getAudioTracks().forEach((track) => {
            track.enabled = muted;
        });

        setMuted(!muted);
    }

    const cameras = devices.filter(
        (device) => device.kind === "videoinput"
    );

    const microphones = devices.filter(
        (device) => device.kind === "audioinput"
    );

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#07111f",
                color: "#eef5ff",
                padding: 20,
                fontFamily:
                    "Inter, system-ui, sans-serif",
            }}
        >
            <div
                style={{
                    maxWidth: 1200,
                    margin: "0 auto",
                }}
            >
                <div style={{ marginBottom: 15 }}>
                    <h1
                        style={{
                            margin: 0,
                            fontSize: 26,
                        }}
                    >
                        NSIKAY CAMERA
                    </h1>

                    <div
                        style={{
                            color: "#91a4b8",
                            fontSize: 13,
                            marginTop: 5,
                        }}
                    >
                        Caméra locale • Webcam PC •
                        Microphone
                    </div>
                </div>

                <div
                    style={{
                        background: "#0d1b2a",
                        border: "1px solid #23364b",
                        borderRadius: 10,
                        padding: 14,
                        marginBottom: 12,
                    }}
                >
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fit,minmax(220px,1fr))",
                            gap: 10,
                        }}
                    >
                        <div>
                            <label
                                style={{
                                    display: "block",
                                    color: "#91a4b8",
                                    fontSize: 11,
                                    marginBottom: 5,
                                }}
                            >
                                CAMÉRA
                            </label>

                            <select
                                value={cameraId}
                                onChange={(e) =>
                                    setCameraId(
                                        e.target.value
                                    )
                                }
                                style={{
                                    width: "100%",
                                    padding: 10,
                                }}
                            >
                                {cameras.length === 0 && (
                                    <option value="">
                                        Aucune caméra
                                    </option>
                                )}

                                {cameras.map((device) => (
                                    <option
                                        key={device.deviceId}
                                        value={
                                            device.deviceId
                                        }
                                    >
                                        {device.label ||
                                            `Caméra ${device.deviceId.slice(
                                                0,
                                                6
                                            )}`}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label
                                style={{
                                    display: "block",
                                    color: "#91a4b8",
                                    fontSize: 11,
                                    marginBottom: 5,
                                }}
                            >
                                MICROPHONE
                            </label>

                            <select
                                value={microphoneId}
                                onChange={(e) =>
                                    setMicrophoneId(
                                        e.target.value
                                    )
                                }
                                style={{
                                    width: "100%",
                                    padding: 10,
                                }}
                            >
                                {microphones.length === 0 && (
                                    <option value="">
                                        Aucun microphone
                                    </option>
                                )}

                                {microphones.map(
                                    (device) => (
                                        <option
                                            key={
                                                device.deviceId
                                            }
                                            value={
                                                device.deviceId
                                            }
                                        >
                                            {device.label ||
                                                `Microphone ${device.deviceId.slice(
                                                    0,
                                                    6
                                                )}`}
                                        </option>
                                    )
                                )}
                            </select>
                        </div>
                    </div>

                    <div
                        style={{
                            display: "flex",
                            gap: 8,
                            flexWrap: "wrap",
                            marginTop: 12,
                        }}
                    >
                        {!running ? (
                            <button
                                type="button"
                                onClick={startCamera}
                                style={{
                                    padding:
                                        "10px 16px",
                                    borderRadius: 7,
                                    border:
                                        "1px solid #27ae60",
                                    background:
                                        "rgba(39,174,96,.18)",
                                    color: "#eef5ff",
                                    fontWeight: 800,
                                    cursor: "pointer",
                                }}
                            >
                                📷 DÉMARRER CAMÉRA
                            </button>
                        ) : (
                            <button
                                type="button"
                                onClick={stopCamera}
                                style={{
                                    padding:
                                        "10px 16px",
                                    borderRadius: 7,
                                    border:
                                        "1px solid #d64545",
                                    background:
                                        "rgba(214,69,69,.18)",
                                    color: "#eef5ff",
                                    fontWeight: 800,
                                    cursor: "pointer",
                                }}
                            >
                                ■ ARRÊTER
                            </button>
                        )}

                        <button
                            type="button"
                            onClick={toggleMute}
                            disabled={!running}
                            style={{
                                padding:
                                    "10px 16px",
                                borderRadius: 7,
                                border:
                                    "1px solid #23364b",
                                background: "#101f31",
                                color: "#eef5ff",
                                fontWeight: 700,
                                cursor: running
                                    ? "pointer"
                                    : "not-allowed",
                            }}
                        >
                            {muted
                                ? "🔇 MICRO COUPÉ"
                                : "🎙 MICRO ACTIF"}
                        </button>

                        <button
                            type="button"
                            onClick={loadDevices}
                            style={{
                                padding:
                                    "10px 16px",
                                borderRadius: 7,
                                border:
                                    "1px solid #23364b",
                                background: "#101f31",
                                color: "#eef5ff",
                                fontWeight: 700,
                                cursor: "pointer",
                            }}
                        >
                            ↻ ACTUALISER SOURCES
                        </button>
                    </div>
                </div>

                <div
                    style={{
                        background: "#02070d",
                        border: "1px solid #23364b",
                        borderRadius: 10,
                        overflow: "hidden",
                    }}
                >
                    <div
                        style={{
                            position: "relative",
                            aspectRatio: "16 / 9",
                            maxHeight: "70vh",
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
                                objectFit: "contain",
                                background: "#02070d",
                            }}
                        />

                        {!running && (
                            <div
                                style={{
                                    position: "absolute",
                                    inset: 0,
                                    display: "flex",
                                    alignItems:
                                        "center",
                                    justifyContent:
                                        "center",
                                    flexDirection:
                                        "column",
                                    color: "#91a4b8",
                                }}
                            >
                                <div
                                    style={{
                                        fontSize: 50,
                                        marginBottom: 10,
                                    }}
                                >
                                    📷
                                </div>

                                <strong
                                    style={{
                                        color: "#eef5ff",
                                    }}
                                >
                                    SOURCE CAMÉRA
                                </strong>

                                <span
                                    style={{
                                        fontSize: 12,
                                        marginTop: 5,
                                    }}
                                >
                                    Démarrez la caméra
                                    pour afficher le
                                    retour vidéo.
                                </span>
                            </div>
                        )}

                        <div
                            style={{
                                position: "absolute",
                                top: 10,
                                left: 10,
                                padding:
                                    "5px 8px",
                                borderRadius: 5,
                                background:
                                    running
                                        ? "rgba(39,174,96,.85)"
                                        : "rgba(0,0,0,.65)",
                                color: "#fff",
                                fontSize: 11,
                                fontWeight: 900,
                            }}
                        >
                            {running
                                ? "● CAMERA CONNECTÉE"
                                : "○ CAMERA OFF"}
                        </div>
                    </div>
                </div>

                <div
                    style={{
                        marginTop: 10,
                        padding: 10,
                        background: "#0d1b2a",
                        border:
                            "1px solid #23364b",
                        borderRadius: 7,
                        color: "#91a4b8",
                        fontSize: 11,
                    }}
                >
                    {message}
                </div>
            </div>
        </div>
    );
}
