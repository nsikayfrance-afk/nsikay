import React from "react";
import { Link, useParams } from "react-router-dom";
import "../styles/nsikay-editorial.css";

const categories = [
  ["economie", "Économie", "💼", "Économie, entreprises, emploi et développement."],
  ["sport-loisirs", "Sport & Loisirs", "🏆", "Sport, compétitions, loisirs et talents."],
  ["culture-art", "Culture & Art", "🎨", "Culture, musique, patrimoine et création artistique."],
  ["technologie-innovation", "Technologie & Innovation", "💡", "Technologie, numérique et innovation."],
  ["agriculture-agronomie", "Agriculture & Agronomie", "🌱", "Agriculture, agronomie et développement rural."],
  ["social", "Social", "🤝", "Solidarité, éducation, santé et jeunesse."],
  ["religion-histoire", "Religion & Histoire", "📚", "Histoire, patrimoine, traditions et mémoire."],
  ["plus-18", "+18", "🔞", "Espace réservé au public adulte."]
];

export default function Editorial() {
  const { category } = useParams();
  const active = categories.find((item) => item[0] === category);

  return (
    <main className="editorial-page">
      <header className="editorial-hero">
        <div className="editorial-brand">
          <span className="editorial-logo">N</span>
          <span>NSIKAY</span>
        </div>

        <span className="editorial-eyebrow">UNIVERS ÉDITORIAL</span>

        <h1>
          {active ? `${active[2]} ${active[1]}` : "Les grands univers NSIKAY."}
        </h1>

        <p>
          {active
            ? active[3]
            : "Information, culture, économie, innovation, agriculture, sport et société."}
        </p>
      </header>

      <nav className="editorial-nav">
        <Link to="/editorial">Toutes les rubriques</Link>
        <Link to="/events">Événements</Link>
        <Link to="/tv">NSIKAY TV</Link>
        <Link to="/publicite">Publicité</Link>
      </nav>

      {!active ? (
        <section className="editorial-grid">
          {categories.map(([slug, title, icon, description]) => (
            <Link
              key={slug}
              to={`/editorial/${slug}`}
              className="editorial-card editorial-category"
            >
              <span className="editorial-icon">{icon}</span>
              <div>
                <small>UNIVERS</small>
                <h2>{title}</h2>
                <p>{description}</p>
              </div>
              <strong>→</strong>
            </Link>
          ))}
        </section>
      ) : (
        <section className="editorial-content">
          <div className="editorial-heading">
            <small>PUBLICATIONS</small>
            <h2>Actualités {active[1]}</h2>
          </div>

          <div className="editorial-grid">
            {[1, 2, 3].map((item) => (
              <article className="editorial-card" key={item}>
                <div className="editorial-image">{active[2]}</div>
                <div className="editorial-card-body">
                  <small>{active[1]}</small>
                  <h3>Actualité NSIKAY — publication {item}</h3>
                  <p>
                    Cet espace accueillera les articles, reportages,
                    analyses et contenus publiés dans cette rubrique.
                  </p>
                  <button type="button">Lire →</button>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
