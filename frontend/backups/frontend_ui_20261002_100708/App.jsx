import React, { useState } from "react";
import "./index.css";

const channels = [
  "Économie",
  "Sport & Loisirs",
  "Culture & Art",
  "Technologie & Innovation",
  "Agriculture & Agronomie",
  "Social",
  "Religion & Histoire",
  "Contenus réservés aux adultes",
];

const partners = [
  "PARTENAIRE 01",
  "PARTENAIRE 02",
  "PARTENAIRE 03",
  "PARTENAIRE 04",
  "PARTENAIRE 05",
];

function Logo({ small = false }) {
  return (
    <div className={small ? "brand brand-small" : "brand"}>
      <div className="brand-mark">N</div>
      <div>
        <strong>NSIKAY</strong>
        <span>Une identité. Un écosystème.</span>
      </div>
    </div>
  );
}

function Avatar({ name = "NS", large = false }) {
  return (
    <div className={large ? "avatar avatar-large" : "avatar"}>
      {name.substring(0, 2).toUpperCase()}
    </div>
  );
}

function Header({ page, setPage }) {
  return (
    <header className="topbar">
      <button className="logo-button" onClick={() => setPage("home")}>
        <Logo />
      </button>

      <nav className="main-nav">
        <button
          className={page === "home" ? "nav-active" : ""}
          onClick={() => setPage("home")}
        >
          Accueil
        </button>

        <button
          className={page === "tv" ? "nav-active" : ""}
          onClick={() => setPage("tv")}
        >
          📺 NSIKAY TV
        </button>

        <button
          className={page === "advertising" ? "nav-active" : ""}
          onClick={() => setPage("advertising")}
        >
          📢 Publicité
        </button>

        <button onClick={() => setPage("events")}>Événements</button>
        <button onClick={() => setPage("wenze")}>WENZE</button>
      </nav>

      <div className="header-actions">
        <button className="outline-button" onClick={() => setPage("login")}>
          Se connecter
        </button>
        <button className="gold-button" onClick={() => setPage("register")}>
          Créer un compte
        </button>
      </div>
    </header>
  );
}

function TvScreen({ setPage }) {
  return (
    <div className="tv-wrapper">
      <div className="tv-frame">
        <div className="tv-top">
          <span className="live-dot">● EN DIRECT</span>
          <span>NSIKAY TV</span>
        </div>

        <div className="tv-screen">
          <div className="tv-globe">
            <div className="globe-ring ring-one"></div>
            <div className="globe-ring ring-two"></div>
            <div className="globe-core">N</div>
          </div>

          <div className="tv-content">
            <span className="tv-label">NSIKAY TV</span>
            <h2>Le monde se connecte.</h2>
            <p>
              Actualités, culture, économie, innovation, sport et événements
              au sein d'un même écosystème.
            </p>
            <button
              className="gold-button"
              onClick={() => setPage("tv")}
            >
              Regarder NSIKAY TV
            </button>
          </div>
        </div>

        <div className="tv-controls">
          <span>▶</span>
          <div className="progress">
            <div></div>
          </div>
          <span>LIVE</span>
        </div>
      </div>
    </div>
  );
}

function AdvertisingPreview({ setPage }) {
  return (
    <section className="advertising-preview">
      <div>
        <span className="section-kicker">ESPACE PUBLICITAIRE</span>
        <h2>Votre visibilité sur NSIKAY</h2>
        <p>
          Présentez votre entreprise, votre activité, votre événement ou
          votre marque auprès de la communauté NSIKAY.
        </p>

        <button
          className="gold-button"
          onClick={() => setPage("advertising")}
        >
          Créer une publicité
        </button>
      </div>

      <div className="ad-display">
        <div className="ad-badge">PUBLICITÉ</div>
        <div className="ad-logo">N</div>
        <h3>VOTRE PUBLICITÉ ICI</h3>
        <p>Une vitrine professionnelle au cœur de NSIKAY.</p>
        <div className="ad-footer-line"></div>
      </div>
    </section>
  );
}

function Partners() {
  return (
    <section className="partners-section">
      <div className="section-heading centered">
        <span className="section-kicker">ÉCOSYSTÈME</span>
        <h2>Nos partenaires</h2>
        <p>
          Les partenaires autorisés peuvent être présentés dans cet espace.
        </p>
      </div>

      <div className="partners-grid">
        {partners.map((partner, index) => (
          <div className="partner-card" key={index}>
            <div className="partner-logo">
              <span>N</span>
            </div>
            <strong>{partner}</strong>
            <small>Logo partenaire</small>
          </div>
        ))}
      </div>
    </section>
  );
}

