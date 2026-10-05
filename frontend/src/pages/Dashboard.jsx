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

const modules = [
  ["🛒", "WENZE", "Commerce", "0 % de commission commerciale", "/wenze"],
  ["💰", "LIBENGA", "Portefeuille", "Paiements et opérations", "/libenga"],
  ["🛡️", "Certification", "Confiance", "Certification des activités", "/certification"],
  ["🎫", "Événements", "Agenda", "Événements et rencontres", "/events"],
  ["📺", "NSIKAY TV", "Média", "Actualités, culture et contenus", "/tv"],
  ["📢", "Publicité", "Visibilité", "Développez votre présence", "/publicite"],
];

export default function Dashboard() {
  const navigate = useNavigate();

  const {
    user,
    profile,
    logout,
    isCertificationAuthority,
    isSuperuser,
    isStaff,
  } = useAuth();

  const canAccessAdministration =
    Boolean(isSuperuser) || Boolean(isStaff);

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

  const visibleModules = canAccessAdministration
    ? [
        ...modules,
        ["⚙️", "Administration", "Gestion", "Administration générale de NSIKAY", "/admin"],
      ]
    : modules;

  return (
    <div className="ns-dashboard-page">
      <header className="ns-dashboard-header">
        <div
          className="ns-dashboard-brand"
          onClick={() => navigate("/espace")}
        >
          <div className="ns-dashboard-logo">N</div>
          <div>
            <strong>NSIKAY</strong>
            <span>Écosystème international</span>
          </div>
        </div>

        <nav className="ns-dashboard-nav">
          <button onClick={() => navigate("/espace")}>Accueil</button>
          <button onClick={() => navigate("/profils")}>Profils</button>
          <button onClick={() => navigate("/events")}>Événements</button>
          <button onClick={() => navigate("/tv")}>TV</button>
        </nav>

        <div className="ns-dashboard-user">
          <button
            className="ns-dashboard-avatar"
            onClick={() => navigate("/mon-profil")}
            title="Mon profil"
          >
            {displayName.charAt(0).toUpperCase()}
          </button>

          <button
            className="ns-dashboard-logout"
            onClick={handleLogout}
          >
            Déconnexion
          </button>
        </div>
      </header>

      <main className="ns-dashboard-main">

        <section className="ns-dashboard-hero">
          <div className="ns-kuba-watermark" />

          <div className="ns-dashboard-hero-content">
            <span className="ns-section-kicker">ESPACE MEMBRE NSIKAY</span>

            <h1>
              Bienvenue dans
              <br />
              <strong>votre espace NSIKAY</strong>
            </h1>

            <p>
              Un seul compte pour votre identité, vos activités et votre
              engagement dans l'écosystème NSIKAY.
            </p>

            <div className="ns-dashboard-actions">
              <button
                className="ns-btn-gold"
                onClick={() => navigate("/mon-profil")}
              >
                Mon profil →
              </button>

              <button
                className="ns-dashboard-outline"
                onClick={() => navigate("/metiers")}
              >
                Mes activités
              </button>
            </div>
          </div>
        </section>

        <section className="ns-dashboard-section">
          <div className="ns-section-header">
            <span className="ns-section-kicker">IDENTITÉ · ACTIVITÉS · ENGAGEMENT</span>
            <h2 className="ns-section-title">Vos trois espaces essentiels</h2>
          </div>

          <div className="ns-dashboard-space-grid">
            {spaces.map(([item], index) => {
              const space = spaces[index];

              return (
                <button
                  key={space.path}
                  className="ns-dashboard-space-card"
                  onClick={() => navigate(space.path)}
                >
                  <span className="ns-dashboard-card-icon">
                    {space.icon}
                  </span>

                  <span className="ns-dashboard-card-title">
                    {space.title}
                  </span>

                  <span className="ns-dashboard-card-text">
                    {space.text}
                  </span>

                  <span className="ns-dashboard-card-link">
                    Accéder →
                  </span>
                </button>
              );
            })}
          </div>
        </section>

        <section className="ns-dashboard-section">
          <div className="ns-section-header">
            <span className="ns-section-kicker">ÉCOSYSTÈME NSIKAY</span>
            <h2 className="ns-section-title">Services et modules</h2>
          </div>

          <div className="ns-dashboard-module-grid">
            {visibleModules.map(
              ([icon, title, category, text, path]) => (
                <button
                  key={path}
                  className="ns-dashboard-module-card"
                  onClick={() => navigate(path)}
                >
                  <span className="ns-dashboard-module-icon">
                    {icon}
                  </span>

                  <span className="ns-dashboard-module-category">
                    {category}
                  </span>

                  <span className="ns-dashboard-module-title">
                    {title}
                  </span>

                  <span className="ns-dashboard-module-text">
                    {text}
                  </span>

                  <span className="ns-dashboard-card-link">
                    Ouvrir →
                  </span>
                </button>
              )
            )}
          </div>
        </section>

        {isCertificationAuthority && (
          <section className="ns-dashboard-section ns-dashboard-authority">
            <div className="ns-section-header">
              <span className="ns-section-kicker">
                AUTORITÉ DE CERTIFICATION
              </span>

              <h2 className="ns-section-title">
                Administration des certifications
              </h2>
            </div>

            <button
              className="ns-dashboard-authority-card"
              onClick={() => navigate("/certification-activites")}
            >
              <span className="ns-dashboard-card-icon">🛡️</span>
              <span>
                Gérer les certifications des activités NSIKAY →
              </span>
            </button>
          </section>
        )}

      </main>

      <footer className="ns-dashboard-footer">
        <strong>NSIKAY</strong>
        <span>Une identité. Des activités. Un engagement.</span>
      </footer>
    </div>
  );
}
