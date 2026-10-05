import React from "react";
import "../styles/nsikay-global.css";

const mainNavigation = [
  { label: "Accueil", href: "/" },
  { label: "Services Pro", href: "/services" },
  { label: "TV", href: "/tv" },
  { label: "Transports", href: "/transports" },
  { label: "Emploi", href: "/jobs" },
  { label: "WENZE", href: "/wenze" },
  { label: "Événements", href: "/events" },
  { label: "Actualités", href: "/editorial" },
];

const editorialRubrics = [
  "Économie",
  "Sport & Loisirs",
  "Culture & Art",
  "Technologie & Innovation",
  "Agriculture & Agronomie",
  "Social",
  "Religion & Histoire",
  "+18",
];

const services = [
  ["Services Pro", "Services, entreprises et professionnels.", "/services"],
  ["Emploi", "Offres d'emploi, missions et formations.", "/jobs"],
  ["WENZE", "Acheter et vendre dans l'écosystème NSIKAY.", "/wenze"],
  ["TV", "Programmes, émissions et contenus audiovisuels.", "/tv"],
  ["Transports", "Services liés à la mobilité et aux transports.", "/transports"],
  ["Événements", "Conférences, rencontres et activités.", "/events"],
];

const news = [
  ["NSIKAY", "Un écosystème numérique pour connecter les personnes, les activités et les engagements."],
  ["ÉCONOMIE", "Créer de nouvelles opportunités pour les entrepreneurs et les professionnels."],
  ["TECHNOLOGIE", "Une identité numérique au centre de l'expérience NSIKAY."],
];

function SectionTitle({ children, href, link = "Découvrir →" }) {
  return (
    <div className="ns-media-section-title">
      <h2>{children}</h2>
      <a href={href} className="ns-gold-link">{link}</a>
    </div>
  );
}