function Footer({ setPage }) {
  return (
    <footer className="footer">
      <div className="footer-main">
        <div className="footer-brand">
          <Logo small />
          <p>
            Une plateforme internationale dédiée à l'identité, aux activités,
            à l'engagement, au commerce, aux événements et aux médias.
          </p>
        </div>

        <div>
          <h4>NSIKAY</h4>
          <button onClick={() => setPage("home")}>Accueil</button>
          <button onClick={() => setPage("tv")}>NSIKAY TV</button>
          <button onClick={() => setPage("advertising")}>Publicité</button>
          <button onClick={() => setPage("events")}>Événements</button>
        </div>

        <div>
          <h4>Services</h4>
          <button onClick={() => setPage("wenze")}>WENZE</button>
          <button onClick={() => setPage("profile")}>Profil</button>
          <button onClick={() => setPage("register")}>Certification</button>
          <button>Libenga</button>
        </div>

        <div>
          <h4>Partenaires</h4>
          <button>Devenir partenaire</button>
          <button>Partenaires institutionnels</button>
          <button>Partenaires commerciaux</button>
        </div>
      </div>

      <div className="official-box">
        <div>
          <span className="official-kicker">INFORMATIONS OFFICIELLES</span>
          <h3>NSIKAY — Association déclarée en France</h3>
        </div>

        <div className="official-data">
          <span>RNA <strong>W442031317</strong></span>
          <span>SIREN <strong>995 089 711</strong></span>
          <span>SIRET <strong>995 089 711 00015</strong></span>
          <span>Loi <strong>1901</strong></span>
          <span>Création <strong>06/12/2025</strong></span>
          <span>Publication JOAFE <strong>16/12/2025</strong></span>
        </div>
      </div>

      <div className="footer-bottom">
        <span>© 2026 NSIKAY — Tous droits réservés.</span>
        <div>
          <button>Mentions légales</button>
          <button>Confidentialité</button>
          <button>Conditions</button>
        </div>
      </div>
    </footer>
  );
}

function Home({ setPage }) {
  return (
    <>
      <section className="hero">
        <div className="hero-text">
          <span className="hero-kicker">NSIKAY INTERNATIONAL</span>

          <h1>
            Une identité.
            <br />
            <span>Un écosystème.</span>
          </h1>

          <p>
            Une plateforme conçue pour connecter les personnes, les activités,
            les entreprises, les événements, les médias et les opportunités.
          </p>

          <div className="hero-actions">
            <button
              className="gold-button large-button"
              onClick={() => setPage("register")}
            >
              Créer mon compte
            </button>

            <button
              className="outline-button light-button"
              onClick={() => setPage("tv")}
            >
              📺 Découvrir NSIKAY TV
            </button>
          </div>

          <div className="identity-preview">
            <Avatar name="NK" large />
            <div>
              <strong>Votre identité NSIKAY</strong>
              <span>Profil personnel • Activités • Engagement</span>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="globe">
            <div className="globe-line line-one"></div>
            <div className="globe-line line-two"></div>
            <div className="globe-center">N</div>
          </div>

          <div className="floating-card card-one">
            <span>👤</span>
            <div>
              <strong>Profil</strong>
              <small>Votre identité</small>
            </div>
          </div>

          <div className="floating-card card-two">
            <span>📺</span>
            <div>
              <strong>NSIKAY TV</strong>
              <small>Votre média</small>
            </div>
          </div>

          <div className="floating-card card-three">
            <span>📢</span>
            <div>
              <strong>Publicité</strong>
              <small>Votre visibilité</small>
            </div>
          </div>
        </div>
      </section>

      <section className="modules-section">
        <div className="section-heading">
          <span className="section-kicker">L'ÉCOSYSTÈME NSIKAY</span>
          <h2>Tout au même endroit</h2>
        </div>

        <div className="module-grid">
          <button className="module-card" onClick={() => setPage("wenze")}>
            <div className="module-icon">W</div>
            <h3>WENZE</h3>
            <p>
              Commerce et présentation des produits et services au sein de
              l'écosystème NSIKAY.
            </p>
            <span>Découvrir →</span>
          </button>

          <button className="module-card tv-module" onClick={() => setPage("tv")}>
            <div className="module-icon">📺</div>
            <h3>NSIKAY TV</h3>
            <p>
              Des chaînes et contenus autour de l'économie, la culture, le
              sport, la technologie et la société.
            </p>
            <span>Regarder →</span>
          </button>

          <button
            className="module-card"
            onClick={() => setPage("events")}
          >
            <div className="module-icon">◆</div>
            <h3>ÉVÉNEMENTS</h3>
            <p>
              Découvrez, créez et présentez vos événements au sein de NSIKAY.
            </p>
            <span>Découvrir →</span>
          </button>

          <button
            className="module-card advertising-module"
            onClick={() => setPage("advertising")}
          >
            <div className="module-icon">📢</div>
            <h3>PUBLICITÉ</h3>
            <p>
              Donnez de la visibilité à votre entreprise, votre activité ou
              votre événement.
            </p>
            <span>Faire connaître →</span>
          </button>

          <button className="module-card">
            <div className="module-icon">L</div>
            <h3>LIBENGA</h3>
            <p>
              L'espace financier de l'écosystème NSIKAY.
            </p>
            <span>Découvrir →</span>
          </button>

          <button className="module-card">
            <div className="module-icon">✓</div>
            <h3>CERTIFICATION</h3>
            <p>
              Un système de certification adapté aux personnes, activités et
              organisations.
            </p>
            <span>En savoir plus →</span>
          </button>
        </div>
      </section>

      <TvScreen setPage={setPage} />

      <AdvertisingPreview setPage={setPage} />

      <Partners />
    </>
  );
}

