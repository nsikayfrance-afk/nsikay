import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <main className="ns-kuba-watermark">

      <section className="ns-hero">
        <div className="ns-container ns-hero-content">
          <div className="ns-section-kicker">
            NSIKAY — ÉCOSYSTÈME INTERNATIONAL
          </div>

          <h1 className="ns-hero-title">
            Une identité.
            <br />
            Des activités.
            <br />
            <span>Un engagement.</span>
          </h1>

          <p className="ns-hero-text">
            Une plateforme internationale pour connecter les personnes,
            les entreprises, les opportunités, la culture et le commerce.
          </p>

          <div className="ns-hero-actions">
            <Link to="/inscription" className="ns-btn ns-btn-gold">
              Créer mon compte
            </Link>

            <Link to="/connexion" className="ns-btn ns-btn-dark">
              Se connecter
            </Link>
          </div>
        </div>
      </section>

      <section className="ns-section ns-employment">
        <div className="ns-container">

          <div className="ns-section-header">
            <div>
              <div className="ns-section-kicker">
                EMPLOI & OPPORTUNITÉS
              </div>

              <h2 className="ns-section-title">
                Trouver une opportunité. Créer son avenir.
              </h2>
            </div>

            <Link to="/jobs" className="ns-btn ns-btn-gold">
              Voir les offres
            </Link>
          </div>

          <div className="ns-job-grid">

            <article className="ns-job-card">
              <span className="ns-badge">EMPLOI</span>
              <h3>Offres d'emploi</h3>
              <p>
                Découvrez les opportunités proposées par les entreprises
                et organisations présentes sur NSIKAY.
              </p>
              <Link to="/jobs">
                Consulter les offres →
              </Link>
            </article>

            <article className="ns-job-card">
              <span className="ns-badge">ENTREPRISES</span>
              <h3>Recrutement</h3>
              <p>
                Les entreprises peuvent publier leurs besoins et
                développer leurs équipes.
              </p>
              <Link to="/companies">
                Recruter sur NSIKAY →
              </Link>
            </article>

            <article className="ns-job-card">
              <span className="ns-badge">FORMATION</span>
              <h3>Stages & formations</h3>
              <p>
                Accédez aux stages, formations et programmes de
                développement des compétences.
              </p>
              <Link to="/training">
                Découvrir les programmes →
              </Link>
            </article>

            <article className="ns-job-card">
              <span className="ns-badge">MISSIONS</span>
              <h3>Missions & opportunités</h3>
              <p>
                Trouvez des missions, projets et collaborations adaptés
                à vos compétences.
              </p>
              <Link to="/opportunities">
                Voir les opportunités →
              </Link>
            </article>

          </div>
        </div>
      </section>

      <section className="ns-section ns-section-dark">
        <div className="ns-container">

          <div className="ns-section-header">
            <div>
              <div className="ns-section-kicker">
                ACTUALITÉS
              </div>

              <h2 className="ns-section-title">
                À la une
              </h2>
            </div>

            <Link to="/editorial" className="ns-btn ns-btn-dark">
              Toutes les actualités
            </Link>
          </div>

          <div className="ns-news-grid">

            <article className="ns-news-main">
              <div className="ns-news-main-content">

                <span className="ns-badge">
                  ÉCONOMIE
                </span>

                <h3>
                  L'Afrique au cœur des nouvelles opportunités
                  économiques et numériques
                </h3>

                <p>
                  Retrouvez les analyses, initiatives et informations
                  qui façonnent les économies africaines et internationales.
                </p>

                <Link to="/editorial/economie">
                  Lire l'article →
                </Link>

              </div>
            </article>

            <div className="ns-news-side">

              <article className="ns-news-card">
                <span className="ns-badge">
                  CULTURE & ART
                </span>

                <h3>
                  Culture, patrimoine et création
                </h3>

                <p>
                  Découvrez les artistes, patrimoines et initiatives
                  culturelles.
                </p>

                <Link to="/editorial/culture">
                  Lire →
                </Link>
              </article>

              <article className="ns-news-card">
                <span className="ns-badge">
                  TECHNOLOGIE
                </span>

                <h3>
                  Innovation & numérique
                </h3>

                <p>
                  Les technologies qui transforment les sociétés.
                </p>

                <Link to="/editorial/technologie">
                  Lire →
                </Link>
              </article>

            </div>
          </div>
        </div>
      </section>

      <section className="ns-section">
        <div className="ns-container">

          <div className="ns-section-header">
            <div>
              <div className="ns-section-kicker">
                PORTAIL ÉDITORIAL
              </div>

              <h2 className="ns-section-title">
                Nos rubriques
              </h2>
            </div>
          </div>

          <div className="ns-category-bar">

            <Link to="/editorial/economie" className="ns-category">
              Économie
            </Link>

            <Link to="/editorial/sport" className="ns-category">
              Sport & Loisirs
            </Link>

            <Link to="/editorial/culture" className="ns-category">
              Culture & Art
            </Link>

            <Link to="/editorial/technologie" className="ns-category">
              Technologie & Innovation
            </Link>

            <Link to="/editorial/agriculture" className="ns-category">
              Agriculture & Agronomie
            </Link>

            <Link to="/editorial/social" className="ns-category">
              Social
            </Link>

            <Link to="/editorial/religion" className="ns-category">
              Religion & Histoire
            </Link>

            <Link to="/editorial/adulte" className="ns-category">
              +18
            </Link>

          </div>
        </div>
      </section>

      <section className="ns-section ns-wenze">
        <div className="ns-container">

          <div className="ns-wenze-card">

            <div>
              <div className="ns-section-kicker">
                COMMERCE
              </div>

              <h2 className="ns-section-title">
                WENZE
              </h2>

              <p>
                Achetez et vendez dans l'écosystème commercial NSIKAY.
              </p>
            </div>

            <Link to="/wenze" className="ns-btn ns-btn-gold">
              Entrer dans WENZE
            </Link>

          </div>
        </div>
      </section>

      <section className="ns-section ns-section-dark">
        <div className="ns-container">

          <div className="ns-section-header">
            <div>
              <div className="ns-section-kicker">
                AGENDA
              </div>

              <h2 className="ns-section-title">
                Événements
              </h2>
            </div>

            <Link to="/events" className="ns-btn ns-btn-gold">
              Voir les événements
            </Link>
          </div>

          <div className="ns-events-grid">

            <article className="ns-event-card">
              <span className="ns-badge">
                INTERNATIONAL
              </span>

              <h3>
                Conférences & rencontres
              </h3>

              <p>
                Rencontres professionnelles, culturelles et
                institutionnelles.
              </p>
            </article>

            <article className="ns-event-card">
              <span className="ns-badge">
                CULTURE
              </span>

              <h3>
                Culture & spectacles
              </h3>

              <p>
                Découvrez les événements culturels et artistiques.
              </p>
            </article>

            <article className="ns-event-card">
              <span className="ns-badge">
                SPORT
              </span>

              <h3>
                Sport & loisirs
              </h3>

              <p>
                Retrouvez les compétitions et activités sportives.
              </p>
            </article>

          </div>
        </div>
      </section>

      <section className="ns-section">
        <div className="ns-container">

          <div className="ns-ad-slot">
            <span>PUBLICITÉ</span>

            <strong>
              Votre visibilité sur l'écosystème NSIKAY
            </strong>
          </div>

        </div>
      </section>

      <footer className="ns-footer">
        <div className="ns-container">

          <div className="ns-footer-grid">

            <div>
              <div className="ns-logo">
                NSIKAY
              </div>

              <p>
                Une identité. Des activités. Un engagement.
              </p>
            </div>

            <div>
              <strong>
                Plateforme
              </strong>

              <Link to="/jobs">
                Emploi
              </Link>

              <Link to="/wenze">
                WENZE
              </Link>

              <Link to="/events">
                Événements
              </Link>
            </div>

            <div>
              <strong>
                Éditorial
              </strong>

              <Link to="/editorial">
                Actualités
              </Link>

              <Link to="/editorial/culture">
                Culture
              </Link>

              <Link to="/editorial/technologie">
                Technologie
              </Link>
            </div>

          </div>

          <div className="ns-divider" />

          <p>
            © {new Date().getFullYear()} NSIKAY — Tous droits réservés.
          </p>

        </div>
      </footer>

    </main>
  );
}