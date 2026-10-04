import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

const API = "/transport";

const styles = {
  page: {
    minHeight: "100vh",
    padding: "28px",
    background:
      "linear-gradient(135deg, #f5f7fb 0%, #ffffff 55%, #eef3f8 100%)",
    color: "#172033",
  },
  container: {
    maxWidth: "1250px",
    margin: "0 auto",
  },
  hero: {
    padding: "30px",
    borderRadius: "24px",
    background:
      "linear-gradient(135deg, #101c36 0%, #173d70 55%, #0b7285 100%)",
    color: "#ffffff",
    boxShadow: "0 16px 45px rgba(16,28,54,.18)",
    marginBottom: "24px",
  },
  title: {
    margin: "0 0 10px",
    fontSize: "32px",
    fontWeight: 800,
  },
  subtitle: {
    margin: 0,
    opacity: .9,
    lineHeight: 1.6,
  },
  tabs: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
    marginBottom: "24px",
  },
  tab: {
    border: "1px solid #d9e0ea",
    borderRadius: "12px",
    padding: "12px 18px",
    cursor: "pointer",
    background: "#ffffff",
    fontWeight: 700,
  },
  tabActive: {
    background: "#173d70",
    color: "#ffffff",
    borderColor: "#173d70",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
    gap: "16px",
    marginBottom: "24px",
  },
  card: {
    background: "#ffffff",
    border: "1px solid #e1e7ef",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 8px 25px rgba(20,40,70,.06)",
  },
  cardTitle: {
    margin: "0 0 8px",
    fontSize: "15px",
    color: "#667085",
  },
  number: {
    fontSize: "30px",
    fontWeight: 800,
  },
  section: {
    background: "#ffffff",
    border: "1px solid #e1e7ef",
    borderRadius: "20px",
    padding: "24px",
    marginBottom: "22px",
  },
  sectionTitle: {
    marginTop: 0,
    fontSize: "22px",
  },
  actions: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))",
    gap: "16px",
  },
  action: {
    padding: "22px",
    borderRadius: "16px",
    border: "1px solid #dce3ec",
    background: "#f9fbfd",
  },
  button: {
    border: 0,
    borderRadius: "10px",
    padding: "11px 16px",
    background: "#173d70",
    color: "#ffffff",
    fontWeight: 700,
    cursor: "pointer",
  },
  secondary: {
    background: "#eef3f8",
    color: "#172033",
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "12px",
    border: "1px solid #d5dce7",
    borderRadius: "10px",
    marginTop: "6px",
    marginBottom: "14px",
  },
  label: {
    fontWeight: 700,
    fontSize: "14px",
  },
  status: {
    padding: "12px 15px",
    borderRadius: "10px",
    background: "#eef7f0",
    color: "#23613b",
    marginBottom: "16px",
  },
  error: {
    padding: "12px 15px",
    borderRadius: "10px",
    background: "#fff0f0",
    color: "#9b2c2c",
    marginBottom: "16px",
  },
};

function StatCard({ label, value }) {
  return (
    <div className="nsikay-transport-page" style={styles.card}>
      <p style={styles.cardTitle}>{label}</p>
      <div className="nsikay-transport-page" style={styles.number}>{value ?? 0}</div>
    </div>
  );
}