function Home() {
  return (
    <div className="ns-media-home">

      <div className="ns-kuba-watermark" aria-hidden="true" />

      <header className="ns-media-header">

        <div className="ns-media-topline">
          <span>NSIKAY — ÉCOSYSTÈME INTERNATIONAL</span>
          <span>AFRIQUE · FRANCE · MONDE</span>
        </div>

        <div className="ns-media-mainbar ns-container">

          <a href="/" className="ns-media-logo">
            NSIKAY
          </a>

          <nav className="ns-media-mainnav" aria-label="Navigation principale">
            {mainNavigation.map((item) => (
              <a key={item.label} href={item.href}>
                {item.label}
              </a>
            ))}
          </nav>

          <div className="ns-media-actions">
            <a className="ns-media-login" href="/login">
              Se connecter
            </a>
            <a className="ns-media-register" href="/register">
              Créer un compte
            </a>
          </div>

        </div>

        <div className="ns-media-rubrics">
          <div className="ns-media-rubrics-inner">
            {editorialRubrics.map((rubric) => (
              <a
                key={rubric}
                href={`/editorial?rubric=${encodeURIComponent(rubric)}`}
              >
                {rubric}
              </a>
            ))}
          </div>
        </div>

      </header>

      <main>

        <section className="ns-media-intro">
          <div className="ns-container">

            <div className="ns-media-kicker">
              L'ÉCOSYSTÈME NSIKAY
            </div>

            <h1>
              Une identité.
              <br />
              <span>Des activités.</span>
              <br />
              Un engagement.
            </h1>

            <p className="ns-media-category">
              Une plateforme internationale qui rassemble identité,
              services, emploi, commerce, médias, transports,
              événements et activités professionnelles.
            </p>

          </div>
        </section>

        <section className="ns-media-news">
          <div className="ns-container">

            <SectionTitle
              href="/editorial"
              link="Toutes les actualités →"
            >
              À LA UNE
            </SectionTitle>

            <div className="ns-media-lead-grid">

              <article className="ns-media-lead">

                <div className="ns-media-lead-image">
                  <div
                    style={{
                      height: "100%",
                      minHeight: "300px",
                      display: "flex",
                      alignItems: "flex-end",
                      padding: "25px",
                      background:
                        "linear-gradient(135deg, rgba(215,180,90,.28), rgba(0,0,0,.2))",
                    }}
                  >
                    <span
                      style={{
                        color: "#d7b45a",
                        fontWeight: 900,
                        letterSpacing: ".18em",
                      }}
                    >
                      NSIKAY
                    </span>
                  </div>
                </div>

                <div className="ns-media-lead-content">
                  <small>ÉCOSYSTÈME INTERNATIONAL</small>

                  <h3>
                    Un espace numérique pour développer
                    les personnes et les activités.
                  </h3>

                  <p>
                    NSIKAY rassemble dans un même environnement
                    l'identité numérique, les activités professionnelles,
                    l'emploi, le commerce, les médias, les transports
                    et les événements.
                  </p>
                </div>

              </article>

              <div className="ns-media-secondary">

                {news.map(([category, title]) => (
                  <article className="ns-media-story" key={title}>
                    <small>{category}</small>
                    <h3>{title}</h3>
                    <p>
                      Découvrez les informations et les services
                      disponibles dans l'écosystème NSIKAY.
                    </p>
                  </article>
                ))}

              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-employment">
          <div className="ns-container">

            <div className="ns-employment-editorial">

              <div className="ns-employment-main">

                <div className="ns-media-kicker">
                  OPPORTUNITÉS
                </div>

                <h2>
                  L'<span>emploi</span>
                  <br />
                  au cœur de NSIKAY.
                </h2>

                <p>
                  Trouvez des offres, développez vos compétences,
                  présentez votre profil professionnel et découvrez
                  de nouvelles opportunités.
                </p>

                <a href="/jobs" className="ns-gold-button">
                  Voir les offres d'emploi
                </a>

              </div>

              <div className="ns-employment-list">

                <article className="ns-media-story">
                  <small>EMPLOI</small>
                  <h3>Offres d'emploi et missions</h3>
                  <p>Consultez les opportunités disponibles.</p>
                </article>

                <article className="ns-media-story">
                  <small>FORMATION</small>
                  <h3>Développez vos compétences</h3>
                  <p>Accédez aux formations et ressources.</p>
                </article>

                <article className="ns-media-story">
                  <small>ENTREPRISES</small>
                  <h3>Recrutez vos futurs talents</h3>
                  <p>Présentez vos besoins professionnels.</p>
                </article>

              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-categories">
          <div className="ns-container">

            <SectionTitle href="/services" link="Tous les services →">
              NOS SERVICES
            </SectionTitle>

            <div className="ns-editorial-grid">

              {services.map(([title, text, href]) => (
                <a
                  key={title}
                  href={href}
                  className="ns-media-story"
                >
                  <small>NSIKAY</small>
                  <h3>{title}</h3>
                  <p>{text}</p>
                  <span className="ns-gold-link">
                    Découvrir →
                  </span>
                </a>
              ))}

            </div>

          </div>
        </section>

        <section className="ns-media-commerce">
          <div className="ns-container">

            <div className="ns-commerce-layout">

              <div>

                <div className="ns-media-kicker">
                  À PROPOS DE NSIKAY
                </div>

                <h2>
                  Une initiative portée depuis la France
                  vers l'international.
                </h2>

                <p>
                  NSIKAY est une association déclarée en France,
                  conçue pour favoriser la création d'activités,
                  le développement des compétences, la culture,
                  l'autonomie et l'inclusion dans l'écosystème
                  numérique.
                </p>

                <p>
                  <strong style={{ color: "#d7b45a" }}>
                    ASSOCIATION DÉCLARÉE EN FRANCE — LOI 1901
                  </strong>
                </p>

                <p>
                  RNA : <strong>W442031317</strong>
                  <br />
                  SIREN : <strong>995 089 711</strong>
                  <br />
                  SIRET : <strong>995 089 711 00015</strong>
                  <br />
                  Création : <strong>6 décembre 2025</strong>
                  <br />
                  Publication JOAFE : <strong>16 décembre 2025</strong>
                </p>

              </div>

              <div className="ns-media-story">

                <small>NOTRE MISSION</small>

                <h3>
                  Une plateforme au service des personnes,
                  des activités et de l'engagement.
                </h3>

                <p>
                  Identité numérique, économie, culture,
                  technologie, agriculture, sport, médias,
                  emploi, formation, commerce et services :
                  NSIKAY rassemble ces dimensions dans un
                  même environnement.
                </p>

              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-commerce">
          <div className="ns-container">

            <SectionTitle href="/wenze" link="Accéder à WENZE →">
              WENZE
            </SectionTitle>

            <div className="ns-commerce-layout">

              <div>
                <h2>
                  Commerce.
                  <br />
                  <span style={{ color: "#d7b45a" }}>
                    Simplement.
                  </span>
                </h2>

                <p>
                  WENZE est l'espace commercial permanent de NSIKAY
                  pour acheter et vendre des produits et services.
                </p>

                <a href="/wenze" className="ns-gold-button">
                  Découvrir WENZE
                </a>
              </div>

              <div className="ns-media-story">
                <small>COMMERCE NSIKAY</small>
                <h3>
                  Une vitrine pour les entreprises,
                  commerçants et créateurs.
                </h3>
                <p>
                  Les activités commerciales sont regroupées
                  dans l'écosystème WENZE.
                </p>
              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-events">
          <div className="ns-container">

            <SectionTitle href="/events" link="Tous les événements →">
              ÉVÉNEMENTS
            </SectionTitle>

            <div className="ns-event-editorial-grid">

              <article className="ns-media-story">
                <small>CONFÉRENCES</small>
                <h3>Rencontres professionnelles</h3>
                <p>
                  Conférences, débats et rencontres autour de
                  l'emploi, de la culture et de l'innovation.
                </p>
              </article>

              <article className="ns-media-story">
                <small>CULTURE</small>
                <h3>Culture et patrimoine</h3>
                <p>
                  Découvrez les événements culturels et artistiques.
                </p>
              </article>

              <article className="ns-media-story">
                <small>COMMUNAUTÉ</small>
                <h3>Participez à la vie NSIKAY</h3>
                <p>
                  Retrouvez les activités et rendez-vous.
                </p>
              </article>

            </div>

          </div>
        </section>

        <section className="ns-media-tv">
          <div className="ns-container">

            <SectionTitle href="/tv" link="Voir NSIKAY TV →">
              NSIKAY TV
            </SectionTitle>

            <div className="ns-tv-layout">

              <article className="ns-media-lead">

                <div className="ns-media-lead-image">
                  <div
                    style={{
                      minHeight: "300px",
                      height: "100%",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "60px",
                      fontWeight: 900,
                      color: "#d7b45a",
                    }}
                  >
                    NSIKAY TV
                  </div>
                </div>

                <div className="ns-media-lead-content">
                  <small>
                    DIRECT · PROGRAMMES · MÉDIAS
                  </small>

                  <h3>
                    L'information, la culture et les histoires
                    de nos communautés.
                  </h3>

                  <a href="/tv" className="ns-gold-link">
                    Accéder à NSIKAY TV →
                  </a>
                </div>

              </article>

              <div>

                <article className="ns-media-story">
                  <small>PROGRAMMES</small>
                  <h3>Émissions et contenus originaux</h3>
                </article>

                <article className="ns-media-story">
                  <small>ACTUALITÉS</small>
                  <h3>Information et analyses</h3>
                </article>

                <article className="ns-media-story">
                  <small>CULTURE</small>
                  <h3>Art, patrimoine et création</h3>
                </article>

              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-categories">
          <div className="ns-container">

            <SectionTitle
              href="/transports"
              link="Découvrir les transports →"
            >
              TRANSPORTS
            </SectionTitle>

            <div className="ns-commerce-layout">

              <div>

                <div className="ns-media-kicker">
                  MOBILITÉ
                </div>

                <h2>
                  Connecter les personnes
                  <br />
                  <span style={{ color: "#d7b45a" }}>
                    aux territoires.
                  </span>
                </h2>

                <p>
                  NSIKAY intègre les services liés aux transports
                  et à la mobilité dans son écosystème.
                </p>

              </div>

              <div className="ns-media-story">
                <small>TRANSPORTS</small>

                <h3>
                  Une nouvelle porte d'entrée vers les services
                  de mobilité.
                </h3>

                <p>
                  Retrouvez les informations et fonctionnalités
                  de transport directement dans NSIKAY.
                </p>
              </div>

            </div>

          </div>
        </section>

        <section className="ns-media-advertising">
          <div className="ns-container">
            <div className="ns-ad-editorial">
              ESPACE PUBLICITAIRE NSIKAY
            </div>
          </div>
        </section>

      </main>

      <footer className="ns-media-footer">

        <div className="ns-container">

          <div className="ns-footer-top">

            <div>

              <div className="ns-media-logo">
                NSIKAY
              </div>

              <p>
                Une identité. Des activités. Un engagement.
              </p>

              <p style={{ color: "#777" }}>
                Association déclarée en France — Loi 1901
                <br />
                RNA W442031317
                <br />
                SIREN 995 089 711
                <br />
                SIRET 995 089 711 00015
              </p>

            </div>

            <div className="ns-footer-links">

              <a href="/services">Services Pro</a>
              <a href="/tv">TV</a>
              <a href="/transports">Transports</a>
              <a href="/jobs">Emploi</a>
              <a href="/wenze">WENZE</a>
              <a href="/events">Événements</a>
              <a href="/editorial">Actualités</a>
              <a href="/about">À propos</a>
              <a href="/contact">Contact</a>

            </div>

          </div>

          <div className="ns-footer-bottom">
            © {new Date().getFullYear()} NSIKAY —
            Association déclarée en France.
            Tous droits réservés.
          </div>

        </div>

      </footer>

    </div>
  );
}

export default Home;
