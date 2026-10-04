import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { mainModules } from "../data/nsikayData";

export default function Dashboard() {
    const { user, profile, logout } = useAuth();

    const displayName =
        user?.first_name ||
        user?.username ||
        "Membre NSIKAY";

    return (
        <div className="ns-app">
            <header className="ns-header">
                <Link to="/espace" className="ns-logo">
                    <span className="logo-symbol">N</span>
                    <span>
                        <strong>NSIKAY</strong>
                        <small>International Ecosystem</small>
                    </span>
                </Link>

                <nav className="top-nav">
                    <Link to="/espace">Accueil</Link>
                    <Link to="/profils">Profils</Link>
                    <Link to="/metiers">Métiers</Link>
                    <Link to="/wenze">WENZE</Link>
                </nav>

                <div className="user-menu">
                    <span>{displayName}</span>

                    <button
                        onClick={logout}
                        className="logout-button"
                    >
                        Déconnexion
                    </button>
                </div>
            </header>

            <main className="dashboard">
                <section className="hero-panel">
                    <div>
                        <span className="eyebrow">
                            ESPACE NSIKAY
                        </span>

                        <h1>
                            Bienvenue,
                            <br />
                            <span>{displayName}</span>
                        </h1>

                        <p>
                            Votre identité, vos activités et votre
                            engagement réunis dans un seul espace.
                        </p>
                    </div>

                    <Link
                        to="/mon-profil"
                        className="hero-action"
                    >
                        Voir mon profil →
                    </Link>
                </section>

                <section className="identity-grid">
                    <div className="identity-card">
                        <span>👤</span>
                        <div>
                            <small>IDENTITÉ</small>
                            <strong>
                                {user?.username || "Membre"}
                            </strong>
                        </div>
                    </div>

                    <div className="identity-card">
                        <span>✉️</span>
                        <div>
                            <small>CONTACT</small>
                            <strong>
                                {user?.email || "Non renseigné"}
                            </strong>
                        </div>
                    </div>

                    <div className="identity-card">
                        <span>🛡️</span>
                        <div>
                            <small>PROFIL</small>
                            <strong>
                                {profile?.profile_type ||
                                    "À compléter"}
                            </strong>
                        </div>
                    </div>
                </section>

                <div className="section-heading">
                    <div>
                        <span className="eyebrow">
                            ÉCOSYSTÈME
                        </span>
                        <h2>Vos espaces NSIKAY</h2>
                    </div>
                </div>

                <section className="module-grid">
                    {mainModules.map(
                        ([key, icon, title, description]) => (
                            <Link
                                key={key}
                                to={
                                    key === "profile"
                                        ? "/profils"
                                        : `/${key}`
                                }
                                className={`module-card module-${key}`}
                            >
                                <span className="module-icon">
                                    {icon}
                                </span>

                                <div>
                                    <h3>{title}</h3>
                                    <p>{description}</p>
                                </div>

                                <span className="module-arrow">
                                    →
                                </span>
                            </Link>
                        )
                    )}
                </section>
            </main>
        </div>
    );
}
