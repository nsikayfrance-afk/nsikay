import { useEffect, useMemo, useState } from "react";
import { api } from "../services/api";

const profileCategories = [
  {
    title: "Personnes",
    items: [
      ["person", "Personne", "Profil personnel NSIKAY"],
      ["artist", "Artiste / Créateur", "Œuvres, création et événements"],
    ],
  },
  {
    title: "Professionnels",
    items: [
      ["professional", "Professionnel / Métier", "Compétences et services"],
      ["agent", "Agent / Expert", "Expertise, missions et certification"],
    ],
  },
  {
    title: "Organisations",
    items: [
      ["company", "Entreprise", "Activités, services et projets"],
      ["association", "Association / ONG", "Missions et actions"],
      ["institution", "Institution", "Services et territoire"],
    ],
  },
  {
    title: "Services spécialisés",
    items: [
      ["bank", "Banque", "Services bancaires et pays"],
      ["school", "École / Université", "Établissements et formations"],
      ["training", "Centre de formation", "Programmes et certifications"],
      ["health", "Hôpital / Santé", "Spécialités et professionnels"],
    ],
  },
];

const emptyForm = {
  profile_type: "person",
  display_name: "",
  legal_name: "",
  professional_title: "",
  description: "",
  country: "",
  city: "",
  phone: "",
  website: "",
  sector: "",
  visibility: "public",
  status: "draft",
  is_primary: false,
};

