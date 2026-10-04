import React, { useEffect, useMemo, useState } from "react";

import {
    createMediaAsset,
    deleteMediaAsset,
    getMediaAssets,
    getMediaDestinations,
    setMediaDestinations,
} from "../services/mediaLibrary";

const TYPE_LABELS = {
    VIDEO: "Vidéo",
    FILM: "Film",
    AUDIO: "Audio",
    IMAGE: "Image",
    PROGRAM: "Programme TV",
    MUSIC: "Musique",
    JINGLE: "Jingle",
    ADVERTISING: "Publicité",
    REPORTAGE: "Reportage",
    INTERVIEW: "Interview",
    ARCHIVE: "Archive",
    DOCUMENT: "Document",
};

const STATUS_LABELS = {
    DRAFT: "Brouillon",
    READY: "Prêt",
    PUBLISHED: "Publié",
    ARCHIVED: "Archivé",
};

export default function MediaLibrary() {
    const [assets, setAssets] = useState([]);
    const [destinations, setDestinations] = useState([]);

    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");

    const [search, setSearch] = useState("");
    const [typeFilter, setTypeFilter] = useState("ALL");

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [assetType, setAssetType] = useState("VIDEO");
    const [file, setFile] = useState(null);

    const [selectedDestinations, setSelectedDestinations] = useState([]);

    async function loadData() {
        setLoading(true);

        try {
            const [assetsResponse, destinationsResponse] =
                await Promise.all([
                    getMediaAssets(),
                    getMediaDestinations(),
                ]);

            const assetsData = assetsResponse?.data;
            const destinationsData = destinationsResponse?.data;

            setAssets(
                Array.isArray(assetsData)
                    ? assetsData
                    : assetsData?.results || []
            );

            setDestinations(
                Array.isArray(destinationsData)
                    ? destinationsData
                    : destinationsData?.results || []
            );
        } catch (error) {
            console.error(error);
            setMessage(
                "Impossible de charger la bibliothèque média."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadData();
    }, []);

    function toggleDestination(id) {
        setSelectedDestinations((current) =>
            current.includes(id)
                ? current.filter((value) => value !== id)
                : [...current, id]
        );
    }

    function toggleDestinationGroup(ids) {
        const allSelected = ids.every((id) =>
            selectedDestinations.includes(id)
        );

        setSelectedDestinations((current) => {
            if (allSelected) {
                return current.filter(
                    (id) => !ids.includes(id)
                );
            }

            return [
                ...new Set([
                    ...current,
                    ...ids,
                ]),
            ];
        });
    }

    async function handleUpload(event) {
        event.preventDefault();

        if (!title.trim()) {
            setMessage("Le titre du média est obligatoire.");
            return;
        }

        if (!file) {
            setMessage("Sélectionne un fichier média.");
            return;
        }

        setUploading(true);
        setMessage("");

        try {
            const formData = new FormData();

            formData.append("title", title);
            formData.append("description", description);
            formData.append("asset_type", assetType);
            formData.append("file", file);
            formData.append("status", "DRAFT");

            const response = await createMediaAsset(formData);
            const created = response?.data;

            if (created?.id && selectedDestinations.length) {
                await setMediaDestinations(
                    created.id,
                    selectedDestinations
                );
            }

            setTitle("");
            setDescription("");
            setAssetType("VIDEO");
            setFile(null);
            setSelectedDestinations([]);

            const fileInput =
                document.getElementById(
                    "media-library-file"
                );

            if (fileInput) {
                fileInput.value = "";
            }

            setMessage(
                "Média ajouté à la bibliothèque."
            );

            await loadData();
        } catch (error) {
            console.error(error);

            const detail =
                error?.response?.data?.detail ||
                "Erreur lors de l'ajout du média.";

            setMessage(detail);
        } finally {
            setUploading(false);
        }
    }

    async function handleDelete(id) {
        const confirmed = window.confirm(
            "Supprimer ce média de la bibliothèque ?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteMediaAsset(id);

            setAssets((current) =>
                current.filter(
                    (asset) => asset.id !== id
                )
            );

            setMessage("Média supprimé.");
        } catch (error) {
            console.error(error);
            setMessage(
                "Impossible de supprimer ce média."
            );
        }
    }

    const filteredAssets = useMemo(() => {
        const query = search.trim().toLowerCase();

        return assets.filter((asset) => {
            const matchesType =
                typeFilter === "ALL" ||
                asset.asset_type === typeFilter;

            const matchesSearch =
                !query ||
                asset.title
                    ?.toLowerCase()
                    .includes(query) ||
                asset.description
                    ?.toLowerCase()
                    .includes(query) ||
                asset.original_filename
                    ?.toLowerCase()
                    .includes(query);

            return matchesType && matchesSearch;
        });
    }, [assets, search, typeFilter]);

    const internalDestinations =
        destinations.filter(
            (destination) =>
                destination.destination_type ===
                "INTERNAL"
        );

    const externalDestinations =
        destinations.filter(
            (destination) =>
                destination.destination_type ===
                "EXTERNAL"
        );

    const internalIds =
        internalDestinations.map(
            (destination) => destination.id
        );

    const externalIds =
        externalDestinations.map(
            (destination) => destination.id
        );

    return (
        <div
            style={{
                padding: "24px",
                maxWidth: "1500px",
                margin: "0 auto",
            }}
        >
            <div
                style={{
                    marginBottom: "24px",
                }}
            >
                <h1
                    style={{
                        margin: 0,
                        fontSize: "32px",
                    }}
                >
                    Bibliothèque Média NSIKAY
                </h1>

                <p
                    style={{
                        marginTop: "8px",
                        opacity: 0.75,
                    }}
                >
                    Stockage central des vidéos, films,
                    audios, programmes, reportages,
                    interviews, publicités et archives.
                </p>
            </div>

            {message && (
                <div
                    style={{
                        padding: "12px 16px",
                        marginBottom: "18px",
                        borderRadius: "8px",
                        background: "#f1f5f9",
                    }}
                >
                    {message}
                </div>
            )}

            <section
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "minmax(320px, 0.9fr) minmax(500px, 1.6fr)",
                    gap: "24px",
                    alignItems: "start",
                }}
            >
                <form
                    onSubmit={handleUpload}
                    style={{
                        border: "1px solid #ddd",
                        borderRadius: "12px",
                        padding: "20px",
                    }}
                >
                    <h2>Ajouter un média</h2>

                    <label>
                        Titre
                        <input
                            value={title}
                            onChange={(event) =>
                                setTitle(
                                    event.target.value
                                )
                            }
                            placeholder="Ex. PIB - Film économique"
                            style={{
                                width: "100%",
                                marginTop: "6px",
                                marginBottom: "14px",
                                padding: "10px",
                                boxSizing: "border-box",
                            }}
                        />
                    </label>

                    <label>
                        Type
                        <select
                            value={assetType}
                            onChange={(event) =>
                                setAssetType(
                                    event.target.value
                                )
                            }
                            style={{
                                width: "100%",
                                marginTop: "6px",
                                marginBottom: "14px",
                                padding: "10px",
                            }}
                        >
                            {Object.entries(
                                TYPE_LABELS
                            ).map(([value, label]) => (
                                <option
                                    key={value}
                                    value={value}
                                >
                                    {label}
                                </option>
                            ))}
                        </select>
                    </label>

                    <label>
                        Description
                        <textarea
                            value={description}
                            onChange={(event) =>
                                setDescription(
                                    event.target.value
                                )
                            }
                            rows={4}
                            placeholder="Description du contenu..."
                            style={{
                                width: "100%",
                                marginTop: "6px",
                                marginBottom: "14px",
                                padding: "10px",
                                boxSizing: "border-box",
                            }}
                        />
                    </label>

                    <label>
                        Fichier
                        <input
                            id="media-library-file"
                            type="file"
                            onChange={(event) =>
                                setFile(
                                    event.target.files?.[0] ||
                                    null
                                )
                            }
                            style={{
                                width: "100%",
                                marginTop: "6px",
                                marginBottom: "18px",
                            }}
                        />
                    </label>

                    <h3>
                        Destinations de diffusion
                    </h3>

                    <div
                        style={{
                            display: "flex",
                            gap: "8px",
                            flexWrap: "wrap",
                            marginBottom: "12px",
                        }}
                    >
                        <button
                            type="button"
                            onClick={() =>
                                toggleDestinationGroup(
                                    internalIds
                                )
                            }
                        >
                            NSIKAY : toutes
                        </button>

                        <button
                            type="button"
                            onClick={() =>
                                toggleDestinationGroup(
                                    externalIds
                                )
                            }
                        >
                            Réseaux : tous
                        </button>
                    </div>

                    <div
                        style={{
                            maxHeight: "300px",
                            overflowY: "auto",
                            border: "1px solid #eee",
                            borderRadius: "8px",
                            padding: "10px",
                        }}
                    >
                        {destinations.map(
                            (destination) => (
                                <label
                                    key={destination.id}
                                    style={{
                                        display: "flex",
                                        alignItems:
                                            "center",
                                        gap: "8px",
                                        padding:
                                            "6px 2px",
                                    }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={selectedDestinations.includes(
                                            destination.id
                                        )}
                                        onChange={() =>
                                            toggleDestination(
                                                destination.id
                                            )
                                        }
                                    />

                                    <span>
                                        {
                                            destination.name
                                        }
                                    </span>
                                </label>
                            )
                        )}
                    </div>

                    <p
                        style={{
                            fontSize: "13px",
                            opacity: 0.7,
                        }}
                    >
                        {selectedDestinations.length}{" "}
                        destination(s) sélectionnée(s).
                    </p>

                    <button
                        type="submit"
                        disabled={uploading}
                        style={{
                            width: "100%",
                            padding: "12px",
                            marginTop: "10px",
                            cursor: uploading
                                ? "wait"
                                : "pointer",
                        }}
                    >
                        {uploading
                            ? "Enregistrement..."
                            : "Ajouter à la bibliothèque"}
                    </button>
                </form>

                <section>
                    <div
                        style={{
                            display: "flex",
                            gap: "10px",
                            marginBottom: "18px",
                            flexWrap: "wrap",
                        }}
                    >
                        <input
                            value={search}
                            onChange={(event) =>
                                setSearch(
                                    event.target.value
                                )
                            }
                            placeholder="Rechercher un média..."
                            style={{
                                flex: 1,
                                minWidth: "240px",
                                padding: "10px",
                            }}
                        />

                        <select
                            value={typeFilter}
                            onChange={(event) =>
                                setTypeFilter(
                                    event.target.value
                                )
                            }
                            style={{
                                padding: "10px",
                            }}
                        >
                            <option value="ALL">
                                Tous les types
                            </option>

                            {Object.entries(
                                TYPE_LABELS
                            ).map(([value, label]) => (
                                <option
                                    key={value}
                                    value={value}
                                >
                                    {label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {loading ? (
                        <p>
                            Chargement de la bibliothèque...
                        </p>
                    ) : filteredAssets.length === 0 ? (
                        <div
                            style={{
                                border:
                                    "1px dashed #bbb",
                                borderRadius: "12px",
                                padding: "40px",
                                textAlign: "center",
                            }}
                        >
                            Aucun média dans la
                            bibliothèque.
                        </div>
                    ) : (
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns:
                                    "repeat(auto-fill, minmax(280px, 1fr))",
                                gap: "16px",
                            }}
                        >
                            {filteredAssets.map(
                                (asset) => (
                                    <article className="nsikay-media-library-page"
                                        key={asset.id}
                                        style={{
                                            border:
                                                "1px solid #ddd",
                                            borderRadius:
                                                "12px",
                                            overflow:
                                                "hidden",
                                        }}
                                    >
                                        {asset.thumbnail_url ? (
                                            <img
                                                src={
                                                    asset.thumbnail_url
                                                }
                                                alt={
                                                    asset.title
                                                }
                                                style={{
                                                    width: "100%",
                                                    height:
                                                        "160px",
                                                    objectFit:
                                                        "cover",
                                                }}
                                            />
                                        ) : (
                                            <div
                                                style={{
                                                    height:
                                                        "160px",
                                                    display:
                                                        "flex",
                                                    alignItems:
                                                        "center",
                                                    justifyContent:
                                                        "center",
                                                    background:
                                                        "#f1f5f9",
                                                    fontSize:
                                                        "42px",
                                                }}
                                            >
                                                {asset.asset_type ===
                                                "AUDIO"
                                                    ? "🎙️"
                                                    : asset.asset_type ===
                                                      "IMAGE"
                                                    ? "🖼️"
                                                    : "🎬"}
                                            </div>
                                        )}

                                        <div
                                            style={{
                                                padding:
                                                    "14px",
                                            }}
                                        >
                                            <h3
                                                style={{
                                                    marginTop: 0,
                                                }}
                                            >
                                                {
                                                    asset.title
                                                }
                                            </h3>

                                            <div
                                                style={{
                                                    fontSize:
                                                        "13px",
                                                    opacity:
                                                        0.7,
                                                    marginBottom:
                                                        "8px",
                                                }}
                                            >
                                                {
                                                    TYPE_LABELS[
                                                        asset
                                                            .asset_type
                                                    ]
                                                }{" "}
                                                •{" "}
                                                {
                                                    STATUS_LABELS[
                                                        asset
                                                            .status
                                                    ]
                                                }
                                            </div>

                                            <p
                                                style={{
                                                    fontSize:
                                                        "14px",
                                                }}
                                            >
                                                {
                                                    asset.description
                                                }
                                            </p>

                                            {asset.file_url && (
                                                <a
                                                    href={
                                                        asset.file_url
                                                    }
                                                    target="_blank"
                                                    rel="noreferrer"
                                                >
                                                    Ouvrir le fichier
                                                </a>
                                            )}

                                            <div
                                                style={{
                                                    marginTop:
                                                        "12px",
                                                }}
                                            >
                                                <strong>
                                                    Destinations
                                                </strong>

                                                <div
                                                    style={{
                                                        display:
                                                            "flex",
                                                        flexWrap:
                                                            "wrap",
                                                        gap: "5px",
                                                        marginTop:
                                                            "6px",
                                                    }}
                                                >
                                                    {(
                                                        asset.distributions ||
                                                        []
                                                    ).map(
                                                        (
                                                            distribution
                                                        ) => (
                                                            <span
                                                                key={
                                                                    distribution.id
                                                                }
                                                                style={{
                                                                    fontSize:
                                                                        "11px",
                                                                    border:
                                                                        "1px solid #ccc",
                                                                    borderRadius:
                                                                        "999px",
                                                                    padding:
                                                                        "4px 7px",
                                                                }}
                                                            >
                                                                {
                                                                    distribution.destination_name
                                                                }
                                                            </span>
                                                        )
                                                    )}
                                                </div>
                                            </div>

                                            <button
                                                type="button"
                                                onClick={() =>
                                                    handleDelete(
                                                        asset.id
                                                    )
                                                }
                                                style={{
                                                    marginTop:
                                                        "14px",
                                                }}
                                            >
                                                Supprimer
                                            </button>
                                        </div>
                                    </article>
                                )
                            )}
                        </div>
                    )}
                </section>
            </section>
        </div>
    );
}