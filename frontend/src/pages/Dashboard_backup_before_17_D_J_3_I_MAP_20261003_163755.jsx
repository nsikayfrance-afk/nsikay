import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const spaces = [
  {
    icon: "👤",
    title: "Profil personnel",
    text: "Votre identité, vos informations et votre présence NSIKAY.",
    path: "/mon-profil",
  },
  {
    icon: "💼",
    title: "Mes activités",
    text: "Présentez vos métiers, services, projets et activités.",
    path: "/metiers",
  },
  {
    icon: "🤝",
    title: "Mon engagement",
    text: "Participez aux événements, actions et initiatives NSIKAY.",
    path: "/events",
  },
];

const profileTypes = [
  ["👤", "Personne", "Profil personnel"],
  ["💼", "Professionnel", "Métier / activité"],
  ["🏢", "Entreprise", "Organisation commerciale"],
  ["🏦", "Banque", "Services financiers"],
  ["🏫", "École", "Éducation / université"],
  ["🎓", "Formation", "Centre de formation"],
  ["🏥", "Santé", "Hôpital / santé"],
  ["🤝", "Association", "ONG / association"],
  ["🏛️", "Institution", "Institution publique"],
  ["🎨", "Artiste", "Créateur / culture"],
  ["🧑‍💼", "Agent", "Expert / mission"],
];

const modules = [
  ["🛒", "WENZE", "Commerce", "0 % de commission commerciale", "/wenze"],
  ["💰", "LIBENGA", "Portefeuille", "Paiements et opérations", "/libenga"],
  ["🛡️", "Certification", "Confiance", "Certification des activités", "/certification"],
  ["🎫", "Événements", "Agenda", "Événements et rencontres", "/events"],
  ["📺", "NSIKAY TV", "Média", "Actualités, culture et contenus", "/tv"],
  ["📢", "Publicité", "Visibilité", "Développez votre présence", "/admin"],
];

const certificationAuthorityModule = [
  [
    "🛡️",
    "Autorité Certification",
    "Administration",
    "Gérer les certifications des activités NSIKAY",
    "/certification-activites",
  ],
];

export default function Dashboard() {
  const navigate = useNavigate();
  const {
    user,
    profile,
    logout,
    isCertificationAuthority,
  } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate("/connexion");
  };

  const displayName =
    profile?.full_name ||
    profile?.name ||
    user?.first_name ||
    user?.username ||
    "Membre NSIKAY";

  return (
    <div className="ns-dashboard">

      <header className="ns-topbar">
        <div className="ns-brand" onClick={() => navigate("/espace")}>
          <div className="ns-brand-mark">N</div>
          <div>
            <strong>NSIKAY</strong>
            <span>Écosystème international</span>
          </div>
        </div>

        <nav className="ns-topnav">
          <button onClick={() => navigate("/espace")}>Accueil</button>
          <button onClick={() => navigate("/profils")}>Profils</button>
          <button onClick={() => navigate("/events")}>Événements</button>
          <button onClick={() => navigate("/tv")}>TV</button>
        </nav>

        <div className="ns-user-menu">
          <button
            className="ns-avatar"
            onClick={() => navigate("/mon-profil")}
            title="Mon profil"
          >
            {displayName.charAt(0).toUpperCase()}
          </button>

          <button className="ns-logout" onClick={handleLogout}>
            Déconnexion
          </button>
        </div>
      </header>

      <main>

        <section className="ns-hero">
          <div className="ns-hero-content">
            <span className="ns-eyebrow">ESPACE MEMBRE</span>

            <h1>
              Bienvenue dans
              <br />
              <strong>votre espace NSIKAY</strong>
            </h1>

            <p>
              Un seul compte pour votre identité, vos activités et votre
              engagement dans l'écosystème NSIKAY.
            </p>

            <div className="ns-hero-actions">
              <button
                className="ns-btn ns-btn-primary"
                onClick={() => navigate("/mon-profil")}
              >
                Mon profil →
              </button>

              <button
                className="ns-btn ns-btn-secondary"
                onClick={() => navigate("/profils")}
              >
                Explorer les profils
              </button>
            </div>
          </div>

          <div className="ns-hero-orbit">
            <div className="ns-orbit-center">N</div>
            <div className="ns-orbit-item orbit-one">👤</div>
            <div className="ns-orbit-item orbit-two">💼</div>
            <div className="ns-orbit-item orbit-three">🤝</div>
          </div>
        </section>

        <section className="ns-section">
          <div className="ns-section-heading">
            <div>
              <span className="ns-eyebrow">IDENTITÉ NSIKAY</span>
              <h2>Votre espace 3-en-1</h2>
            </div>
            <p>
              Une identité unique pour gérer votre présence, vos activités
              et votre participation.
            </p>
          </div>

          <div className="ns-space-grid">
            {spaces.map((space) => (
              <button
                key={space.title}
                className="ns-space-card"
                onClick={() => navigate(space.path)}
              >
                <span className="ns-card-icon">{space.icon}</span>
                <h3>{space.title}</h3>
                <p>{space.text}</p>
                <span className="ns-card-link">Accéder →</span>
              </button>
            ))}
          </div>
        </section>

        <section className="ns-section ns-section-dark">
          <div className="ns-section-heading">
            <div>
              <span className="ns-eyebrow">ÉCOSYSTÈME</span>
              <h2>Créer ou découvrir un profil</h2>
            </div>
            <button
              className="ns-link-button"
              onClick={() => navigate("/profils")}
            >
              Voir tous les profils →
            </button>
          </div>

          <div className="ns-profile-grid">
            {profileTypes.map(([icon, title, text]) => (
              <button
                key={title}
                className="ns-profile-card"
                onClick={() => navigate("/profils")}
              >
                <span>{icon}</span>
                <strong>{title}</strong>
                <small>{text}</small>
              </button>
            ))}
          </div>
        </section>

        <section className="ns-section">
          <div className="ns-section-heading">
            <div>
              <span className="ns-eyebrow">SERVICES NSIKAY</span>
              <h2>Les grands modules</h2>
            </div>
          </div>

          <div className="ns-module-grid">
            {modules.map(([icon, title, category, text, path]) => (
              <button
                key={title}
                className="ns-module-card"
                onClick={() => navigate(path)}
              >
                <span className="ns-module-icon">{icon}</span>
                <div>
                  <small>{category}</small>
                  <h3>{title}</h3>
                  <p>{text}</p>
                </div>
                <b>→</b>
              </button>
            ))}
          </div>
        </section>

        <section className="ns-quick-panel">
          <div>
            <span className="ns-eyebrow">VOTRE IDENTITÉ</span>
            <h2>{displayName}</h2>
            <p>
              Connecté avec le compte <strong>@{user?.username || "membre"}</strong>
            </p>
          </div>

          <div className="ns-quick-actions">
            <button onClick={() => navigate("/mon-profil")}>
              Modifier mon profil
            </button>
            <button onClick={() => navigate("/certification")}>
              Vérifier mes activités
            </button>
          </div>
        </section>

      </main>

      <footer className="ns-footer">
        <div>
          <strong>NSIKAY</strong>
          <span>Écosystème international</span>
        </div>

        <div className="ns-footer-links">
          <button onClick={() => navigate("/profils")}>Profils</button>
          <button onClick={() => navigate("/wenze")}>WENZE</button>
          <button onClick={() => navigate("/libenga")}>LIBENGA</button>
          <button onClick={() => navigate("/events")}>Événements</button>
          <button onClick={() => navigate("/tv")}>NSIKAY TV</button>
        </div>
      </footer>

    </div>
  );
}

