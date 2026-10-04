import { useEffect, useMemo, useState } from "react";
import financeApi from "../services/finance";

const sections = [
    ["overview", "Vue générale"],
    ["wallet", "Portefeuille"],
    ["transactions", "Transactions"],
    ["banks", "Banques partenaires"],
    ["partners", "Partenaires financiers"],
    ["credits", "Crédits"],
    ["insurance", "Assurances"],
    ["currencies", "Devises"],
    ["routing", "Routage financier"],
    ["commissions", "Commissions"],
    ["reports", "Rapports"],
    ["security", "Sécurité / conformité"],
    ["admin", "Administration finance"],
];

const datasets = {
    banks: ["banks", "bank_accounts", "bank_services"],
    partners: [
        "partner_applications",
        "partner_certifications",
        "partner_supplies",
        "partner_wallets",
        "partner_deposits",
        "supply_transactions",
    ],
    credits: ["bank_credits"],
    insurance: ["bank_insurances"],
    currencies: ["currencies", "exchange_rates"],
    routing: ["routing_rules", "routing_logs"],
    commissions: ["commissions", "fees"],
    reports: [
        "control_reports",
        "compliance_reports",
        "bank_reports",
    ],
    security: [
        "audit_logs",
        "compliance_logs",
        "fraud_alerts",
        "partner_approvals",
    ],
};

function CountCard({ label, value }) {
    return (
        <div className="finance-count-card">
            <div className="finance-count-value">{value}</div>
            <div className="finance-count-label">{label}</div>
        </div>
    );
}

function DataBlock({ title, data }) {
    if (!Array.isArray(data)) {
        return (
            <div className="finance-data-block">
                <h3>{title}</h3>
                <div className="finance-empty">Aucune donnée.</div>
            </div>
        );
    }

    return (
        <div className="finance-data-block">
            <div className="finance-data-title">
                <h3>{title}</h3>
                <span>{data.length}</span>
            </div>

            {data.length === 0 ? (
                <div className="finance-empty">
                    Aucune donnée enregistrée.
                </div>
            ) : (
                <div className="finance-data-list">
                    {data.slice(0, 20).map((item, index) => (
                        <pre key={index}>
                            {JSON.stringify(item, null, 2)}
                        </pre>
                    ))}
                </div>
            )}
        </div>
    );
}

