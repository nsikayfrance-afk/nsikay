import React from "react";
import { Link } from "react-router-dom";
import "../styles/nsikay-design.css";

const modules = [
  {
    icon: "🛒",
    title: "WENZE",
    text: "Commerce, vendeurs, produits, commandes et livraisons.",
    path: "/wenze",
  },
  {
    icon: "💳",
    title: "Libenga",
    text: "Portefeuille, paiements et services financiers numériques.",
    path: "/libenga",
  },
  {
    icon: "🚗",
    title: "Transport",
    text: "Livraisons WENZE, courses et location de véhicules.",
    path: "/transport",
  },
  {
    icon: "📅",
    title: "Événements",
    text: "Événements, inscriptions, billets et rencontres.",
    path: "/events",
  },
  {
    icon: "📺",
    title: "NSIKAY TV",
    text: "Actualités, culture, économie, sport et émissions.",
    path: "/tv",
  },
  {
    icon: "💼",
    title: "Activités",
    text: "Métiers, entreprises, projets et opportunités.",
    path: "/activities",
  },
];

const themes = [
  "Économie",
  "Sport & Loisirs",
  "Culture & Art",
  "Technologie & Innovation",
  "Agriculture & Agronomie",
  "Social",
  "Religion & Histoire",
  "+18",
];

export default function Home() {
  return (
    <div className="nsikay-home">

      <header className="nsikay-header">
        <Link to="/" className="nsikay-brand">
          <span className="nsikay-brand-mark">N</span>
          <span>
            <strong>NSIKAY</strong>
            <small>L’écosystème international</small>
          </span>
        </Link>

        <nav className="nsikay-nav">
          <Link to="/">Accueil</Link>
          <Link to="/activities">Activités</Link>
          <Link to="/wenze">WENZE</Link>
          <Link to="/events">Événements</Link>
          <Link to="/tv">TV</Link>
          <Link to="/transport">Transport</Link>
        </nav>

        <div className="nsikay-header-actions">
          <Link to="/connexion" className="nsikay-login-link">
            Connexion
          </Link>
          <Link to="/inscription" className="nsikay-primary-small">
            Créer un compte
          </Link>
        </div>
      </header>

      <main>

        <section className="nsikay-hero">

          <div className="nsikay-hero-content">
            <div className="nsikay-eyebrow">
              <span></span>
              ÉCOSYSTÈME INTERNATIONAL
            </div>

            <h1>
              Connecter les
              <em> personnes</em>,
              <br />
              les activités et
              <br />
              les opportunités.
            </h1>

            <p>
              NSIKAY réunit dans un même écosystème les personnes,
              entreprises, activités, talents, partenaires, commerces
              et services à travers le monde.
            </p>

            <div className="nsikay-hero-actions">
              <Link to="/inscription" className="nsikay-primary-button">
                Créer mon compte
                <span>→</span>
              </Link>

              <Link to="/connexion" className="nsikay-secondary-button">
                Se connecter
              </Link>
            </div>

            <div className="nsikay-hero-stats">
              <div>
                <strong>01</strong>
                <span>Identité</span>
              </div>
              <div>
                <strong>03</strong>
                <span>Espaces</span>
              </div>
              <div>
                <strong>∞</strong>
                <span>Opportunités</span>
              </div>
            </div>
          </div>

          <div className="nsikay-hero-visual">
            <div className="nsikay-hero-glow"></div>

            <img
              src="/images/nsikay-hero.jpg"
              alt="NSIKAY - écosystème international"
              className="nsikay-hero-image"
              onError={(event) => {
                event.currentTarget.src =
                  "/images/nsikay-hero-placeholder.svg";
              }}
            />

            <div className="nsikay-floating-card card-finance">
              <span>💳</span>
              <div>
                <strong>Finance</strong>
                <small>Connectée</small>
              </div>
            </div>

            <div className="nsikay-floating-card card-commerce">
              <span>🛒</span>
              <div>
                <strong>WENZE</strong>
                <small>Commerce</small>
              </div>
            </div>

            <div className="nsikay-floating-card card-world">
              <span>🌍</span>
              <div>
                <strong>International</strong>
                <small>Connecté</small>
              </div>
            </div>
          </div>
        </section>

        <section className="nsikay-section">
          <div className="nsikay-section-heading">
            <div>
              <span className="nsikay-section-label">L'ÉCOSYSTÈME</span>
              <h2>Tout NSIKAY au même endroit.</h2>
            </div>
            <p>
              Une seule identité pour découvrir, développer,
              vendre, participer et créer des opportunités.
            </p>
          </div>

          <div className="nsikay-module-grid">
            {modules.map((module) => (
              <Link
                to={module.path}
                className="nsikay-module-card"
                key={module.title}
              >
                <div className="nsikay-module-icon">{module.icon}</div>
                <div>
                  <h3>{module.title}</h3>
                  <p>{module.text}</p>
                </div>
                <span className="nsikay-card-arrow">↗</span>
              </Link>
            ))}
          </div>
        </section>

        <section className="nsikay-identity-section">
          <div className="nsikay-identity-copy">
            <span className="nsikay-section-label">UNE IDENTITÉ</span>
            <h2>
              Un compte.
              <br />
              <em>Trois espaces.</em>
            </h2>
            <p>
              Votre identité NSIKAY vous donne accès à votre espace
              personnel, vos activités et votre engagement.
            </p>

            <Link to="/inscription" className="nsikay-outline-button">
              Découvrir mon espace →
            </Link>
          </div>

          <div className="nsikay-identity-cards">
            <div className="identity-card identity-personal">
              <span>01</span>
              <div className="identity-card-icon">👤</div>
              <h3>Profil personnel</h3>
              <p>Votre identité et votre réseau.</p>
            </div>

            <div className="identity-card identity-business">
              <span>02</span>
              <div className="identity-card-icon">💼</div>
              <h3>Activités</h3>
              <p>Vos métiers, entreprises et projets.</p>
            </div>

            <div className="identity-card identity-engagement">
              <span>03</span>
              <div className="identity-card-icon">🤝</div>
              <h3>Engagement</h3>
              <p>Votre participation à l’écosystème.</p>
            </div>
          </div>
        </section>

        <section className="nsikay-themes">
          <div className="nsikay-section-heading">
            <div>
              <span className="nsikay-section-label">CONTENU</span>
              <h2>Les grands univers NSIKAY.</h2>
            </div>
          </div>

          <div className="nsikay-theme-list">
            {themes.map((theme) => (
              <div className="nsikay-theme" key={theme}>
                <span>+</span>
                {theme}
              </div>
            ))}
          </div>
        </section>

        <section className="nsikay-final-cta">
          <div>
            <span className="nsikay-section-label">REJOINDRE NSIKAY</span>
            <h2>
              Construisons ensemble
              <br />
              les opportunités de demain.
            </h2>
          </div>

          <Link to="/inscription" className="nsikay-primary-button">
            Créer mon compte
            <span>→</span>
          </Link>
        </section>

      </main>

      <footer className="nsikay-footer">
        <div className="nsikay-footer-brand">
          <span className="nsikay-brand-mark">N</span>
          <div>
            <strong>NSIKAY</strong>
            <small>L’écosystème international</small>
          </div>
        </div>

        <div className="nsikay-footer-links">
          <Link to="/connexion">Connexion</Link>
          <Link to="/inscription">Créer un compte</Link>
          <Link to="/wenze">WENZE</Link>
          <Link to="/events">Événements</Link>
        </div>

        <p>© {new Date().getFullYear()} NSIKAY — Tous droits réservés.</p>
      </footer>

    </div>
  );
}