function CompanyCatalog({ companies }) {
  return (
    <div className="nsikay-transport-page" style={styles.section}>
      <h2 style={styles.sectionTitle}>🏢 Entreprises de transport</h2>

      {companies.length === 0 ? (
        <p>Aucune entreprise de transport enregistrée pour le moment.</p>
      ) : (
        <div className="nsikay-transport-page" style={styles.actions}>
          {companies.map((company) => (
            <div className="nsikay-transport-page" style={styles.action} key={company.id}>
              <h3>{company.company_name || `Entreprise #${company.id}`}</h3>
              <p>
                Type :{" "}
                {company.transport_type === "GOODS"
                  ? "Marchandises"
                  : company.transport_type === "PASSENGER"
                    ? "Personnes"
                    : "Marchandises et personnes"}
              </p>
              <p>
                Localisation : {company.city || "—"},{" "}
                {company.country || "—"}
              </p>
              <p>
                Certification :{" "}
                {company.certification ? "Associée" : "À traiter"}
              </p>
              <p>
                Activation : {company.active ? "Active" : "Inactive"}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function RideForm({ onCreated }) {
  const [form, setForm] = useState({
    pickup_address: "",
    destination_address: "",
    reference: "",
    estimated_amount: "",
    currency: "",
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  function update(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");

    try {
      const response = await fetch(`${API}/personnes/courses/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          pickup_address: form.pickup_address,
          destination_address: form.destination_address,
          reference:
            form.reference ||
            `RIDE-${Date.now()}`,
          estimated_amount: form.estimated_amount || "0.00",
          currency: form.currency || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          JSON.stringify(data)
        );
      }

      setMessage("Course créée avec succès.");
      setForm({
        pickup_address: "",
        destination_address: "",
        reference: "",
        estimated_amount: "",
        currency: "",
      });

      if (onCreated) {
        onCreated(data);
      }
    } catch (error) {
      setMessage(`Erreur : ${error.message}`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <label style={styles.label}>Point de départ</label>
      <input
        style={styles.input}
        value={form.pickup_address}
        onChange={(e) =>
          update("pickup_address", e.target.value)
        }
        required
      />

      <label style={styles.label}>Destination</label>
      <input
        style={styles.input}
        value={form.destination_address}
        onChange={(e) =>
          update("destination_address", e.target.value)
        }
        required
      />

      <label style={styles.label}>Référence</label>
      <input
        style={styles.input}
        value={form.reference}
        onChange={(e) =>
          update("reference", e.target.value)
        }
        placeholder="Générée automatiquement si vide"
      />

      <label style={styles.label}>Montant estimatif</label>
      <input
        style={styles.input}
        type="number"
        step="0.01"
        value={form.estimated_amount}
        onChange={(e) =>
          update("estimated_amount", e.target.value)
        }
      />

      <label style={styles.label}>ID devise NSIKAY</label>
      <input
        style={styles.input}
        type="number"
        value={form.currency}
        onChange={(e) =>
          update("currency", e.target.value)
        }
        placeholder="À sélectionner depuis les devises disponibles"
      />

      <button style={styles.button} disabled={saving}>
        {saving ? "Enregistrement..." : "Commander la course"}
      </button>

      {message && (
        <p style={{ marginTop: "14px" }}>{message}</p>
      )}
    </form>
  );
}

function RentalForm() {
  const [form, setForm] = useState({
    start_at: "",
    end_at: "",
    pickup_address: "",
    amount: "",
    currency: "",
    reference: "",
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  function update(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");

    try {
      const response = await fetch(`${API}/personnes/locations/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          start_at: form.start_at,
          end_at: form.end_at,
          pickup_address: form.pickup_address,
          amount: form.amount || "0.00",
          currency: form.currency || null,
          reference:
            form.reference ||
            `RENTAL-${Date.now()}`,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          JSON.stringify(data)
        );
      }

      setMessage("Réservation de voiture créée avec succès.");
    } catch (error) {
      setMessage(`Erreur : ${error.message}`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <label style={styles.label}>Début de location</label>
      <input
        style={styles.input}
        type="datetime-local"
        value={form.start_at}
        onChange={(e) =>
          update("start_at", e.target.value)
        }
        required
      />

      <label style={styles.label}>Fin de location</label>
      <input
        style={styles.input}
        type="datetime-local"
        value={form.end_at}
        onChange={(e) =>
          update("end_at", e.target.value)
        }
        required
      />

      <label style={styles.label}>Lieu de prise en charge</label>
      <input
        style={styles.input}
        value={form.pickup_address}
        onChange={(e) =>
          update("pickup_address", e.target.value)
        }
      />

      <label style={styles.label}>Montant</label>
      <input
        style={styles.input}
        type="number"
        step="0.01"
        value={form.amount}
        onChange={(e) =>
          update("amount", e.target.value)
        }
      />

      <label style={styles.label}>ID devise NSIKAY</label>
      <input
        style={styles.input}
        type="number"
        value={form.currency}
        onChange={(e) =>
          update("currency", e.target.value)
        }
      />

      <label style={styles.label}>Référence</label>
      <input
        style={styles.input}
        value={form.reference}
        onChange={(e) =>
          update("reference", e.target.value)
        }
        placeholder="Générée automatiquement si vide"
      />

      <button style={styles.button} disabled={saving}>
        {saving
          ? "Enregistrement..."
          : "Réserver la voiture"}
      </button>

      {message && (
        <p style={{ marginTop: "14px" }}>{message}</p>
      )}
    </form>
  );
}

export default function Transport({
  section = "home" }) {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [services, setServices] = useState([]);
  const [deliveries, setDeliveries] = useState([]);
  const [rides, setRides] = useState([]);
  const [rentals, setRentals] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function getJson(url) {
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(
        `${response.status} ${text}`
      );
    }

    return response.json();
  }

  async function loadTransport() {
    setLoading(true);
    setError("");

    try {
      const [
        dashboardData,
        companyData,
        serviceData,
        deliveryData,
        rideData,
        rentalData,
      ] = await Promise.all([
        getJson(`${API}/dashboard/`),
        getJson(`${API}/companies/`),
        getJson(`${API}/services/`),
        getJson(`${API}/marchandises/livraisons/`),
        getJson(`${API}/personnes/courses/`),
        getJson(`${API}/personnes/locations/`),
      ]);

      setDashboard(dashboardData);
      setCompanies(companyData.results || companyData);
      setServices(serviceData.results || serviceData);
      setDeliveries(deliveryData.results || deliveryData);
      setRides(rideData.results || rideData);
      setRentals(rentalData.results || rentalData);
    } catch (err) {
      setError(
        `Impossible de charger le module Transport : ${err.message}`
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTransport();
  }, []);

  if (loading) {
    return (
      <div className="nsikay-transport-page" style={styles.page}>
        <div className="nsikay-transport-page" style={styles.container}>
          <div className="nsikay-transport-page" style={styles.card}>
            Chargement du module Transport NSIKAY...
          </div>
        </div>
      </div>
    );
  }

  const stats = dashboard?.transport || {};

  return (
    <div className="nsikay-transport-page" style={styles.page}>
      <div className="nsikay-transport-page" style={styles.container}>

        <section style={styles.hero}>
          <h1 style={styles.title}>
            🚚 Transport NSIKAY
          </h1>

          <p style={styles.subtitle}>
            Un espace unique pour le transport des marchandises
            WENZE et le transport des personnes.
          </p>
        </section>

        <div className="nsikay-transport-page" style={styles.tabs}>
          <button
            style={{
              ...styles.tab,
              ...(section === "home"
                ? styles.tabActive
                : {}),
            }}
            onClick={() =>
              navigate("/transport")
            }
          >
            🚚 Transport
          </button>

          <button
            style={{
              ...styles.tab,
              ...(section === "marchandises"
                ? styles.tabActive
                : {}),
            }}
            onClick={() =>
              navigate("/transport/marchandises"
              )
            }
          >
            📦 Marchandises WENZE
          </button>

          <button
            style={{
              ...styles.tab,
              ...(section === "personnes"
                ? styles.tabActive
                : {}),
            }}
            onClick={() =>
              navigate("/transport/personnes"
              )
            }
          >
            🚗 Transport de personnes
          </button>
        </div>

        {error && (
          <div className="nsikay-transport-page" style={styles.error}>
            {error}
            <br />
            <button
              style={{
                ...styles.button,
                marginTop: "10px",
              }}
              onClick={loadTransport}
            >
              Réessayer
            </button>
          </div>
        )}

        <div className="nsikay-transport-page" style={styles.grid}>
          <StatCard
            label="Entreprises"
            value={stats.entreprises}
          />
          <StatCard
            label="Véhicules"
            value={stats.vehicules}
          />
          <StatCard
            label="Conducteurs"
            value={stats.conducteurs}
          />
          <StatCard
            label="Services"
            value={stats.services}
          />
          <StatCard
            label="Livraisons WENZE"
            value={stats.livraisons_wenze}
          />
          <StatCard
            label="Courses"
            value={stats.courses_personnes}
          />
          <StatCard
            label="Locations"
            value={stats.locations_journee}
          />
          <StatCard
            label="Suivis"
            value={stats.suivis}
          />
        </div>

        {(section === "home" || !section) && (
          <>
            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                Deux catégories de transport
              </h2>

              <div className="nsikay-transport-page" style={styles.actions}>
                <div className="nsikay-transport-page" style={styles.action}>
                  <h3>📦 Marchandises / WENZE</h3>
                  <p>
                    Livraison des commandes effectuées dans
                    WENZE vers leur destination.
                  </p>

                  <p>
                    Les opérations sont reliées aux commandes
                    WENZE et peuvent être suivies par référence.
                  </p>
                </div>

                <div className="nsikay-transport-page" style={styles.action}>
                  <h3>🚗 Transport de personnes</h3>
                  <p>
                    Commander directement une course ou réserver
                    une voiture pour une journée.
                  </p>

                  <p>
                    Le catalogue des entreprises et services
                    permet de sélectionner l'offre disponible.
                  </p>
                </div>
              </div>
            </section>

            <CompanyCatalog companies={companies} />

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                🛡️ Certification
              </h2>

              <div className="nsikay-transport-page" style={styles.status}>
                La certification est obligatoire pour l'activation
                des activités de transport.
                <br />
                Le module utilise l'infrastructure
                <strong> NSIKAYCertification </strong>
                existante.
              </div>
            </section>
          </>
        )}

        {section === "marchandises" && (
          <section style={styles.section}>
            <h2 style={styles.sectionTitle}>
              📦 Transport des marchandises WENZE
            </h2>

            <p>
              Cette section regroupe les livraisons associées
              aux commandes WENZE.
            </p>

            {deliveries.length === 0 ? (
              <p>
                Aucune livraison WENZE enregistrée.
              </p>
            ) : (
              <div className="nsikay-transport-page" style={styles.actions}>
                {deliveries.map((delivery) => (
                  <div className="nsikay-transport-page"
                    style={styles.action}
                    key={delivery.id}
                  >
                    <h3>
                      {delivery.tracking_reference}
                    </h3>

                    <p>
                      Statut : {delivery.status}
                    </p>

                    <p>
                      Destination :{" "}
                      {delivery.delivery_address || "—"}
                    </p>

                    <p>
                      Destinataire :{" "}
                      {delivery.recipient_name || "—"}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {section === "personnes" && (
          <>
            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                🚗 Commander une course
              </h2>

              <RideForm
                onCreated={loadTransport}
              />
            </section>

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                🗓️ Réserver une voiture à la journée
              </h2>

              <RentalForm />
            </section>

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                🚕 Courses enregistrées
              </h2>

              {rides.length === 0 ? (
                <p>
                  Aucune course enregistrée.
                </p>
              ) : (
                <div className="nsikay-transport-page" style={styles.actions}>
                  {rides.map((ride) => (
                    <div className="nsikay-transport-page"
                      style={styles.action}
                      key={ride.id}
                    >
                      <h3>{ride.reference}</h3>
                      <p>
                        {ride.pickup_address}
                        {" → "}
                        {ride.destination_address}
                      </p>
                      <p>
                        Statut : {ride.status}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>
                🗓️ Locations enregistrées
              </h2>

              {rentals.length === 0 ? (
                <p>
                  Aucune location enregistrée.
                </p>
              ) : (
                <div className="nsikay-transport-page" style={styles.actions}>
                  {rentals.map((rental) => (
                    <div className="nsikay-transport-page"
                      style={styles.action}
                      key={rental.id}
                    >
                      <h3>{rental.reference}</h3>
                      <p>
                        Du {rental.start_at}
                        {" au "}
                        {rental.end_at}
                      </p>
                      <p>
                        Statut : {rental.status}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}

        <section style={styles.section}>
          <h2 style={styles.sectionTitle}>
            🏢 Catalogue Transport
          </h2>

          <p>
            Services actuellement enregistrés :
            {" "}
            <strong>{services.length}</strong>
          </p>

          {services.length > 0 && (
            <div className="nsikay-transport-page" style={styles.actions}>
              {services.map((service) => (
                <div className="nsikay-transport-page"
                  style={styles.action}
                  key={service.id}
                >
                  <h3>{service.name}</h3>

                  <p>
                    Type : {service.service_type}
                  </p>

                  <p>
                    Tarification :{" "}
                    {service.pricing_mode}
                  </p>

                  <p>
                    Statut :{" "}
                    {service.active
                      ? "Actif"
                      : "En attente d'activation"}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}