import { useEffect, useState } from "react";
import financeApi from "../services/finance";

const sections = [
    ["overview", "Vue générale", "Synthèse financière NSIKAY"],
    ["wallet", "Libenga / Wallet", "Solde et opérations"],
    ["transactions", "Transactions", "Historique financier"],
    ["banks", "Banques", "Banques et services"],
    ["partners", "Partenaires financiers", "Partenaires et accompagnement"],
    ["credits", "Crédits", "Financement des projets"],
    ["insurance", "Assurances", "Services d'assurance"],
    ["currencies", "Devises & taux", "EUR · USD · CDF"],
    ["routing", "Routage financier", "Orientation des flux"],
    ["reports", "Rapports", "Rapports financiers"],
    ["security", "Sécurité & KYC", "Contrôles et conformité"],
    ["admin", "Administration Finance", "Pilotage réservé"],
];

function Card({ title, value, text }) {
    return (
        <div className="finance-card">
            <div className="finance-card-title">{title}</div>
            <div className="finance-card-value">{value}</div>
            <div className="finance-card-text">{text}</div>
        </div>
    );
}

export default function Finance() {
    const [active, setActive] = useState("overview");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [status, setStatus] = useState(null);
    const [wallet, setWallet] = useState(null);
    const [transactions, setTransactions] = useState(null);
    const [banks, setBanks] = useState(null);
    const [countries, setCountries] = useState(null);

    async function loadFinance() {
        setLoading(true);
        setError("");

        const results = await Promise.allSettled([
            financeApi.status(),
            financeApi.wallet(),
            financeApi.transactions(),
            financeApi.banks(),
            financeApi.countries(),
        ]);

        const [statusResult, walletResult, transactionsResult, banksResult, countriesResult] = results;

        if (statusResult.status === "fulfilled") {
            setStatus(statusResult.value);
        }

        if (walletResult.status === "fulfilled") {
            setWallet(walletResult.value);
        }

        if (transactionsResult.status === "fulfilled") {
            setTransactions(transactionsResult.value);
        }

        if (banksResult.status === "fulfilled") {
            setBanks(banksResult.value);
        }

        if (countriesResult.status === "fulfilled") {
            setCountries(countriesResult.value);
        }

        if (results.every((result) => result.status === "rejected")) {
            setError("Les données Finance ne sont pas accessibles pour cette session.");
        }

        setLoading(false);
    }

    useEffect(() => {
        loadFinance();
    }, []);

    const balances = wallet?.balances || [];
    const operations = wallet?.operations || [];

    return (
        <div className="finance-page">
            <div className="finance-header">
                <div>
                    <span className="finance-kicker">NSIKAY FINANCE</span>
                    <h1>Finance</h1>
                    <p>
                        Espace financier intégré : Libenga, transactions,
                        banques, partenaires, devises et contrôle financier.
                    </p>
                </div>

                <button
                    className="finance-refresh"
                    onClick={loadFinance}
                    disabled={loading}
                >
                    {loading ? "Actualisation..." : "Actualiser"}
                </button>
            </div>

            {error && (
                <div className="finance-alert finance-alert-error">
                    {error}
                </div>
            )}

            <div className="finance-layout">
                <aside className="finance-sidebar">
                    <div className="finance-sidebar-title">
                        ESPACE FINANCIER
                    </div>

                    {sections.map(([id, label, description]) => (
                        <button
                            key={id}
                            className={
                                active === id
                                    ? "finance-nav active"
                                    : "finance-nav"
                            }
                            onClick={() => setActive(id)}
                        >
                            <strong>{label}</strong>
                            <span>{description}</span>
                        </button>
                    ))}
                </aside>

                <main className="finance-content">
                    {active === "overview" && (
                        <>
                            <div className="finance-section-heading">
                                <div>
                                    <span>TABLEAU DE BORD</span>
                                    <h2>Vue générale</h2>
                                </div>
                                <span className="finance-status">
                                    {status?.status || "CONNECTÉ"}
                                </span>
                            </div>

                            <div className="finance-grid">
                                <Card
                                    title="Wallet"
                                    value={wallet?.wallet_id || "—"}
                                    text="Compte Libenga de la session"
                                />

                                <Card
                                    title="Soldes"
                                    value={balances.length}
                                    text="Devises actuellement disponibles"
                                />

                                <Card
                                    title="Opérations"
                                    value={operations.length}
                                    text="Dernières opérations Wallet"
                                />

                                <Card
                                    title="Transactions"
                                    value={
                                        Array.isArray(transactions?.data)
                                            ? transactions.data.length
                                            : "—"
                                    }
                                    text="Transactions retournées par l'API"
                                />
                            </div>

                            <div className="finance-panels">
                                <section className="finance-panel">
                                    <h3>Règles financières NSIKAY</h3>

                                    <div className="finance-rule">
                                        <span>Transfert NSIKAY</span>
                                        <strong>0,50 %</strong>
                                    </div>

                                    <div className="finance-rule">
                                        <span>Retrait</span>
                                        <strong>1,20 %</strong>
                                    </div>

                                    <div className="finance-rule">
                                        <span>Mobile Money / Visa</span>
                                        <strong>0,85 %</strong>
                                    </div>

                                    <div className="finance-rule">
                                        <span>WENZE</span>
                                        <strong>0 %</strong>
                                    </div>
                                </section>

                                <section className="finance-panel">
                                    <h3>Devises de référence</h3>

                                    <div className="currency-list">
                                        {["EUR", "USD", "CDF"].map((currency) => (
                                            <div key={currency}>
                                                <strong>{currency}</strong>
                                                <span>Devise de référence NSIKAY</span>
                                            </div>
                                        ))}
                                    </div>
                                </section>
                            </div>
                        </>
                    )}

                    {active === "wallet" && (
                        <>
                            <div className="finance-section-heading">
                                <div>
                                    <span>LIBENGA</span>
                                    <h2>Wallet</h2>
                                </div>
                            </div>

                            <div className="finance-grid">
                                {balances.length === 0 && (
                                    <Card
                                        title="Solde"
                                        value="—"
                                        text="Aucun solde multi-devise retourné"
                                    />
                                )}

                                {balances.map((item, index) => (
                                    <Card
                                        key={index}
                                        title={item.currency || "Devise"}
                                        value={item.balance ?? "0"}
                                        text="Solde disponible"
                                    />
                                ))}

                                <Card
                                    title="KYC"
                                    value={wallet?.kyc?.level || "LEVEL_1"}
                                    text={
                                        wallet?.kyc?.active
                                            ? "KYC actif"
                                            : "KYC à compléter"
                                    }
                                />

                                <Card
                                    title="Sécurité"
                                    value={wallet?.security || "—"}
                                    text="État de sécurité du Wallet"
                                />
                            </div>

                            <section className="finance-panel">
                                <h3>Dernières opérations</h3>

                                {operations.length === 0 ? (
                                    <p className="finance-empty">
                                        Aucune opération Wallet retournée.
                                    </p>
                                ) : (
                                    <div className="finance-table">
                                        <div className="finance-table-row finance-table-head">
                                            <span>Type</span>
                                            <span>Montant</span>
                                            <span>Devise</span>
                                            <span>Date</span>
                                        </div>

                                        {operations.map((operation, index) => (
                                            <div
                                                className="finance-table-row"
                                                key={index}
                                            >
                                                <span>{operation.type || "—"}</span>
                                                <span>{operation.amount || "—"}</span>
                                                <span>{operation.currency || "—"}</span>
                                                <span>{operation.date || "—"}</span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </section>
                        </>
                    )}

                    {active === "transactions" && (
                        <section className="finance-panel">
                            <div className="finance-section-heading">
                                <div>
                                    <span>MOUVEMENTS</span>
                                    <h2>Transactions</h2>
                                </div>
                            </div>

                            <pre className="finance-json">
                                {JSON.stringify(
                                    transactions || {
                                        status: "Aucune donnée",
                                    },
                                    null,
                                    2
                                )}
                            </pre>
                        </section>
                    )}

                    {active === "banks" && (
                        <section className="finance-panel">
                            <div className="finance-section-heading">
                                <div>
                                    <span>RÉSEAU BANCAIRE</span>
                                    <h2>Banques</h2>
                                </div>
                            </div>

                            <pre className="finance-json">
                                {JSON.stringify(
                                    banks || {
                                        status: "Aucune donnée",
                                    },
                                    null,
                                    2
                                )}
                            </pre>
                        </section>
                    )}

                    {active === "currencies" && (
                        <section className="finance-panel">
                            <div className="finance-section-heading">
                                <div>
                                    <span>CHANGE</span>
                                    <h2>Devises & taux</h2>
                                </div>
                            </div>

                            <div className="currency-list large">
                                {["EUR", "USD", "CDF"].map((currency) => (
                                    <div key={currency}>
                                        <strong>{currency}</strong>
                                        <span>
                                            Devise de référence NSIKAY
                                        </span>
                                    </div>
                                ))}
                            </div>

                            <p className="finance-note">
                                Les équivalences doivent utiliser les taux
                                datés et sourcés enregistrés par NSIKAY.
                            </p>
                        </section>
                    )}

                    {active === "security" && (
                        <section className="finance-panel">
                            <div className="finance-section-heading">
                                <div>
                                    <span>PROTECTION</span>
                                    <h2>Sécurité & KYC</h2>
                                </div>
                            </div>

                            <div className="finance-security-grid">
                                <Card
                                    title="KYC"
                                    value={wallet?.kyc?.level || "LEVEL_1"}
                                    text="Niveau KYC du Wallet"
                                />
                                <Card
                                    title="Wallet"
                                    value={wallet?.security || "ACTIVE"}
                                    text="Protection du compte"
                                />
                                <Card
                                    title="Contrôle"
                                    value="ACTIF"
                                    text="Surveillance financière"
                                />
                            </div>
                        </section>
                    )}

                    {active !== "overview" &&
                        active !== "wallet" &&
                        active !== "transactions" &&
                        active !== "banks" &&
                        active !== "currencies" &&
                        active !== "security" && (
                            <section className="finance-panel">
                                <div className="finance-section-heading">
                                    <div>
                                        <span>MODULE FINANCE</span>
                                        <h2>
                                            {
                                                sections.find(
                                                    ([id]) => id === active
                                                )?.[1]
                                            }
                                        </h2>
                                    </div>
                                </div>

                                <div className="finance-module-placeholder">
                                    <strong>
                                        Module connecté à l'écosystème Finance
                                        NSIKAY
                                    </strong>
                                    <p>
                                        Cette section est maintenant visible
                                        dans l'architecture Finance. Les
                                        opérations métier seront raccordées
                                        aux API correspondantes sans créer de
                                        fausses données.
                                    </p>

                                    {active === "partners" && (
                                        <div className="finance-info-box">
                                            Partenaires financiers ·
                                            certification · dépôts ·
                                            approvisionnement
                                        </div>
                                    )}

                                    {active === "credits" && (
                                        <div className="finance-info-box">
                                            Crédits · projets ·
                                            accompagnement bancaire
                                        </div>
                                    )}

                                    {active === "insurance" && (
                                        <div className="finance-info-box">
                                            Assurances et services bancaires
                                        </div>
                                    )}

                                    {active === "routing" && (
                                        <div className="finance-info-box">
                                            Routage des commissions, cartes,
                                            ventes et revenus selon les règles
                                            administratives.
                                        </div>
                                    )}

                                    {active === "reports" && (
                                        <div className="finance-info-box">
                                            Rapports financiers, audit et
                                            contrôle.
                                        </div>
                                    )}

                                    {active === "admin" && (
                                        <div className="finance-info-box">
                                            Zone réservée aux administrateurs
                                            et contrôleurs autorisés.
                                        </div>
                                    )}
                                </div>
                            </section>
                        )}

                    <div className="finance-footer-info">
                        Pays disponibles :{" "}
                        {countries?.countries?.length ??
                            "API pays disponible"}
                    </div>
                </main>
            </div>
        </div>
    );
}
