import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const adminModules = [
  {
    icon: "👥",
    title: "Utilisateurs",
    category: "Administration",
    description: "Membres, profils, rôles et accès NSIKAY.",
    path: "/profils",
  },
  {
    icon: "🛡️",
    title: "Certification",
    category: "Conformité",
    description: "Certifications, agents et inspections.",
    path: "/certification",
  },
  {
    icon: "🏦",
    title: "Banque & Finance",
    category: "Finance",
    description: "Banques partenaires, opérations et devises.",
    path: "/finance",
  },
  {
    icon: "💰",
    title: "Libenga",
    category: "Finance",
    description: "Portefeuilles et opérations financières.",
    path: "/libenga",
  },
  {
    icon: "🛒",
    title: "WENZE",
    category: "Commerce",
    description: "Commerce, vendeurs, produits et commandes.",
    path: "/wenze",
  },
  {
    icon: "🚗",
    title: "Transport",
    category: "Mobilité",
    description: "Marchandises, livraisons et transport de personnes.",
    path: "/transport",
  },
  {
    icon: "🎫",
    title: "Événements",
    category: "Organisation",
    description: "Événements, inscriptions et billetterie.",
    path: "/events",
  },
  {
    icon: "📢",
    title: "Publicité",
    category: "Communication",
    description: "Campagnes, visibilité et espaces publicitaires.",
    path: "/publicite",
  },
  {
    icon: "📺",
    title: "NSIKAY TV",
    category: "Média",
    description: "Contenus, chaînes et régie média.",
    path: "/tv",
  },
  {
    icon: "🌍",
    title: "Pays & Territoires",
    category: "Administration",
    description: "Configuration et supervision des espaces pays.",
    path: "/admin",
  },
  {
    icon: "⚙️",
    title: "Configuration",
    category: "Système",
    description: "Paramètres généraux de la plateforme NSIKAY.",
    path: "/admin",
  },
];

const globalCards = [
  {
    key: "services",
    label: "Services",
    icon: "🧩",
  },
  {
    key: "pays",
    label: "Pays",
    icon: "🌍",
  },
  {
    key: "matrice",
    label: "Matrice",
    icon: "🗂️",
  },
  {
    key: "actifs",
    label: "Actifs",
    icon: "🟢",
  },
  {
    key: "valides",
    label: "Validés",
    icon: "✅",
  },
  {
    key: "attente",
    label: "En attente",
    icon: "⏳",
  },
];

function StatCard({ icon, label, value, loading }) {
  return (
    <div
      style={{
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        padding: 20,
        minHeight: 125,
        boxShadow: "0 4px 14px rgba(0,0,0,0.05)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          color: "#374151",
          fontSize: 14,
          fontWeight: 600,
        }}
      >
        <span style={{ fontSize: 22 }}>{icon}</span>
        <span>{label}</span>
      </div>

      <div
        style={{
          marginTop: 18,
          fontSize: 32,
          fontWeight: 800,
          color: "#111827",
        }}
      >
        {loading ? "…" : value ?? 0}
      </div>
    </div>
  );
}

