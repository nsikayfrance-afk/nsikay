import { useState } from "react";
import { useNavigate } from "react-router-dom";

const categories = [
  {
    id: "personnes",
    title: "Personnes",
    subtitle: "Identité et vie personnelle",
    icon: "👤",
    description:
      "Créez votre présence personnelle et développez votre identité au sein de l'écosystème NSIKAY.",
    types: [
      ["person", "Personne", "Profil personnel"],
      ["artist", "Artiste / Créateur", "Culture, art et création"],
    ],
  },
  {
    id: "professionnels",
    title: "Professionnels",
    subtitle: "Métiers et compétences",
    icon: "💼",
    description:
      "Présentez votre métier, vos compétences, vos services, votre expérience et vos activités professionnelles.",
    types: [
      ["professional", "Professionnel / Métier", "Métier et activité"],
      ["agent", "Agent / Expert", "Expertise et missions"],
    ],
  },
  {
    id: "organisations",
    title: "Organisations",
    subtitle: "Entreprises et structures",
    icon: "🏢",
    description:
      "Donnez une identité numérique officielle à votre entreprise, association ou organisation.",
    types: [
      ["company", "Entreprise", "Activité commerciale"],
      ["association", "Association / ONG", "Action associative"],
      ["institution", "Institution", "Institution publique ou privée"],
    ],
  },
  {
    id: "services",
    title: "Services spécialisés",
    subtitle: "Éducation, santé et finance",
    icon: "🏛️",
    description:
      "Créez des profils spécialisés pour les établissements et services qui structurent la société.",
    types: [
      ["bank", "Banque", "Services bancaires"],
      ["school", "École / Université", "Éducation"],
      ["training", "Centre de formation", "Formation professionnelle"],
      ["health", "Hôpital / Santé", "Santé et soins"],
    ],
  },
];

const allTypes = categories.flatMap((category) =>
  category.types.map(([id, title, subtitle]) => ({
    id,
    title,
    subtitle,
    category: category.title,
    icon:
      id === "person"
        ? "👤"
        : id === "professional"
        ? "💼"
        : id === "company"
        ? "🏢"
        : id === "bank"
        ? "🏦"
        : id === "school"
        ? "🏫"
        : id === "training"
        ? "🎓"
        : id === "health"
        ? "🏥"
        : id === "association"
        ? "🤝"
        : id === "institution"
        ? "🏛️"
        : id === "artist"
        ? "🎨"
        : "🧑‍💼",
  }))
);