export default function Finance() {
    const [active, setActive] = useState("overview");
    const [overview, setOverview] = useState(null);
    const [status, setStatus] = useState(null);
    const [wallet, setWallet] = useState(null);
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let mounted = true;

        async function loadFinance() {
            setLoading(true);
            setError("");

            const results = await Promise.allSettled([
                financeApi.status(),
                financeApi.overview(),
                financeApi.wallet(),
                financeApi.transactions(),
            ]);

            if (!mounted) return;

            const [statusResult, overviewResult, walletResult, txResult] =
                results;

            if (statusResult.status === "fulfilled") {
                setStatus(statusResult.value);
            }

            if (overviewResult.status === "fulfilled") {
                setOverview(overviewResult.value);
            } else {
                setError(
                    overviewResult.reason?.message ||
                        "Impossible de charger les données financières."
                );
            }

            if (walletResult.status === "fulfilled") {
                setWallet(walletResult.value);
            }

            if (txResult.status === "fulfilled") {
                const value = txResult.value;
                setTransactions(
                    Array.isArray(value)
                        ? value
                        : value?.results || value?.transactions || []
                );
            }

            setLoading(false);
        }

        loadFinance();

        return () => {
            mounted = false;
        };
    }, []);

    const counts = useMemo(() => {
        if (!overview) return {};

        const result = {};

        Object.entries(overview).forEach(([key, value]) => {
            if (Array.isArray(value)) {
                result[key] = value.length;
            }
        });

        return result;
    }, [overview]);

    const activeDataset = datasets[active] || [];

    return (
        <div className="finance-page">
            <aside className="finance-sidebar">
                <div className="finance-brand">
                    <div className="finance-brand-title">NSIKAY</div>
                    <div className="finance-brand-subtitle">FINANCE</div>
                </div>

                <div className="finance-menu">
                    {sections.map(([key, label]) => (
                        <button
                            key={key}
                            className={
                                active === key
                                    ? "finance-menu-item active"
                                    : "finance-menu-item"
                            }
                            onClick={() => setActive(key)}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </aside>

            <main className="finance-main">
                <header className="finance-header">
                    <div>
                        <div className="finance-eyebrow">
                            NSIKAY / ESPACE FINANCIER
                        </div>
                        <h1>Finance</h1>
                        <p>
                            Banques, partenaires, portefeuille, opérations,
                            devises, routage, commissions et conformité.
                        </p>
                    </div>

                    <div className="finance-status">
                        <span className="finance-status-dot" />
                        {status?.status || "CHARGEMENT"}
                    </div>
                </header>

                {loading && (
                    <div className="finance-loading">
                        Chargement des données financières...
                    </div>
                )}

                {error && (
                    <div className="finance-error">
                        {error}
                    </div>
                )}

                {active === "overview" && (
                    <>
                        <section className="finance-grid">
                            <CountCard
                                label="Banques"
                                value={counts.banks ?? 0}
                            />
                            <CountCard
                                label="Comptes bancaires"
                                value={counts.bank_accounts ?? 0}
                            />
                            <CountCard
                                label="Partenaires"
                                value={counts.partner_applications ?? 0}
                            />
                            <CountCard
                                label="Crédits"
                                value={counts.bank_credits ?? 0}
                            />
                            <CountCard
                                label="Assurances"
                                value={counts.bank_insurances ?? 0}
                            />
                            <CountCard
                                label="Devises"
                                value={counts.currencies ?? 0}
                            />
                            <CountCard
                                label="Règles de routage"
                                value={counts.routing_rules ?? 0}
                            />
                            <CountCard
                                label="Alertes fraude"
                                value={counts.fraud_alerts ?? 0}
                            />
                        </section>

                        <section className="finance-panel">
                            <h2>Règles financières NSIKAY</h2>

                            <div className="finance-rules">
                                <div>
                                    <strong>0,50 %</strong>
                                    <span>Transfert NSIKAY standard</span>
                                </div>

                                <div>
                                    <strong>1,20 %</strong>
                                    <span>Retrait</span>
                                </div>

                                <div>
                                    <strong>0,85 %</strong>
                                    <span>Mobile Money / Visa</span>
                                </div>

                                <div>
                                    <strong>0 %</strong>
                                    <span>WENZE</span>
                                </div>
                            </div>
                        </section>

                        <section className="finance-panel">
                            <h2>Devises de référence</h2>

                            <div className="finance-currencies">
                                <span>EUR</span>
                                <span>USD</span>
                                <span>CDF</span>
                            </div>
                        </section>
                    </>
                )}

                {active === "wallet" && (
                    <section className="finance-panel">
                        <h2>Portefeuille Libenga / Wallet</h2>
                        <DataBlock
                            title="Wallet utilisateur"
                            data={
                                wallet
                                    ? [wallet]
                                    : []
                            }
                        />
                    </section>
                )}

                {active === "transactions" && (
                    <section className="finance-panel">
                        <h2>Transactions</h2>
                        <DataBlock
                            title="Opérations récentes"
                            data={transactions}
                        />
                    </section>
                )}

                {active !== "overview" &&
                    active !== "wallet" &&
                    active !== "transactions" && (
                        <section className="finance-panel">
                            <h2>
                                {sections.find(
                                    ([key]) => key === active
                                )?.[1] || "Finance"}
                            </h2>

                            {activeDataset.map((dataset) => (
                                <DataBlock
                                    key={dataset}
                                    title={dataset}
                                    data={overview?.[dataset] || []}
                                />
                            ))}
                        </section>
                    )}
            </main>
        </div>
    );
}
