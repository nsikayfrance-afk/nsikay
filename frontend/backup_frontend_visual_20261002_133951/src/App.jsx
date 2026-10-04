import { useMemo, useState } from "react";
import {
    getWenzeProducts,
    getTVChannels,
    registerNsikayUser,
    loginNsikayUser,
} from "./services/nsikay";

const initialRegister = {
    firstName: "",
    lastName: "",
    username: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    country: "",
    city: "",
    accept: false,
};

function PhotoCard({
    title,
    description,
    icon,
    file,
    onChange,
    required = true,
}) {
    const preview = useMemo(() => {
        if (!file) return null;
        return URL.createObjectURL(file);
    }, [file]);

    return (
        <div className={`photo-card ${file ? "has-file" : ""}`}>
            <div className="photo-icon">{icon}</div>

            <div className="photo-title">
                {title}
                {required && <span className="required">*</span>}
            </div>

            <p>{description}</p>

            {preview ? (
                <div className="photo-preview">
                    <img src={preview} alt={title} />
                    <label className="replace-photo">
                        Modifier
                        <input
                            type="file"
                            accept="image/*"
                            onChange={onChange}
                        />
                    </label>
                </div>
            ) : (
                <label className="upload-button">
                    Ajouter une photo
                    <input
                        type="file"
                        accept="image/*"
                        onChange={onChange}
                    />
                </label>
            )}
        </div>
    );
}

