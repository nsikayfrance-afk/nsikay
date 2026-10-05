import React from "react";
import { Link } from "react-router-dom";

const news = [
  {
    category: "ÉCONOMIE",
    title: "Les nouvelles dynamiques économiques qui transforment l’Afrique",
    text: "Analyses, initiatives, entreprises et opportunités au cœur de l’actualité économique.",
    path: "/editorial/economie",
    featured: true,
  },
  {
    category: "CULTURE",
    title: "Patrimoine, création et nouvelles générations",
    text: "La culture africaine entre héritage et création contemporaine.",
    path: "/editorial/culture",
  },
  {
    category: "TECHNOLOGIE",
    title: "Le numérique accélère les transformations",
    text: "Innovation, intelligence numérique et nouveaux usages.",
    path: "/editorial/technologie",
  },
  {
    category: "AGRICULTURE",
    title: "Agriculture et souveraineté alimentaire",
    text: "Initiatives, production et innovation agricole.",
    path: "/editorial/agriculture",
  },
];

const categories = [
  ["Économie", "/editorial/economie"],
  ["Sport & Loisirs", "/editorial/sport"],
  ["Culture & Art", "/editorial/culture"],
  ["Technologie & Innovation", "/editorial/technologie"],
  ["Agriculture & Agronomie", "/editorial/agriculture"],
  ["Social", "/editorial/social"],
  ["Religion & Histoire", "/editorial/religion"],
  ["+18", "/editorial/adulte"],
];