function SectionTitle({ icon, title, description }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          fontSize: 20,
          fontWeight: 800,
          color: "#111827",
        }}
      >
        <span>{icon}</span>
        <span>{title}</span>
      </div>

      {description && (
        <div
          style={{
            marginTop: 5,
            color: "#6b7280",
            fontSize: 13,
          }}
        >
          {description}
        </div>
      )}
    </div>
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
    if (!canAccessAdministration) {
      return;
    }

    setLoadingStats(true);
    setStatsError("");

    try {
      const response = await fetch(
        "/service-dashboard/statistics/",
        {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

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
        throw new Error(
          "La réponse du serveur est invalide."
        );
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
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#f5f7fb",
          color: "#374151",
          fontWeight: 600,
        }}
      >
        Vérification des accès administrateur…
      </div>
    );
  }

  if (!canAccessAdministration) {
    navigate("/espace", { replace: true });

    return null;
  }

  const globalStats =
    statistics?.statistiques_globales || {};

  const services =
    Array.isArray(statistics?.par_service)
      ? statistics.par_service
      : [];

  const countries =
    Array.isArray(statistics?.par_pays)
      ? statistics.par_pays
      : [];

  const logsTotal = statistics?.logs_total ?? 0;

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f5f7fb",
        padding: "32px 24px 60px",
        color: "#111827",
      }}
    >
      <div
        style={{
          maxWidth: 1400,
          margin: "0 auto",
        }}
      >
        <header className="nsikay-admin-page"
          style={{
            background:
              "linear-gradient(135deg, #111827 0%, #1f2937 55%, #374151 100%)",
            color: "#ffffff",
            borderRadius: 22,
            padding: "28px 30px",
            boxShadow: "0 8px 30px rgba(0,0,0,0.12)",
            marginBottom: 24,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              gap: 20,
              flexWrap: "wrap",
            }}
          >
            <div>
              <div
                style={{
                  fontSize: 13,
                  fontWeight: 700,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  opacity: 0.75,
                }}
              >
                NSIKAY
              </div>

              <h1
                style={{
                  margin: "7px 0 8px",
                  fontSize: 32,
                  fontWeight: 900,
                }}
              >
                Administration
              </h1>

              <p
                style={{
                  margin: 0,
                  maxWidth: 720,
                  color: "#d1d5db",
                  lineHeight: 1.6,
                }}
              >
                Centre de supervision générale de la plateforme
                NSIKAY et de ses services.
              </p>
            </div>

            <div
              style={{
                background: "rgba(255,255,255,0.08)",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: 16,
                padding: 16,
                minWidth: 250,
              }}
            >
              <div
                style={{
                  fontSize: 12,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                  color: "#9ca3af",
                }}
              >
                Session administrative
              </div>

              <div
                style={{
                  marginTop: 7,
                  fontWeight: 800,
                }}
              >
                {isSuperuser
                  ? "Super Administrateur"
                  : "Administrateur / Staff"}
              </div>

              <div
                style={{
                  marginTop: 4,
                  fontSize: 12,
                  color: "#d1d5db",
                }}
              >
                Accès autorisé
              </div>
            </div>
          </div>
        </header>

        <section
          style={{
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 18,
            padding: 22,
            marginBottom: 24,
            boxShadow: "0 4px 16px rgba(0,0,0,0.04)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 16,
              flexWrap: "wrap",
              marginBottom: 20,
            }}
          >
            <div>
              <SectionTitle
                icon="📊"
                title="Statistiques administratives"
                description="Données directement fournies par le service Django de supervision."
              />

              {lastRefresh && !loadingStats && (
                <div
                  style={{
                    marginTop: -8,
                    color: "#6b7280",
                    fontSize: 12,
                  }}
                >
                  Dernière actualisation :{" "}
                  {lastRefresh.toLocaleTimeString("fr-FR")}
                </div>
              )}
            </div>

            <button
              type="button"
              onClick={loadStatistics}
              disabled={loadingStats}
              style={{
                border: "none",
                borderRadius: 12,
                padding: "11px 16px",
                background: loadingStats
                  ? "#9ca3af"
                  : "#111827",
                color: "#ffffff",
                fontWeight: 700,
                cursor: loadingStats
                  ? "wait"
                  : "pointer",
              }}
            >
              {loadingStats
                ? "Actualisation…"
                : "↻ Actualiser"}
            </button>
          </div>

          {statsError && (
            <div
              style={{
                background: "#fef2f2",
                border: "1px solid #fecaca",
                color: "#991b1b",
                borderRadius: 12,
                padding: 14,
                marginBottom: 18,
              }}
            >
              <strong>Erreur de chargement :</strong>{" "}
              {statsError}
            </div>
          )}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(170px, 1fr))",
              gap: 16,
            }}
          >
            {globalCards.map((card) => (
              <StatCard
                key={card.key}
                icon={card.icon}
                label={card.label}
                value={globalStats[card.key]}
                loading={loadingStats}
              />
            ))}

            <StatCard
              icon="📝"
              label="Logs administratifs"
              value={logsTotal}
              loading={loadingStats}
            />
          </div>
        </section>

        <section
          style={{
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 18,
            padding: 22,
            marginBottom: 24,
            boxShadow: "0 4px 16px rgba(0,0,0,0.04)",
          }}
        >
          <SectionTitle
            icon="🧩"
            title="Statistiques par service"
            description="Répartition réelle des activations enregistrées dans la matrice NSIKAY."
          />

          {loadingStats ? (
            <div
              style={{
                padding: 20,
                color: "#6b7280",
              }}
            >
              Chargement des services…
            </div>
          ) : services.length === 0 ? (
            <div
              style={{
                padding: 20,
                background: "#f9fafb",
                borderRadius: 12,
                color: "#6b7280",
              }}
            >
              Aucun service retourné par l’API.
            </div>
          ) : (
            <div
              style={{
                overflowX: "auto",
              }}
            >
              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                }}
              >
                <thead>
                  <tr>
                    {[
                      "Service",
                      "Total pays",
                      "Actifs",
                      "Inactifs",
                    ].map((header) => (
                      <th
                        key={header}
                        style={{
                          textAlign: "left",
                          padding: "12px 10px",
                          borderBottom:
                            "2px solid #e5e7eb",
                          color: "#374151",
                          fontSize: 13,
                        }}
                      >
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {services.map((item, index) => (
                    <tr
                      key={`${item.service}-${index}`}
                    >
                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                          fontWeight: 700,
                        }}
                      >
                        {item.service}
                      </td>

                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                        }}
                      >
                        {item.total_pays ?? 0}
                      </td>

                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                          fontWeight: 700,
                        }}
                      >
                        {item.actifs ?? 0}
                      </td>

                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                        }}
                      >
                        {item.inactifs ?? 0}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section
          style={{
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 18,
            padding: 22,
            marginBottom: 24,
            boxShadow: "0 4px 16px rgba(0,0,0,0.04)",
          }}
        >
          <SectionTitle
            icon="🌍"
            title="Statistiques par pays"
            description="État réel des services enregistrés pour chaque pays."
          />

          {loadingStats ? (
            <div
              style={{
                padding: 20,
                color: "#6b7280",
              }}
            >
              Chargement des pays…
            </div>
          ) : countries.length === 0 ? (
            <div
              style={{
                padding: 20,
                background: "#f9fafb",
                borderRadius: 12,
                color: "#6b7280",
              }}
            >
              Aucun pays retourné par l’API.
            </div>
          ) : (
            <div
              style={{
                overflowX: "auto",
              }}
            >
              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                }}
              >
                <thead>
                  <tr>
                    {[
                      "Pays",
                      "Services",
                      "Actifs",
                    ].map((header) => (
                      <th
                        key={header}
                        style={{
                          textAlign: "left",
                          padding: "12px 10px",
                          borderBottom:
                            "2px solid #e5e7eb",
                          color: "#374151",
                          fontSize: 13,
                        }}
                      >
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {countries.map((item, index) => (
                    <tr
                      key={`${item.pays}-${index}`}
                    >
                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                          fontWeight: 700,
                        }}
                      >
                        {item.pays}
                      </td>

                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                        }}
                      >
                        {item.services ?? 0}
                      </td>

                      <td
                        style={{
                          padding: "13px 10px",
                          borderBottom:
                            "1px solid #f0f0f0",
                          fontWeight: 700,
                        }}
                      >
                        {item.actifs ?? 0}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section>
          <SectionTitle
            icon="⚙️"
            title="Modules d’administration"
            description="Accès aux différents domaines de supervision de NSIKAY."
          />

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(250px, 1fr))",
              gap: 16,
            }}
          >
            {adminModules.map((module) => (
              <button
                key={module.title}
                type="button"
                onClick={() => navigate(module.path)}
                style={{
                  textAlign: "left",
                  background: "#ffffff",
                  border: "1px solid #e5e7eb",
                  borderRadius: 16,
                  padding: 20,
                  cursor: "pointer",
                  boxShadow:
                    "0 4px 14px rgba(0,0,0,0.04)",
                  transition:
                    "transform 0.15s ease, box-shadow 0.15s ease",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                  }}
                >
                  <span
                    style={{
                      fontSize: 30,
                    }}
                  >
                    {module.icon}
                  </span>

                  <div>
                    <div
                      style={{
                        fontSize: 17,
                        fontWeight: 800,
                        color: "#111827",
                      }}
                    >
                      {module.title}
                    </div>

                    <div
                      style={{
                        marginTop: 3,
                        fontSize: 11,
                        fontWeight: 700,
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                        color: "#6b7280",
                      }}
                    >
                      {module.category}
                    </div>
                  </div>
                </div>

                <p
                  style={{
                    margin:
                      "15px 0 0",
                    color: "#6b7280",
                    fontSize: 13,
                    lineHeight: 1.55,
                  }}
                >
                  {module.description}
                </p>

                <div
                  style={{
                    marginTop: 16,
                    color: "#111827",
                    fontSize: 13,
                    fontWeight: 700,
                  }}
                >
                  Ouvrir →
                </div>
              </button>
            ))}
          </div>
        </section>

        <section
          style={{
            marginTop: 28,
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 18,
            padding: 22,
          }}
        >
          <SectionTitle
            icon="🔐"
            title="Principes de supervision"
            description="Le tableau de bord affiche les données réellement retournées par les services NSIKAY."
          />

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(220px, 1fr))",
              gap: 12,
            }}
          >
            {[
              "Contrôle des accès administratifs",
              "Supervision des services et pays",
              "Suivi des activations",
              "Traçabilité des opérations administratives",
              "Gestion des domaines NSIKAY",
              "Données issues du backend Django",
            ].map((item) => (
              <div
                key={item}
                style={{
                  padding: 14,
                  background: "#f9fafb",
                  borderRadius: 12,
                  fontSize: 13,
                  fontWeight: 600,
                  color: "#374151",
                }}
              >
                ✓ {item}
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}