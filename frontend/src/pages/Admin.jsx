import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const modules = [
  {
    icon: "◉",
    title: "Tableau de bord",
    category: "Administration",
    description: "Supervision générale de la plateforme NSIKAY.",
    path: "/admin",
    featured: true,
  },
  {
    icon: "👥",
    title: "Utilisateurs",
    category: "Administration",
    description: "Membres, profils, accès et supervision des utilisateurs.",
    path: "/profils",
  },
  {
    icon: "✓",
    title: "Certifications",
    category: "Conformité",
    description: "Certification des personnes, agents, entreprises et organisations.",
    path: "/certification",
  },
  {
    icon: "▣",
    title: "Entreprises",
    category: "Économie",
    description: "Enregistrement, certification et supervision des entreprises.",
    path: "/companies",
  },
  {
    icon: "◆",
    title: "Emploi",
    category: "Emploi",
    description: "Offres, candidatures, sélections, engagements et contrats.",
    path: "/jobs",
  },
  {
    icon: "◇",
    title: "Assurances",
    category: "Emploi & protection",
    description: "Partenaires, produits et assurances obligatoires liées aux engagements.",
    path: "/jobs",
  },
  {
    icon: "▤",
    title: "Banques partenaires",
    category: "Finance",
    description: "Banques certifiées, services, comptes et relations pays.",
    path: "/finance",
  },
  {
    icon: "¤",
    title: "Finance NSIKAY",
    category: "Finance",
    description: "Libenga, transactions, devises, routage et commissions.",
    path: "/finance",
  },
  {
    icon: "W",
    title: "WENZE",
    category: "Commerce",
    description: "Produits, vendeurs, commandes et commerce international.",
    path: "/wenze",
  },
  {
    icon: "→",
    title: "Transport",
    category: "Mobilité",
    description: "Livraisons WENZE et transport de personnes.",
    path: "/transport",
  },
  {
    icon: "●",
    title: "Événements",
    category: "Organisation",
    description: "Événements, inscriptions et billetterie.",
    path: "/events",
  },
  {
    icon: "◆",
    title: "Publicité",
    category: "Communication",
    description: "Campagnes, espaces publicitaires et visibilité.",
    path: "/publicite",
  },
  {
    icon: "TV",
    title: "NSIKAY TV",
    category: "Média",
    description: "Contenus, chaînes, partenaires et régie média.",
    path: "/tv",
  },
  {
    icon: "◎",
    title: "Pays & territoires",
    category: "Administration",
    description: "Supervision des pays, services et activations.",
    path: "/admin",
  },
];

const statCards = [
  ["services", "Services", "Services enregistrés"],
  ["pays", "Pays", "Pays dans la matrice"],
  ["matrice", "Relations", "Relations service / pays"],
  ["actifs", "Actifs", "Activations actives"],
  ["valides", "Validés", "Éléments validés"],
  ["attente", "En attente", "Demandes à traiter"],
];

function StatCard({ label, value, description, loading }) {
  return (
    <div className="ns-admin-stat">
      <div className="ns-admin-stat-label">{label}</div>
      <div className="ns-admin-stat-value">
        {loading ? "…" : Number(value ?? 0).toLocaleString("fr-FR")}
      </div>
      <div className="ns-admin-stat-description">{description}</div>
    </div>
  );
}

function ModuleCard({ module, onOpen }) {
  return (
    <button
      type="button"
      className={`ns-admin-module ${module.featured ? "featured" : ""}`}
      onClick={() => onOpen(module.path)}
    >
      <div className="ns-admin-module-top">
        <span className="ns-admin-module-icon">{module.icon}</span>
        <span className="ns-admin-module-category">{module.category}</span>
      </div>

      <div className="ns-admin-module-title">{module.title}</div>

      <div className="ns-admin-module-description">
        {module.description}
      </div>

      <div className="ns-admin-module-action">
        Ouvrir le module <span>→</span>
      </div>
    </button>
  );
}

