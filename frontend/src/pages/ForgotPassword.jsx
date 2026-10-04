import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function ForgotPassword() {
    const navigate = useNavigate();

    const [identifier, setIdentifier] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setMessage("");
        setSubmitting(true);

        try {
            const result =
                await api.passwordRecoveryRequest(
                    identifier
                );

            setMessage(
                result.detail ||
                "Si les informations correspondent à un compte NSIKAY, un code de récupération sera envoyé."
            );

            sessionStorage.setItem(
                "nsikay_recovery_identifier",
                identifier
            );

            navigate("/reinitialiser-mot-de-passe");
        } catch (err) {
            setError(
                err.message ||
                "Impossible de traiter la demande."
            );
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <div className="auth-brand">
                    <div className="brand-mark">N</div>
                    <div>
                        <strong>NSIKAY</strong>
                        <span>Sécurité du compte</span>
                    </div>
                </div>

                <h1>Mot de passe oublié ?</h1>

                <p className="auth-subtitle">
                    Saisissez votre e-mail ou votre identifiant
                    NSIKAY pour commencer la récupération.
                </p>

                {error && (
                    <div className="form-error">
                        {error}
                    </div>
                )}

                {message && (
                    <div className="form-success">
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <label>
                        E-mail ou nom d'utilisateur
                        <input
                            value={identifier}
                            onChange={(e) =>
                                setIdentifier(
                                    e.target.value
                                )
                            }
                            autoComplete="username"
                            required
                        />
                    </label>

                    <button
                        className="primary-button"
                        disabled={submitting}
                    >
                        {submitting
                            ? "Vérification..."
                            : "Continuer"}
                    </button>
                </form>

                <div className="auth-footer">
                    <Link to="/connexion">
                        Retour à la connexion
                    </Link>
                </div>
            </div>
        </div>
    );
}
