import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function MyProfile() {
    const { user, profile } = useAuth();

    return (
        <div className="ns-app">
            <header className="simple-header">
                <Link to="/espace" className="ns-logo">
                    <span className="logo-symbol">N</span>
                    <span>
                        <strong>NSIKAY</strong>
                        <small>Mon profil</small>
                    </span>
                </Link>

                <Link to="/espace" className="back-link">
                    ← Mon espace
                </Link>
            </header>

            <main className="content-page">
                <div className="profile-cover">
                    <div className="profile-avatar">
                        {(user?.username || "N")
                            .charAt(0)
                            .toUpperCase()}
                    </div>

                    <div>
                        <span className="eyebrow">
                            PROFIL NSIKAY
                        </span>

                        <h1>
                            {user?.first_name ||
                                user?.username ||
                                "Membre NSIKAY"}
                        </h1>

                        <p>
                            @{user?.username}
                        </p>
                    </div>
                </div>

                <section className="profile-information">
                    <div className="info-card">
                        <span>Identifiant</span>
                        <strong>
                            {user?.username || "—"}
                        </strong>
                    </div>

                    <div className="info-card">
                        <span>E-mail</span>
                        <strong>
                            {user?.email || "—"}
                        </strong>
                    </div>

                    <div className="info-card">
                        <span>Type de profil</span>
                        <strong>
                            {profile?.profile_type ||
                                "Profil à compléter"}
                        </strong>
                    </div>

                    <div className="info-card">
                        <span>Vérification</span>
                        <strong>
                            {profile?.verified
                                ? "✓ Vérifié"
                                : "À vérifier"}
                        </strong>
                    </div>
                </section>

                <section className="three-space">
                    <article>
                        <span>👤</span>
                        <h2>Profil personnel</h2>
                        <p>
                            Votre identité et vos informations
                            personnelles.
                        </p>
                    </article>

                    <article>
                        <span>💼</span>
                        <h2>Activités</h2>
                        <p>
                            Vos métiers, services, projets et activités.
                        </p>
                    </article>

                    <article>
                        <span>🤝</span>
                        <h2>Engagement</h2>
                        <p>
                            Vos engagements, missions et participations.
                        </p>
                    </article>
                </section>
            </main>
        </div>
    );
}