export default function Admin() {
  const navigate = useNavigate();
  const { loading: authLoading, isSuperuser, isStaff } = useAuth();

  const [statistics, setStatistics] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [statsError, setStatsError] = useState("");
  const [lastRefresh, setLastRefresh] = useState(null);

  const canAccessAdministration =
    Boolean(isSuperuser) || Boolean(isStaff);

  const loadStatistics = useCallback(async () => {
    if (!canAccessAdministration) return;

    setLoadingStats(true);
    setStatsError("");

    try {
      const response = await fetch("/service-dashboard/statistics/", {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        let detail = "";

        try {
          const errorData = await response.json();
          detail =
            errorData?.detail ||
            errorData?.message ||
            "";
        } catch {
          // Réponse non JSON.
        }

        throw new Error(
          detail ||
            `Erreur HTTP ${response.status} lors du chargement des statistiques.`
        );
      }

      const data = await response.json();

      if (!data || typeof data !== "object") {
        throw new Error("La réponse du serveur est invalide.");
      }

      setStatistics(data);
      setLastRefresh(new Date());
    } catch (error) {
      console.error(
        "NSIKAY - erreur statistiques administration:",
        error
      );

      setStatistics(null);
      setStatsError(
        error?.message ||
          "Impossible de charger les statistiques administratives."
      );
    } finally {
      setLoadingStats(false);
    }
  }, [canAccessAdministration]);

  useEffect(() => {
    if (!authLoading && canAccessAdministration) {
      loadStatistics();
    }
  }, [
    authLoading,
    canAccessAdministration,
    loadStatistics,
  ]);

  if (authLoading) {
    return (
      <div className="ns-admin-loading-screen">
        Vérification des accès administrateur…
      </div>
    );
  }

  if (!canAccessAdministration) {
    navigate("/espace", { replace: true });
    return null;
  }

  const globalStats = statistics?.statistiques_globales || {};

  const services = Array.isArray(statistics?.par_service)
    ? statistics.par_service
    : [];

  const countries = Array.isArray(statistics?.par_pays)
    ? statistics.par_pays
    : [];

  const logsTotal = statistics?.logs_total ?? 0;

  return (
    <div className="ns-admin-page">
      <div className="ns-admin-watermark" aria-hidden="true">
        EMPIRE KUBA
      </div>

      <div className="ns-admin-container">
        <header className="ns-admin-hero">
          <div className="ns-admin-hero-grid">
            <div>
              <div className="ns-admin-eyebrow">
                NSIKAY · ADMINISTRATION CENTRALE
              </div>

              <h1>Centre de supervision</h1>

              <p>
                Administration générale de l'écosystème NSIKAY :
                territoires, services, certifications, emploi,
                finance, commerce, médias et conformité.
              </p>

              <div className="ns-admin-hero-actions">
                <button
                  type="button"
                  className="ns-admin-gold-button"
                  onClick={loadStatistics}
                  disabled={loadingStats}
                >
                  {loadingStats
                    ? "Actualisation…"
                    : "Actualiser les données"}
                </button>

                <button
                  type="button"
                  className="ns-admin-dark-button"
                  onClick={() => navigate("/finance")}
                >
                  Ouvrir Finance
                </button>
              </div>
            </div>

            <div className="ns-admin-identity-card">
              <div className="ns-admin-identity-label">
                ESPACE SÉCURISÉ
              </div>

              <div className="ns-admin-identity-title">
                {isSuperuser
                  ? "Super Administrateur NSIKAY"
                  : "Administrateur NSIKAY"}
              </div>

              <div className="ns-admin-identity-status">
                <span />
                Accès administratif autorisé
              </div>

              <div className="ns-admin-identity-divider" />

              <div className="ns-admin-identity-note">
                Les données affichées proviennent des services
                Django actifs de NSIKAY.
              </div>
            </div>
          </div>
        </header>

        <section className="ns-admin-section">
          <div className="ns-admin-section-heading">
            <div>
              <div className="ns-admin-section-kicker">
                SUPERVISION
              </div>
              <h2>État global de NSIKAY</h2>
              <p>
                Vue synthétique des services et activations enregistrés.
              </p>
            </div>

            {lastRefresh && (
              <div className="ns-admin-refresh">
                Dernière actualisation{" "}
                {lastRefresh.toLocaleTimeString("fr-FR")}
              </div>
            )}
          </div>

          {statsError && (
            <div className="ns-admin-error">
              <strong>Erreur :</strong> {statsError}
            </div>
          )}

          <div className="ns-admin-stats-grid">
            {statCards.map(([key, label, description]) => (
              <StatCard
                key={key}
                label={label}
                value={globalStats[key]}
                description={description}
                loading={loadingStats}
              />
            ))}

            <StatCard
              label="Journal"
              value={logsTotal}
              description="Logs administratifs"
              loading={loadingStats}
            />
          </div>
        </section>

        <section className="ns-admin-section">
          <div className="ns-admin-section-heading">
            <div>
              <div className="ns-admin-section-kicker">
                CONTRÔLE TERRITORIAL
              </div>
              <h2>Services par pays</h2>
              <p>
                Données réelles retournées par le service de supervision.
              </p>
            </div>
          </div>

          {loadingStats ? (
            <div className="ns-admin-empty">
              Chargement des données territoriales…
            </div>
          ) : countries.length === 0 ? (
            <div className="ns-admin-empty">
              Aucun pays retourné par l'API.
            </div>
          ) : (
            <div className="ns-admin-table-wrap">
              <table className="ns-admin-table">
                <thead>
                  <tr>
                    <th>Pays</th>
                    <th>Services</th>
                    <th>Actifs</th>
                  </tr>
                </thead>
                <tbody>
                  {countries.map((item, index) => (
                    <tr key={`${item.pays}-${index}`}>
                      <td className="strong">
                        {item.pays || "—"}
                      </td>
                      <td>{item.services ?? 0}</td>
                      <td>
                        <span className="ns-admin-badge success">
                          {item.actifs ?? 0}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="ns-admin-section">
          <div className="ns-admin-section-heading">
            <div>
              <div className="ns-admin-section-kicker">
                MATRICE NSIKAY
              </div>
              <h2>Services</h2>
              <p>
                Répartition des services et de leur état d'activation.
              </p>
            </div>
          </div>

          {loadingStats ? (
            <div className="ns-admin-empty">
              Chargement des services…
            </div>
          ) : services.length === 0 ? (
            <div className="ns-admin-empty">
              Aucun service retourné par l'API.
            </div>
          ) : (
            <div className="ns-admin-table-wrap">
              <table className="ns-admin-table">
                <thead>
                  <tr>
                    <th>Service</th>
                    <th>Total pays</th>
                    <th>Actifs</th>
                    <th>Inactifs</th>
                  </tr>
                </thead>
                <tbody>
                  {services.map((item, index) => (
                    <tr key={`${item.service}-${index}`}>
                      <td className="strong">
                        {item.service || "—"}
                      </td>
                      <td>{item.total_pays ?? 0}</td>
                      <td>
                        <span className="ns-admin-badge success">
                          {item.actifs ?? 0}
                        </span>
                      </td>
                      <td>
                        <span className="ns-admin-badge neutral">
                          {item.inactifs ?? 0}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="ns-admin-section">
          <div className="ns-admin-section-heading">
            <div>
              <div className="ns-admin-section-kicker">
                DOMAINES
              </div>
              <h2>Administration NSIKAY</h2>
              <p>
                Accès aux différents domaines opérationnels.
              </p>
            </div>
          </div>

          <div className="ns-admin-module-grid">
            {modules.map((module) => (
              <ModuleCard
                key={module.title}
                module={module}
                onOpen={navigate}
              />
            ))}
          </div>
        </section>

        <section className="ns-admin-control-panel">
          <div>
            <div className="ns-admin-section-kicker">
              PRINCIPES DE CONTRÔLE
            </div>
            <h2>Une administration centralisée</h2>
          </div>

          <div className="ns-admin-control-grid">
            <div>
              <strong>Certification</strong>
              <span>
                Aucun service sensible ne doit être activé sans
                la certification requise.
              </span>
            </div>

            <div>
              <strong>Finance</strong>
              <span>
                Les opérations financières restent soumises aux
                règles et contrôles NSIKAY.
              </span>
            </div>

            <div>
              <strong>Emploi</strong>
              <span>
                L'assurance obligatoire intervient avant
                l'engagement professionnel.
              </span>
            </div>

            <div>
              <strong>Traçabilité</strong>
              <span>
                Les actions administratives doivent rester
                auditables.
              </span>
            </div>
          </div>
        </section>

        <footer className="ns-admin-footer">
          <div>
            <strong>NSIKAY</strong>
            <span>Administration centrale</span>
          </div>

          <div>
            Données fournies par les services Django actifs.
          </div>
        </footer>
      </div>
    </div>
  );
}