export default function Profiles() {
  const [profiles, setProfiles] = useState([]);
  const [selectedType, setSelectedType] = useState("person");
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadProfiles = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await api.profiles();

      setProfiles(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      setError(err.message || "Erreur lors du chargement des profils.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfiles();
  }, []);

  const filteredProfiles = useMemo(() => {
    const term = search.trim().toLowerCase();

    return profiles.filter((profile) => {
      const matchesType =
        !selectedType ||
        profile.profile_type === selectedType;

      const text = [
        profile.display_name,
        profile.legal_name,
        profile.professional_title,
        profile.description,
        profile.country,
        profile.city,
        profile.sector,
      ]
        .join(" ")
        .toLowerCase();

      const matchesSearch =
        !term || text.includes(term);

      return matchesType && matchesSearch;
    });
  }, [profiles, selectedType, search]);

  const openCreate = (type = "person") => {
    setEditingId(null);
    setSelectedType(type);

    setForm({
      ...emptyForm,
      profile_type: type,
      is_primary:
        type === "person" &&
        profiles.filter((p) => p.profile_type === "person").length === 0,
    });

    setMessage("");
    setError("");
    setShowForm(true);
  };

  const openEdit = (profile) => {
    setEditingId(profile.id);
    setSelectedType(profile.profile_type);

    setForm({
      profile_type: profile.profile_type || "person",
      display_name: profile.display_name || "",
      legal_name: profile.legal_name || "",
      professional_title: profile.professional_title || "",
      description: profile.description || "",
      country: profile.country || "",
      city: profile.city || "",
      phone: profile.phone || "",
      website: profile.website || "",
      sector: profile.sector || "",
      visibility: profile.visibility || "public",
      status: profile.status || "draft",
      is_primary: Boolean(profile.is_primary),
    });

    setMessage("");
    setError("");
    setShowForm(true);
  };

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setSaving(true);
    setMessage("");
    setError("");

    try {
      let result;

      if (editingId) {
        result = await api.updateProfileItem(
          editingId,
          form
        );

        setProfiles((current) =>
          current.map((item) =>
            item.id === result.id ? result : item
          )
        );

        setMessage("Profil modifié avec succès.");
      } else {
        result = await api.createProfile(form);

        setProfiles((current) => [
          result,
          ...current,
        ]);

        setMessage("Profil créé avec succès.");
      }

      setShowForm(false);
      setEditingId(null);

    } catch (err) {
      setError(
        err.message ||
        "Une erreur est survenue."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (profile) => {
    const confirmed = window.confirm(
      `Supprimer le profil « ${profile.display_name} » ?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await api.deleteProfileItem(profile.id);

      setProfiles((current) =>
        current.filter((item) => item.id !== profile.id)
      );

      setMessage("Profil supprimé.");
      setError("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="profiles-page">

      <section className="profiles-hero">
        <div>
          <span className="profiles-kicker">
            NSIKAY · IDENTITÉ UNIFIÉE
          </span>

          <h1>
            Vos profils dans NSIKAY
          </h1>

          <p>
            Un compte NSIKAY peut porter plusieurs profils
            personnels, professionnels et institutionnels.
          </p>
        </div>

        <button
          className="profiles-primary-button"
          onClick={() => openCreate("person")}
        >
          + Créer mon profil
        </button>
      </section>

      {message && (
        <div className="profiles-success">
          {message}
        </div>
      )}

      {error && (
        <div className="profiles-error">
          {error}
        </div>
      )}

      <section className="profiles-search">
        <input
          type="search"
          placeholder="Rechercher dans mes profils..."
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
        />
      </section>

      <section className="profiles-layout">

        <aside className="profiles-sidebar">

          <h2>
            Types de profils
          </h2>

          <button
            className={
              selectedType === ""
                ? "profile-type active"
                : "profile-type"
            }
            onClick={() => setSelectedType("")}
          >
            <strong>Tous</strong>
            <span>{profiles.length}</span>
          </button>

          {profileCategories.map((category) => (
            <div
              key={category.title}
              className="profile-category"
            >
              <h3>{category.title}</h3>

              {category.items.map(
                ([type, label, description]) => (
                  <button
                    key={type}
                    className={
                      selectedType === type
                        ? "profile-type active"
                        : "profile-type"
                    }
                    onClick={() =>
                      setSelectedType(type)
                    }
                  >
                    <span>
                      <strong>{label}</strong>
                      <small>{description}</small>
                    </span>

                    <span>
                      {
                        profiles.filter(
                          (profile) =>
                            profile.profile_type === type
                        ).length
                      }
                    </span>
                  </button>
                )
              )}
            </div>
          ))}
        </aside>

        <div className="profiles-content">

          <div className="profiles-content-header">
            <div>
              <span className="profiles-kicker">
                MES PROFILS
              </span>

              <h2>
                Profils enregistrés
              </h2>
            </div>

            <button
              className="profiles-secondary-button"
              onClick={() => openCreate(selectedType || "person")}
            >
              + Nouveau profil
            </button>
          </div>

          {loading ? (
            <div className="profiles-empty">
              Chargement des profils...
            </div>
          ) : filteredProfiles.length === 0 ? (
            <div className="profiles-empty">
              <div className="profiles-empty-icon">
                +
              </div>

              <h3>
                Aucun profil pour le moment
              </h3>

              <p>
                Commencez par créer votre profil personnel.
              </p>

              <button
                className="profiles-primary-button"
                onClick={() => openCreate("person")}
              >
                Créer mon profil personnel
              </button>
            </div>
          ) : (
            <div className="profiles-grid">
              {filteredProfiles.map((profile) => (
                <article
                  key={profile.id}
                  className="profile-card-real"
                >
                  <div className="profile-card-top">
                    <span className="profile-badge">
                      {profile.profile_type_label}
                    </span>

                    {profile.is_primary && (
                      <span className="profile-primary">
                        Principal
                      </span>
                    )}
                  </div>

                  <h3>
                    {profile.display_name}
                  </h3>

                  {profile.professional_title && (
                    <p className="profile-title">
                      {profile.professional_title}
                    </p>
                  )}

                  <p className="profile-description">
                    {profile.description ||
                      "Aucune description renseignée."}
                  </p>

                  <div className="profile-meta">
                    {profile.country && (
                      <span>
                        🌍 {profile.country}
                      </span>
                    )}

                    {profile.city && (
                      <span>
                        📍 {profile.city}
                      </span>
                    )}

                    {profile.status_label && (
                      <span>
                        ● {profile.status_label}
                      </span>
                    )}
                  </div>

                  <div className="profile-card-actions">
                    <button
                      onClick={() => openEdit(profile)}
                    >
                      Modifier
                    </button>

                    <button
                      className="danger"
                      onClick={() => handleDelete(profile)}
                    >
                      Supprimer
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="profiles-principle">
        <span className="profiles-kicker">
          ARCHITECTURE NSIKAY
        </span>

        <h2>
          Un compte · plusieurs dimensions
        </h2>

        <div className="profiles-principle-grid">
          <div>
            <strong>PROFIL PERSONNEL</strong>
            <p>
              Identité, présentation et informations personnelles.
            </p>
          </div>

          <div>
            <strong>ACTIVITÉS</strong>
            <p>
              Métier, services, entreprise et projets.
            </p>
          </div>

          <div>
            <strong>ENGAGEMENT</strong>
            <p>
              Associations, événements, actions et participation.
            </p>
          </div>
        </div>
      </section>

      {showForm && (
        <div className="profile-modal-backdrop">
          <div className="profile-modal">

            <div className="profile-modal-header">
              <div>
                <span className="profiles-kicker">
                  {editingId
                    ? "MODIFICATION"
                    : "NOUVEAU PROFIL"}
                </span>

                <h2>
                  {editingId
                    ? "Modifier le profil"
                    : "Créer un profil NSIKAY"}
                </h2>
              </div>

              <button
                className="profile-modal-close"
                onClick={() => setShowForm(false)}
              >
                ×
              </button>
            </div>

            <form
              className="profile-form"
              onSubmit={handleSubmit}
            >

              <div className="profile-form-grid">

                <label>
                  Type de profil

                  <select
                    name="profile_type"
                    value={form.profile_type}
                    onChange={handleChange}
                    disabled={Boolean(editingId)}
                  >
                    {profileCategories
                      .flatMap((category) =>
                        category.items
                      )
                      .map(([type, label]) => (
                        <option
                          key={type}
                          value={type}
                        >
                          {label}
                        </option>
                      ))}
                  </select>
                </label>

                <label>
                  Nom affiché *

                  <input
                    name="display_name"
                    value={form.display_name}
                    onChange={handleChange}
                    placeholder="Nom du profil"
                    required
                  />
                </label>

                <label>
                  Nom légal

                  <input
                    name="legal_name"
                    value={form.legal_name}
                    onChange={handleChange}
                    placeholder="Nom légal si nécessaire"
                  />
                </label>

                <label>
                  Métier / fonction

                  <input
                    name="professional_title"
                    value={form.professional_title}
                    onChange={handleChange}
                    placeholder="Ex. Entrepreneur, artiste..."
                  />
                </label>

                <label>
                  Pays

                  <input
                    name="country"
                    value={form.country}
                    onChange={handleChange}
                    placeholder="Pays"
                  />
                </label>

                <label>
                  Ville

                  <input
                    name="city"
                    value={form.city}
                    onChange={handleChange}
                    placeholder="Ville"
                  />
                </label>

                <label>
                  Téléphone

                  <input
                    name="phone"
                    value={form.phone}
                    onChange={handleChange}
                    placeholder="Téléphone"
                  />
                </label>

                <label>
                  Site web

                  <input
                    name="website"
                    type="url"
                    value={form.website}
                    onChange={handleChange}
                    placeholder="https://..."
                  />
                </label>

                <label>
                  Secteur

                  <input
                    name="sector"
                    value={form.sector}
                    onChange={handleChange}
                    placeholder="Secteur d'activité"
                  />
                </label>

                <label>
                  Visibilité

                  <select
                    name="visibility"
                    value={form.visibility}
                    onChange={handleChange}
                  >
                    <option value="public">
                      Public
                    </option>

                    <option value="private">
                      Privé
                    </option>
                  </select>
                </label>

                <label>
                  Statut

                  <select
                    name="status"
                    value={form.status}
                    onChange={handleChange}
                  >
                    <option value="draft">
                      Brouillon
                    </option>

                    <option value="active">
                      Actif
                    </option>

                    <option value="suspended">
                      Suspendu
                    </option>
                  </select>
                </label>

                <label className="profile-checkbox">
                  <input
                    type="checkbox"
                    name="is_primary"
                    checked={form.is_primary}
                    onChange={handleChange}
                  />

                  <span>
                    Définir comme profil principal
                  </span>
                </label>

              </div>

              <label>
                Description

                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  placeholder="Présentez ce profil..."
                  rows="5"
                />
              </label>

              <div className="profile-form-footer">

                <button
                  type="button"
                  className="profiles-secondary-button"
                  onClick={() => setShowForm(false)}
                >
                  Annuler
                </button>

                <button
                  type="submit"
                  className="profiles-primary-button"
                  disabled={saving}
                >
                  {saving
                    ? "Enregistrement..."
                    : editingId
                      ? "Enregistrer les modifications"
                      : "Créer le profil"}
                </button>

              </div>

            </form>
          </div>
        </div>
      )}

    </main>
  );
}
