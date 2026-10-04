import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function ResetPassword() {
    const navigate = useNavigate();

    const [recoveryId, setRecoveryId] = useState("");
    const [code, setCode] = useState("");
    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] =
        useState("");

    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleVerify() {
        setError("");
        setMessage("");

        if (!recoveryId || !code) {
            setError(
                "Saisissez l'identifiant de récupération et le code reçu."
            );
            return;
        }

        setSubmitting(true);

        try {
            await api.passwordRecoveryVerify(
                Number(recoveryId),
                code
            );

            setMessage(
                "Code vérifié. Vous pouvez maintenant définir votre nouveau mot de passe."
            );
        } catch (err) {
            setError(
                err.message ||
                "Code invalide ou expiré."
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleReset(event) {
        event.preventDefault();

        setError("");
        setMessage("");

        if (!recoveryId || !code) {
            setError(
                "Saisissez l'identifiant de récupération et le code."
            );
            return;
        }

        setSubmitting(true);

        try {
            const result =
                await api.passwordRecoveryReset(
                    Number(recoveryId),
                    code,
                    password,
                    passwordConfirm
                );

            setMessage(
                result.detail ||
                "Votre mot de passe a été réinitialisé."
            );

            setTimeout(() => {
                navigate("/connexion");
            }, 1200);
        } catch (err) {
            setError(
                err.message ||
                "Impossible de réinitialiser le mot de passe."
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

                <h1>Réinitialiser le mot de passe</h1>

                <p className="auth-subtitle">
                    Entrez le code reçu puis choisissez
                    un nouveau mot de passe.
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

                <label>
                    Identifiant de récupération
                    <input
                        inputMode="numeric"
                        value={recoveryId}
                        onChange={(e) =>
                            setRecoveryId(
                                e.target.value
                            )
                        }
                        placeholder="Identifiant reçu"
                    />
                </label>

                <label>
                    Code de récupération
                    <input
                        inputMode="numeric"
                        maxLength={6}
                        value={code}
                        onChange={(e) =>
                            setCode(
                                e.target.value
                                    .replace(/\D/g, "")
                            )
                        }
                        autoComplete="one-time-code"
                        placeholder="6 chiffres"
                    />
                </label>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={handleVerify}
                    disabled={submitting}
                >
                    Vérifier le code
                </button>

                <form onSubmit={handleReset}>
                    <label>
                        Nouveau mot de passe
                        <input
                            type="password"
                            value={password}
                            onChange={(e) =>
                                setPassword(
                                    e.target.value
                                )
                            }
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />
                    </label>

                    <label>
                        Confirmation
                        <input
                            type="password"
                            value={passwordConfirm}
                            onChange={(e) =>
                                setPasswordConfirm(
                                    e.target.value
                                )
                            }
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />
                    </label>

                    <button
                        className="primary-button"
                        disabled={submitting}
                    >
                        {submitting
                            ? "Modification..."
                            : "Réinitialiser mon mot de passe"}
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