export default function Profiles() {
  const navigate = useNavigate();
  const [selected, setSelected] = useState(null);
  const [search, setSearch] = useState("");

  const filteredTypes = allTypes.filter((item) => {
    const value = `${item.title} ${item.subtitle} ${item.category}`.toLowerCase();
    return value.includes(search.toLowerCase());
  });

  const handleSelect = (type) => {
    setSelected(type);
  };

  return (
    <div className="profiles-page">

      <header className="profiles-header">
        <div
          className="profiles-brand"
          onClick={() => navigate("/espace")}
        >
          <div className="profiles-brand-mark">N</div>
          <div>
            <strong>NSIKAY</strong>
            <span>Profils & identité</span>
          </div>
        </div>

        <div className="profiles-header-actions">
          <button onClick={() => navigate("/espace")}>
            ← Espace principal
          </button>

          <button
            className="profiles-header-primary"
            onClick={() => navigate("/mon-profil")}
          >
            Mon profil
          </button>
        </div>
      </header>

      <main>

        <section className="profiles-hero">
          <div className="profiles-hero-content">
            <span className="profiles-eyebrow">IDENTITÉ NSIKAY</span>

            <h1>
              Un profil pour
              <br />
              <strong>chaque identité</strong>
            </h1>

            <p>
              NSIKAY permet aux personnes, professionnels, entreprises,
              banques, établissements, associations et institutions de
              disposer d'une présence structurée dans un même écosystème.
            </p>

            <div className="profiles-search">
              <span>⌕</span>
              <input
                type="search"
                placeholder="Rechercher un type de profil..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
          </div>

          <div className="profiles-hero-symbol">
            <div className="profiles-symbol-ring ring-one"></div>
            <div className="profiles-symbol-ring ring-two"></div>
            <div className="profiles-symbol-center">N</div>
          </div>
        </section>

        <section className="profiles-section">

          <div className="profiles-section-title">
            <div>
              <span className="profiles-eyebrow">CHOISIR UNE IDENTITÉ</span>
              <h2>Types de profils</h2>
            </div>

            <p>
              Sélectionnez le profil correspondant à votre activité ou à
              votre organisation.
            </p>
          </div>

          {search ? (
            <div className="profiles-results">

              <div className="profiles-results-head">
                <strong>
                  {filteredTypes.length} résultat
                  {filteredTypes.length > 1 ? "s" : ""}
                </strong>
                <span>Recherche : {search}</span>
              </div>

              <div className="profiles-type-grid">
                {filteredTypes.map((type) => (
                  <button
                    key={type.id}
                    className={`profiles-type-card ${
                      selected?.id === type.id ? "selected" : ""
                    }`}
                    onClick={() => handleSelect(type)}
                  >
                    <span className="profiles-type-icon">{type.icon}</span>
                    <div>
                      <small>{type.category}</small>
                      <h3>{type.title}</h3>
                      <p>{type.subtitle}</p>
                    </div>
                    <b>→</b>
                  </button>
                ))}
              </div>

              {filteredTypes.length === 0 && (
                <div className="profiles-empty">
                  <span>🔎</span>
                  <h3>Aucun profil trouvé</h3>
                  <p>
                    Essayez une autre recherche.
                  </p>
                </div>
              )}

            </div>
          ) : (
            <div className="profiles-category-grid">

              {categories.map((category) => (
                <article
                  className="profiles-category"
                  key={category.id}
                >
                  <div className="profiles-category-head">
                    <span>{category.icon}</span>

                    <div>
                      <h3>{category.title}</h3>
                      <small>{category.subtitle}</small>
                    </div>
                  </div>

                  <p className="profiles-category-description">
                    {category.description}
                  </p>

                  <div className="profiles-category-types">
                    {category.types.map(([id, title, subtitle]) => {
                      const type = allTypes.find(
                        (item) => item.id === id
                      );

                      return (
                        <button
                          key={id}
                          className={`profiles-mini-card ${
                            selected?.id === id ? "selected" : ""
                          }`}
                          onClick={() => handleSelect(type)}
                        >
                          <span>{type.icon}</span>
                          <div>
                            <strong>{title}</strong>
                            <small>{subtitle}</small>
                          </div>
                          <b>→</b>
                        </button>
                      );
                    })}
                  </div>
                </article>
              ))}

            </div>
          )}

        </section>

        {selected && (
          <section className="profiles-selected">

            <div className="profiles-selected-icon">
              {selected.icon}
            </div>

            <div className="profiles-selected-content">
              <span className="profiles-eyebrow">
                PROFIL SÉLECTIONNÉ
              </span>

              <h2>{selected.title}</h2>

              <p>
                {selected.subtitle}. Ce profil pourra ensuite être complété
                avec ses informations, ses activités, ses services,
                ses certifications et ses moyens de contact.
              </p>
            </div>

            <div className="profiles-selected-actions">
              <button
                className="profiles-create-button"
                onClick={() =>
                  alert(
                    `Préparation du formulaire : ${selected.title}`
                  )
                }
              >
                Préparer ce profil →
              </button>

              <button
                className="profiles-cancel-button"
                onClick={() => setSelected(null)}
              >
                Annuler
              </button>
            </div>

          </section>
        )}

        <section className="profiles-principle">

          <div className="profiles-principle-number">
            3
          </div>

          <div>
            <span className="profiles-eyebrow">MODÈLE NSIKAY</span>

            <h2>
              Une identité.
              <br />
              Trois espaces.
            </h2>

            <div className="profiles-principle-list">
              <div>
                <span>01</span>
                <strong>Profil personnel</strong>
                <small>Votre identité</small>
              </div>

              <div>
                <span>02</span>
                <strong>Activités</strong>
                <small>Vos métiers et projets</small>
              </div>

              <div>
                <span>03</span>
                <strong>Engagement</strong>
                <small>Votre participation</small>
              </div>
            </div>
          </div>

        </section>

      </main>

      <footer className="profiles-footer">
        <div>
          <strong>NSIKAY</strong>
          <span>Écosystème international</span>
        </div>

        <div>
          <span>
            Profils • Activités • Engagement
          </span>
        </div>
      </footer>

    </div>
  );
}
