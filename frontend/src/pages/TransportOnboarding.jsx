import { useState } from "react";
import { useNavigate } from "react-router-dom";

const INITIAL_FORM = {
    name: "",
    description: "",
    transport_type: "BOTH",
    country: "",
    city: "",
    phone: "",
    email: "",
    website: "",
};

export default function TransportOnboarding() {
    const navigate = useNavigate();

    const [form, setForm] = useState(INITIAL_FORM);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState(null);

    function update(name, value) {
        setForm((current) => ({
            ...current,
            [name]: value,
        }));
    }

    async function submit(event) {
        event.preventDefault();

        setError("");
        setResult(null);
        setSubmitting(true);

        try {
            const token =
                localStorage.getItem("nsikay_token");

            if (!token) {
                throw new Error(
                    "Vous devez être connecté à NSIKAY."
                );
            }

            const response = await fetch(
                "/transport/onboarding/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Token ${token}`,
                    },
                    body: JSON.stringify(form),
                }
            );

            let data = null;

            try {
                data = await response.json();
            } catch {
                data = null;
            }

            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.message ||
                    "Impossible d'enregistrer l'entreprise."
                );
            }

            setResult(data);
        } catch (err) {
            setError(
                err?.message ||
                "Une erreur est survenue."
            );
        } finally {
            setSubmitting(false);
        }
    }

    if (result) {
        return (
            <div className="page-container">
                <div className="card">
                    <h1>
                        Entreprise enregistrée
                    </h1>

                    <p>
                        Votre entreprise de transport a été
                        enregistrée dans NSIKAY.
                    </p>

                    <div className="card">
                        <strong>
                            {result.company?.name}
                        </strong>

                        <p>
                            Certification :
                            {" "}
                            {result.certification?.status}
                        </p>

                        <p>
                            Type :
                            {" "}
                            {result.transport_company?.transport_type}
                        </p>

                        <p>
                            Localisation :
                            {" "}
                            {result.transport_company?.city}
                            {" — "}
                            {result.transport_company?.country}
                        </p>
                    </div>

                    <h2>
                        Étapes suivantes
                    </h2>

                    <ol>
                        {result.workflow?.map(
                            (step, index) => (
                                <li key={index}>
                                    {step}
                                </li>
                            )
                        )}
                    </ol>

                    <p>
                        L'entreprise reste inactive tant que
                        la certification NSIKAY et la validation
                        administrative ne sont pas terminées.
                    </p>

                    <button
                        className="primary-button"
                        onClick={() =>
                            navigate("/transport")
                        }
                    >
                        Retour au transport
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container">
            <div className="card">
                <h1>
                    Inscrire une entreprise de transport
                </h1>

                <p>
                    Enregistrez votre entreprise pour proposer
                    des services de transport de marchandises
                    et/ou de personnes sur NSIKAY.
                </p>

                {error && (
                    <div className="form-error">
                        {error}
                    </div>
                )}

                <form onSubmit={submit}>

                    <label>
                        Nom de l'entreprise

                        <input
                            value={form.name}
                            onChange={(e) =>
                                update(
                                    "name",
                                    e.target.value
                                )
                            }
                            required
                        />
                    </label>

                    <label>
                        Type de transport

                        <select
                            value={form.transport_type}
                            onChange={(e) =>
                                update(
                                    "transport_type",
                                    e.target.value
                                )
                            }
                        >
                            <option value="GOODS">
                                Marchandises / WENZE
                            </option>

                            <option value="PASSENGER">
                                Transport de personnes
                            </option>

                            <option value="BOTH">
                                Marchandises et personnes
                            </option>
                        </select>
                    </label>

                    <label>
                        Pays

                        <input
                            value={form.country}
                            onChange={(e) =>
                                update(
                                    "country",
                                    e.target.value
                                )
                            }
                            required
                        />
                    </label>

                    <label>
                        Ville

                        <input
                            value={form.city}
                            onChange={(e) =>
                                update(
                                    "city",
                                    e.target.value
                                )
                            }
                            required
                        />
                    </label>

                    <label>
                        Téléphone

                        <input
                            value={form.phone}
                            onChange={(e) =>
                                update(
                                    "phone",
                                    e.target.value
                                )
                            }
                        />
                    </label>

                    <label>
                        E-mail professionnel

                        <input
                            type="email"
                            value={form.email}
                            onChange={(e) =>
                                update(
                                    "email",
                                    e.target.value
                                )
                            }
                        />
                    </label>

                    <label>
                        Site internet

                        <input
                            type="url"
                            value={form.website}
                            onChange={(e) =>
                                update(
                                    "website",
                                    e.target.value
                                )
                            }
                            placeholder="https://..."
                        />
                    </label>

                    <label>
                        Présentation

                        <textarea
                            value={form.description}
                            onChange={(e) =>
                                update(
                                    "description",
                                    e.target.value
                                )
                            }
                            rows={5}
                        />
                    </label>

                    <div className="card">
                        <strong>
                            Certification NSIKAY obligatoire
                        </strong>

                        <p>
                            L'enregistrement ne signifie pas
                            que l'entreprise est immédiatement
                            active. Une certification NSIKAY
                            doit être traitée et approuvée,
                            puis l'administration doit valider
                            l'entreprise avant son activation.
                        </p>
                    </div>

                    <button
                        className="primary-button"
                        disabled={submitting}
                    >
                        {submitting
                            ? "Enregistrement..."
                            : "Enregistrer l'entreprise"}
                    </button>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={() =>
                            navigate("/transport")
                        }
                    >
                        Annuler
                    </button>

                </form>
            </div>
        </div>
    );
}