function TvPage({ setPage }) {
  return (
    <main className="inner-page">
      <div className="page-header">
        <span className="section-kicker">NSIKAY MEDIA</span>
        <h1>📺 NSIKAY TV</h1>
        <p>
          Les contenus et chaînes de l'écosystème NSIKAY.
        </p>
      </div>

      <TvScreen setPage={setPage} />

      <section className="channels-section">
        <div className="section-heading">
          <span className="section-kicker">CHAÎNES</span>
          <h2>Explorez les univers NSIKAY</h2>
        </div>

        <div className="channel-grid">
          {channels.map((channel, index) => (
            <div className="channel-card" key={channel}>
              <div className="channel-number">
                {String(index + 1).padStart(2, "0")}
              </div>
              <div>
                <h3>{channel}</h3>
                <p>Chaîne NSIKAY</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

function AdvertisingPage() {
  return (
    <main className="inner-page">
      <div className="page-header">
        <span className="section-kicker">VISIBILITÉ</span>
        <h1>📢 Publicité NSIKAY</h1>
        <p>
          Un espace destiné aux entreprises, organisations, créateurs et
          porteurs de projets.
        </p>
      </div>

      <section className="ad-dashboard">
        <div className="ad-dashboard-card primary">
          <span>01</span>
          <h2>Créer une publicité</h2>
          <p>
            Présentez votre activité et choisissez votre emplacement de
            visibilité.
          </p>
          <button className="gold-button">Commencer</button>
        </div>

        <div className="ad-dashboard-card">
          <span>02</span>
          <h2>Mes campagnes</h2>
          <p>
            Retrouvez et gérez vos campagnes publicitaires.
          </p>
          <button className="outline-button">Voir mes campagnes</button>
        </div>

        <div className="ad-dashboard-card">
          <span>03</span>
          <h2>Visibilité</h2>
          <p>
            Prévisualisez les emplacements disponibles dans l'écosystème.
          </p>
          <button className="outline-button">Voir les espaces</button>
        </div>
      </section>

      <div className="advertising-banner-large">
        <div className="ad-badge">ESPACE PUBLICITAIRE NSIKAY</div>
        <h2>Votre marque peut apparaître ici</h2>
        <p>
          Accueil • NSIKAY TV • Événements • WENZE • Espaces partenaires
        </p>
      </div>
    </main>
  );
}

function SimplePage({ title, text }) {
  return (
    <main className="inner-page">
      <div className="page-header">
        <span className="section-kicker">NSIKAY</span>
        <h1>{title}</h1>
        <p>{text}</p>
      </div>

      <div className="placeholder-panel">
        <div className="placeholder-icon">N</div>
        <h2>Espace NSIKAY</h2>
        <p>Cette section sera connectée au backend Django.</p>
      </div>
    </main>
  );
}

function Login({ setPage }) {
  return (
    <main className="auth-page">
      <div className="auth-card">
        <Logo />
        <span className="section-kicker">ESPACE MEMBRE</span>
        <h1>Se connecter</h1>

        <label>Identifiant ou e-mail</label>
        <input placeholder="Votre identifiant" />

        <label>Mot de passe</label>
        <input type="password" placeholder="Votre mot de passe" />

        <button className="gold-button full-button">
          Se connecter
        </button>

        <button className="text-button" onClick={() => setPage("register")}>
          Créer un compte NSIKAY
        </button>
      </div>
    </main>
  );
}

function Register({ setPage }) {
  const [submitted, setSubmitted] = useState(false);

  if (submitted) {
    return (
      <main className="auth-page">
        <div className="auth-card success-card">
          <div className="success-icon">✓</div>
          <h1>Dossier envoyé</h1>
          <p>
            Votre demande de création de compte et votre dossier d'identité
            sont prêts pour vérification.
          </p>
          <p className="status-label">Vérification d'identité : EN ATTENTE</p>
          <button className="gold-button" onClick={() => setPage("home")}>
            Retour à l'accueil
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="auth-page">
      <div className="register-card">
        <Logo />
        <span className="section-kicker">CRÉATION DE COMPTE</span>
        <h1>Créer votre identité NSIKAY</h1>

        <div className="form-section">
          <h3>1. Informations personnelles</h3>

          <div className="form-grid">
            <input placeholder="Prénom" />
            <input placeholder="Nom" />
            <input placeholder="Nom d'utilisateur NSIKAY" />
            <input placeholder="E-mail" />
            <input placeholder="Téléphone" />
            <input placeholder="Pays" />
            <input type="date" />
            <input type="password" placeholder="Mot de passe" />
            <input type="password" placeholder="Confirmer le mot de passe" />
          </div>
        </div>

        <div className="form-section">
          <h3>2. Vérification d'identité</h3>
          <p className="form-help">
            Trois éléments sont prévus pour permettre la vérification de
            l'identité.
          </p>

          <div className="photo-grid">
            <div className="photo-upload">
              <div className="upload-icon">👤</div>
              <strong>Photo personnelle</strong>
              <span>Photo claire du visage</span>
              <button>Ajouter une photo</button>
            </div>

            <div className="photo-upload">
              <div className="upload-icon">🪪</div>
              <strong>Pièce d'identité</strong>
              <span>Document lisible</span>
              <button>Ajouter le document</button>
            </div>

            <div className="photo-upload">
              <div className="upload-icon">📷</div>
              <strong>Photo avec identité</strong>
              <span>Personne + document visible</span>
              <button>Ajouter une photo</button>
            </div>
          </div>
        </div>

        <label className="checkbox-row">
          <input type="checkbox" />
          <span>
            Je confirme l'exactitude des informations transmises.
          </span>
        </label>

        <button
          className="gold-button full-button"
          onClick={() => setSubmitted(true)}
        >
          Envoyer le dossier
        </button>

        <button className="text-button" onClick={() => setPage("login")}>
          J'ai déjà un compte
        </button>
      </div>
    </main>
  );
}

function App() {
  const [page, setPage] = useState("home");

  const renderPage = () => {
    if (page === "home") return <Home setPage={setPage} />;
    if (page === "tv") return <TvPage setPage={setPage} />;
    if (page === "advertising") return <AdvertisingPage />;
    if (page === "login") return <Login setPage={setPage} />;
    if (page === "register") return <Register setPage={setPage} />;
    if (page === "profile")
      return (
        <SimplePage
          title="Profil personnel"
          text="Votre identité et votre espace personnel NSIKAY."
        />
      );
    if (page === "events")
      return (
        <SimplePage
          title="Événements"
          text="Découvrez et présentez les événements de l'écosystème NSIKAY."
        />
      );
    if (page === "wenze")
      return (
        <SimplePage
          title="WENZE"
          text="L'espace commerce de l'écosystème NSIKAY."
        />
      );

    return <Home setPage={setPage} />;
  };

  return (
    <div className="app">
      <Header page={page} setPage={setPage} />
      {renderPage()}
      <Footer setPage={setPage} />
    </div>
  );
}

export default App;