function App() {
    const [page, setPage] = useState("home");
    const [loginMode, setLoginMode] = useState("login");

    const [register, setRegister] = useState(initialRegister);

    const [photos, setPhotos] = useState({
        personal: null,
        identity: null,
        identityHolder: null,
    });

    const [login, setLogin] = useState({
        identifier: "",
        password: "",
    });

    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const updateRegister = (field, value) => {
        setRegister((current) => ({
            ...current,
            [field]: value,
        }));
    };

    const updatePhoto = (field, file) => {
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            setMessage("Veuillez sélectionner une image.");
            return;
        }

        if (file.size > 8 * 1024 * 1024) {
            setMessage("La photo ne doit pas dépasser 8 Mo.");
            return;
        }

        setPhotos((current) => ({
            ...current,
            [field]: file,
        }));

        setMessage("");
    };

    const openRegister = () => {
        setLoginMode("register");
        setPage("auth");
        setMessage("");
    };

    const openLogin = () => {
        setLoginMode("login");
        setPage("auth");
        setMessage("");
    };

    const submitRegister = async (event) => {
        event.preventDefault();
        setMessage("");

        if (
            !register.firstName ||
            !register.lastName ||
            !register.email ||
            !register.password
        ) {
            setMessage("Veuillez compléter les champs obligatoires.");
            return;
        }

        if (register.password !== register.confirmPassword) {
            setMessage("Les mots de passe ne correspondent pas.");
            return;
        }

        if (!photos.personal || !photos.identity || !photos.identityHolder) {
            setMessage(
                "Les trois photos d'identification sont obligatoires."
            );
            return;
        }

        if (!register.accept) {
            setMessage("Vous devez accepter les conditions d'utilisation.");
            return;
        }

        const formData = new FormData();

        formData.append("first_name", register.firstName);
        formData.append("last_name", register.lastName);
        formData.append("username", register.username);
        formData.append("email", register.email);
        formData.append("phone", register.phone);
        formData.append("password", register.password);
        formData.append("country", register.country);
        formData.append("city", register.city);

        formData.append("personal_photo", photos.personal);
        formData.append("identity_document", photos.identity);
        formData.append("identity_holder_photo", photos.identityHolder);

        setLoading(true);

        try {
            await registerNsikayUser(formData);

            setMessage(
                "Inscription envoyée. Votre dossier est maintenant transmis pour vérification."
            );
        } catch (error) {
            /*
             * Le formulaire est déjà prêt.
             * Si le endpoint Django n'est pas encore branché exactement
             * sous cette URL, on affiche une information claire sans
             * perdre les données saisies.
             */
            const detail =
                error?.response?.data?.detail ||
                error?.response?.data?.message ||
                "Le serveur d'inscription doit encore être raccordé à cette interface.";

            setMessage(detail);
        } finally {
            setLoading(false);
        }
    };

    const submitLogin = async (event) => {
        event.preventDefault();
        setMessage("");

        if (!login.identifier || !login.password) {
            setMessage("Veuillez saisir votre identifiant et votre mot de passe.");
            return;
        }

        setLoading(true);

        try {
            await loginNsikayUser(login);
            setPage("dashboard");
            setMessage("");
        } catch (error) {
            const detail =
                error?.response?.data?.detail ||
                error?.response?.data?.message ||
                "La connexion Django doit encore être raccordée à cette interface.";

            setMessage(detail);
        } finally {
            setLoading(false);
        }
    };

    if (page === "dashboard") {
        return (
            <div className="app-shell">
                <header className="topbar">
                    <button
                        className="brand"
                        onClick={() => setPage("home")}
                    >
                        <span className="brand-mark">N</span>
                        <span>
                            <strong>NSIKAY</strong>
                            <small>Nantes • Monde</small>
                        </span>
                    </button>

                    <button
                        className="outline-button"
                        onClick={() => {
                            setPage("home");
                            setLoginMode("login");
                        }}
                    >
                        Déconnexion
                    </button>
                </header>

                <main className="dashboard">
                    <section className="dashboard-hero">
                        <div>
                            <span className="eyebrow">ESPACE NSIKAY</span>
                            <h1>Bienvenue dans votre espace.</h1>
                            <p>
                                Un seul compte pour accéder à vos espaces
                                personnels, professionnels et d'engagement.
                            </p>
                        </div>
                    </section>

                    <section className="module-grid">
                        <button
                            className="module-card"
                            onClick={async () => {
                                try {
                                    await getWenzeProducts();
                                    setMessage("WENZE est accessible.");
                                } catch {
                                    setMessage(
                                        "Le module WENZE est disponible côté interface, mais le serveur doit être actif."
                                    );
                                }
                            }}
                        >
                            <span>🛍️</span>
                            <strong>WENZE</strong>
                            <small>Commerce NSIKAY</small>
                        </button>

                        <button
                            className="module-card"
                            onClick={async () => {
                                try {
                                    await getTVChannels();
                                    setMessage("NSIKAY TV est accessible.");
                                } catch {
                                    setMessage(
                                        "Le module TV est disponible côté interface."
                                    );
                                }
                            }}
                        >
                            <span>📺</span>
                            <strong>NSIKAY TV</strong>
                            <small>Chaînes et contenus</small>
                        </button>

                        <button
                            className="module-card"
                            onClick={() => setMessage("Espace Finance")}
                        >
                            <span>💳</span>
                            <strong>Finance</strong>
                            <small>Portefeuille et opérations</small>
                        </button>

                        <button
                            className="module-card"
                            onClick={() => setMessage("Espace Événements")}
                        >
                            <span>🎟️</span>
                            <strong>Événements</strong>
                            <small>Participer et organiser</small>
                        </button>

                        <button
                            className="module-card"
                            onClick={() => setMessage("Espace Certification")}
                        >
                            <span>✓</span>
                            <strong>Certification</strong>
                            <small>Identité et services</small>
                        </button>

                        <button
                            className="module-card"
                            onClick={() => setMessage("Espace Engagement")}
                        >
                            <span>🌍</span>
                            <strong>Engagement</strong>
                            <small>Actions et missions</small>
                        </button>
                    </section>

                    {message && (
                        <div className="status-message success">
                            {message}
                        </div>
                    )}
                </main>
            </div>
        );
    }

    if (page === "auth") {
        return (
            <div className="app-shell">
                <header className="topbar">
                    <button
                        className="brand"
                        onClick={() => setPage("home")}
                    >
                        <span className="brand-mark">N</span>
                        <span>
                            <strong>NSIKAY</strong>
                            <small>Nantes • Monde</small>
                        </span>
                    </button>

                    <button
                        className="outline-button"
                        onClick={() => setPage("home")}
                    >
                        Accueil
                    </button>
                </header>

                <main className="auth-page">
                    <section className="auth-card">
                        <div className="auth-header">
                            <span className="eyebrow">ESPACE MEMBRE</span>

                            <h1>
                                {loginMode === "login"
                                    ? "Connexion"
                                    : "Créer votre compte NSIKAY"}
                            </h1>

                            <p>
                                {loginMode === "login"
                                    ? "Accédez à votre écosystème NSIKAY."
                                    : "Créez une identité NSIKAY unique pour accéder aux différents espaces."}
                            </p>
                        </div>

                        <div className="auth-switch">
                            <button
                                className={
                                    loginMode === "login" ? "active" : ""
                                }
                                onClick={() => {
                                    setLoginMode("login");
                                    setMessage("");
                                }}
                            >
                                Connexion
                            </button>

                            <button
                                className={
                                    loginMode === "register" ? "active" : ""
                                }
                                onClick={() => {
                                    setLoginMode("register");
                                    setMessage("");
                                }}
                            >
                                Créer un compte
                            </button>
                        </div>

                        {loginMode === "login" ? (
                            <form onSubmit={submitLogin}>
                                <div className="form-grid">
                                    <label>
                                        Identifiant ou e-mail
                                        <input
                                            value={login.identifier}
                                            onChange={(event) =>
                                                setLogin((current) => ({
                                                    ...current,
                                                    identifier:
                                                        event.target.value,
                                                }))
                                            }
                                            placeholder="Votre identifiant"
                                        />
                                    </label>

                                    <label>
                                        Mot de passe
                                        <input
                                            type="password"
                                            value={login.password}
                                            onChange={(event) =>
                                                setLogin((current) => ({
                                                    ...current,
                                                    password:
                                                        event.target.value,
                                                }))
                                            }
                                            placeholder="Votre mot de passe"
                                        />
                                    </label>
                                </div>

                                {message && (
                                    <div className="status-message">
                                        {message}
                                    </div>
                                )}

                                <button
                                    className="primary-button full"
                                    disabled={loading}
                                >
                                    {loading
                                        ? "Connexion..."
                                        : "Se connecter"}
                                </button>

                                <button
                                    type="button"
                                    className="text-button"
                                    onClick={openRegister}
                                >
                                    Je n'ai pas encore de compte
                                </button>
                            </form>
                        ) : (
                            <form onSubmit={submitRegister}>
                                <div className="section-label">
                                    1 — Informations personnelles
                                </div>

                                <div className="form-grid two">
                                    <label>
                                        Prénom *
                                        <input
                                            value={register.firstName}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "firstName",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Prénom"
                                        />
                                    </label>

                                    <label>
                                        Nom *
                                        <input
                                            value={register.lastName}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "lastName",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Nom"
                                        />
                                    </label>

                                    <label>
                                        Nom d'utilisateur
                                        <input
                                            value={register.username}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "username",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="@identifiant"
                                        />
                                    </label>

                                    <label>
                                        E-mail *
                                        <input
                                            type="email"
                                            value={register.email}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "email",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="nom@exemple.com"
                                        />
                                    </label>

                                    <label>
                                        Téléphone
                                        <input
                                            value={register.phone}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "phone",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="+..."
                                        />
                                    </label>

                                    <label>
                                        Pays
                                        <input
                                            value={register.country}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "country",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Pays"
                                        />
                                    </label>

                                    <label>
                                        Ville
                                        <input
                                            value={register.city}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "city",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Ville"
                                        />
                                    </label>

                                    <label>
                                        Mot de passe *
                                        <input
                                            type="password"
                                            value={register.password}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "password",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Mot de passe"
                                        />
                                    </label>

                                    <label>
                                        Confirmation *
                                        <input
                                            type="password"
                                            value={register.confirmPassword}
                                            onChange={(event) =>
                                                updateRegister(
                                                    "confirmPassword",
                                                    event.target.value
                                                )
                                            }
                                            placeholder="Confirmer"
                                        />
                                    </label>
                                </div>

                                <div className="section-label">
                                    2 — Vérification d'identité
                                </div>

                                <p className="identity-info">
                                    Les trois éléments permettent de préparer
                                    la vérification d'identité NSIKAY.
                                </p>

                                <div className="photo-grid">
                                    <PhotoCard
                                        title="Photo personnelle"
                                        description="Photo claire de la personne."
                                        icon="📷"
                                        file={photos.personal}
                                        onChange={(event) =>
                                            updatePhoto(
                                                "personal",
                                                event.target.files?.[0]
                                            )
                                        }
                                    />

                                    <PhotoCard
                                        title="Pièce d'identité"
                                        description="Photo lisible du document."
                                        icon="🪪"
                                        file={photos.identity}
                                        onChange={(event) =>
                                            updatePhoto(
                                                "identity",
                                                event.target.files?.[0]
                                            )
                                        }
                                    />

                                    <PhotoCard
                                        title="Personne + pièce"
                                        description="La personne tient sa pièce dans la même photo."
                                        icon="🤳"
                                        file={photos.identityHolder}
                                        onChange={(event) =>
                                            updatePhoto(
                                                "identityHolder",
                                                event.target.files?.[0]
                                            )
                                        }
                                    />
                                </div>

                                <label className="consent">
                                    <input
                                        type="checkbox"
                                        checked={register.accept}
                                        onChange={(event) =>
                                            updateRegister(
                                                "accept",
                                                event.target.checked
                                            )
                                        }
                                    />
                                    <span>
                                        J'accepte les conditions d'utilisation
                                        et le traitement nécessaire à la
                                        vérification de mon compte.
                                    </span>
                                </label>

                                {message && (
                                    <div className="status-message">
                                        {message}
                                    </div>
                                )}

                                <button
                                    className="primary-button full"
                                    disabled={loading}
                                >
                                    {loading
                                        ? "Transmission..."
                                        : "Créer mon compte NSIKAY"}
                                </button>

                                <button
                                    type="button"
                                    className="text-button"
                                    onClick={openLogin}
                                >
                                    J'ai déjà un compte
                                </button>
                            </form>
                        )}
                    </section>
                </main>
            </div>
        );
    }

    return (
        <div className="app-shell">
            <header className="topbar">
                <button className="brand" onClick={() => setPage("home")}>
                    <span className="brand-mark">N</span>

                    <span>
                        <strong>NSIKAY</strong>
                        <small>Nantes • Monde</small>
                    </span>
                </button>

                <nav className="top-actions">
                    <button
                        className="ghost-button"
                        onClick={openLogin}
                    >
                        Se connecter
                    </button>

                    <button
                        className="primary-button"
                        onClick={openRegister}
                    >
                        Créer un compte
                    </button>
                </nav>
            </header>

            <main>
                <section className="hero">
                    <div className="hero-content">
                        <span className="eyebrow">
                            ÉCOSYSTÈME INTERNATIONAL
                        </span>

                        <h1>
                            Une identité.
                            <br />
                            <span>Trois espaces.</span>
                            <br />
                            Un écosystème.
                        </h1>

                        <p>
                            NSIKAY rassemble identité personnelle, activités
                            professionnelles et engagement dans une
                            plateforme internationale.
                        </p>

                        <div className="hero-actions">
                            <button
                                className="primary-button large"
                                onClick={openRegister}
                            >
                                Créer mon compte
                            </button>

                            <button
                                className="outline-button large"
                                onClick={openLogin}
                            >
                                Se connecter
                            </button>
                        </div>

                        <div className="trust-line">
                            <span>✓ Profil</span>
                            <span>✓ Activités</span>
                            <span>✓ Engagement</span>
                        </div>
                    </div>

                    <div className="hero-orbit">
                        <div className="orbit orbit-one"></div>
                        <div className="orbit orbit-two"></div>

                        <div className="globe">
                            <div className="globe-letter">N</div>
                            <div className="globe-text">
                                NSIKAY
                            </div>
                        </div>

                        <div className="floating-card card-one">
                            👤
                            <strong>Profil</strong>
                        </div>

                        <div className="floating-card card-two">
                            🛍️
                            <strong>WENZE</strong>
                        </div>

                        <div className="floating-card card-three">
                            🌍
                            <strong>Engagement</strong>
                        </div>
                    </div>
                </section>

                <section className="identity-section">
                    <div>
                        <span className="eyebrow">IDENTITÉ NSIKAY</span>
                        <h2>Un compte pour plusieurs dimensions.</h2>
                    </div>

                    <div className="identity-grid">
                        <article>
                            <span>01</span>
                            <h3>Profil personnel</h3>
                            <p>
                                Votre identité et votre présence au sein de
                                l'écosystème.
                            </p>
                        </article>

                        <article>
                            <span>02</span>
                            <h3>Activités</h3>
                            <p>
                                Vos activités, services, projets et
                                opportunités.
                            </p>
                        </article>

                        <article>
                            <span>03</span>
                            <h3>Engagement</h3>
                            <p>
                                Vos actions, missions, événements et
                                contributions.
                            </p>
                        </article>
                    </div>
                </section>

                <section className="features">
                    <span className="eyebrow">L'ÉCOSYSTÈME</span>
                    <h2>Les principaux espaces NSIKAY</h2>

                    <div className="feature-grid">
                        <div>🛍️ WENZE</div>
                        <div>📺 NSIKAY TV</div>
                        <div>💳 Finance</div>
                        <div>🎟️ Événements</div>
                        <div>✓ Certification</div>
                        <div>📣 Publicité</div>
                    </div>
                </section>
            </main>

            <footer>
                <strong>NSIKAY</strong>
                <span>Association française • Écosystème international</span>
            </footer>
        </div>
    );
}

export default App;