export default function Home() {
  return (
    <main className="ns-media-home">
      <div className="ns-kuba-watermark" aria-hidden="true" />

      <header className="ns-media-header">
        <div className="ns-media-topline">
          <div className="ns-container ns-media-topline-inner">
            <span>NSIKAY — ÉCOSYSTÈME INTERNATIONAL</span>
            <span>INTERNATIONAL · AFRIQUE · MONDE</span>
          </div>
        </div>

        <div className="ns-container ns-media-mainbar">
          <Link to="/" className="ns-media-logo">NSIKAY</Link>

          <nav className="ns-media-mainnav">
            <Link to="/editorial">Actualités</Link>
            <Link to="/jobs">Emploi</Link>
            <Link to="/wenze">WENZE</Link>
            <Link to="/events">Événements</Link>
            <Link to="/tv">NSIKAY TV</Link>
          </nav>

          <div className="ns-media-actions">
            <Link to="/connexion" className="ns-media-login">Connexion</Link>
            <Link to="/inscription" className="ns-media-register">Inscription</Link>
          </div>
        </div>

        <div className="ns-media-rubrics">
          <div className="ns-container ns-media-rubrics-inner">
            {categories.map(([label, path]) => (
              <Link key={label} to={path}>{label}</Link>
            ))}
          </div>
        </div>
      </header>

      <section className="ns-media-intro">
        <div className="ns-container">
          <div className="ns-media-kicker">
            UNE PLATEFORME · UNE INFORMATION · DES OPPORTUNITÉS
          </div>

          <h1>
            Une identité.
            <br />
            Des activités.
            <br />
            <span>Un engagement.</span>
          </h1>

          <p>
            NSIKAY rassemble information, emploi, commerce, culture,
            événements, technologie et engagement dans un même écosystème.
          </p>
        </div>
      </section>

      <section className="ns-media-news">
        <div className="ns-container">
          <div className="ns-media-section-title">
            <span>À LA UNE</span>
            <Link to="/editorial">Toute l’actualité →</Link>
          </div>

          <div className="ns-media-lead-grid">
            <article className="ns-media-lead">
              <div className="ns-media-lead-image">
                <span>NSIKAY</span>
              </div>

              <div className="ns-media-lead-content">
                <span className="ns-media-category">{news[0].category}</span>
                <h2>{news[0].title}</h2>
                <p>{news[0].text}</p>
                <Link to={news[0].path}>Lire la suite →</Link>
              </div>
            </article>

            <div className="ns-media-secondary">
              {news.slice(1, 3).map((item) => (
                <article className="ns-media-story" key={item.title}>
                  <div className="ns-media-story-image">
                    <span>{item.category}</span>
                  </div>

                  <div>
                    <span className="ns-media-category">{item.category}</span>
                    <h3>{item.title}</h3>
                    <p>{item.text}</p>
                    <Link to={item.path}>Lire →</Link>
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="ns-media-news-strip">
            {news.slice(3).map((item) => (
              <article key={item.title}>
                <span>{item.category}</span>
                <h3>{item.title}</h3>
                <Link to={item.path}>Lire →</Link>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="ns-media-employment">
        <div className="ns-container">
          <div className="ns-media-section-title">
            <span>EMPLOI & OPPORTUNITÉS</span>
            <Link to="/jobs">Toutes les offres →</Link>
          </div>

          <div className="ns-employment-editorial">
            <div className="ns-employment-main">
              <span className="ns-media-category">EMPLOI</span>

              <h2>
                Les opportunités professionnelles
                au cœur de l’écosystème NSIKAY
              </h2>

              <p>
                Consultez les offres d’emploi, les recrutements,
                les stages, les formations et les missions disponibles
                sur la plateforme.
              </p>

              <Link to="/jobs" className="ns-gold-link">
                Découvrir les offres d’emploi →
              </Link>
            </div>

            <div className="ns-employment-list">
              <article>
                <span>OFFRES</span>
                <h3>Emplois disponibles</h3>
                <p>Découvrez les opportunités publiées.</p>
                <Link to="/jobs">Voir les offres →</Link>
              </article>

              <article>
                <span>ENTREPRISES</span>
                <h3>Recruter sur NSIKAY</h3>
                <p>Publiez vos besoins et trouvez vos talents.</p>
                <Link to="/companies">Pour les entreprises →</Link>
              </article>

              <article>
                <span>COMPÉTENCES</span>
                <h3>Stages & formations</h3>
                <p>Développez vos compétences et votre parcours.</p>
                <Link to="/training">Découvrir →</Link>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section className="ns-media-categories">
        <div className="ns-container">
          <div className="ns-media-section-title">
            <span>NOS RUBRIQUES</span>
          </div>

          <div className="ns-editorial-grid">
            {categories.map(([label, path], index) => (
              <Link key={label} to={path} className={index === 0 ? "active" : ""}>
                <small>0{index + 1}</small>
                <strong>{label}</strong>
                <span>→</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="ns-media-commerce">
        <div className="ns-container">
          <div className="ns-commerce-layout">
            <div>
              <span className="ns-media-category">COMMERCE</span>
              <h2>WENZE</h2>
              <p>
                Acheter, vendre et développer son activité
                dans l’écosystème commercial NSIKAY.
              </p>
            </div>

            <Link to="/wenze" className="ns-gold-button">
              Entrer dans WENZE →
            </Link>
          </div>
        </div>
      </section>

      <section className="ns-media-events">
        <div className="ns-container">
          <div className="ns-media-section-title">
            <span>ÉVÉNEMENTS</span>
            <Link to="/events">Tout l’agenda →</Link>
          </div>

          <div className="ns-event-editorial-grid">
            <article>
              <span>01 · INTERNATIONAL</span>
              <h3>Conférences & rencontres</h3>
              <p>Rencontres professionnelles, culturelles et institutionnelles.</p>
              <Link to="/events">Découvrir →</Link>
            </article>

            <article>
              <span>02 · CULTURE</span>
              <h3>Culture & spectacles</h3>
              <p>Artistes, patrimoine, spectacles et création.</p>
              <Link to="/events">Découvrir →</Link>
            </article>

            <article>
              <span>03 · SPORT</span>
              <h3>Sport & loisirs</h3>
              <p>Compétitions, activités et grands rendez-vous.</p>
              <Link to="/events">Découvrir →</Link>
            </article>
          </div>
        </div>
      </section>

      <section className="ns-media-tv">
        <div className="ns-container ns-tv-layout">
          <div>
            <span className="ns-media-category">NSIKAY TV</span>
            <h2>L’information en images.</h2>
            <p>
              Retrouvez les programmes, émissions, directs
              et contenus audiovisuels de NSIKAY.
            </p>
          </div>

          <Link to="/tv" className="ns-gold-button">
            Regarder NSIKAY TV →
          </Link>
        </div>
      </section>

      <section className="ns-media-advertising">
        <div className="ns-container">
          <div className="ns-ad-editorial">
            <span>PUBLICITÉ</span>
            <strong>Votre visibilité auprès de l’écosystème NSIKAY</strong>
            <Link to="/advertising">Découvrir les solutions →</Link>
          </div>
        </div>
      </section>

      <footer className="ns-media-footer">
        <div className="ns-container">
          <div className="ns-footer-top">
            <div>
              <Link to="/" className="ns-media-logo">NSIKAY</Link>
              <p>Une identité. Des activités. Un engagement.</p>
            </div>

            <div className="ns-footer-links">
              <Link to="/editorial">Actualités</Link>
              <Link to="/jobs">Emploi</Link>
              <Link to="/wenze">WENZE</Link>
              <Link to="/events">Événements</Link>
              <Link to="/tv">NSIKAY TV</Link>
              <Link to="/connexion">Connexion</Link>
            </div>
          </div>

          <div className="ns-footer-bottom">
            <span>© {new Date().getFullYear()} NSIKAY</span>
            <span>Écosystème international</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
