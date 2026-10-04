import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../services/api";

export default function ResetPassword() {
    const navigate = useNavigate();

    const [recoveryId, setRecoveryId] = useState(
        sessionStorage.getItem("nsikay_recovery_id") || ""
    );

    const [code, setCode] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    async function handleVerify(event) {
        event.preventDefault();

        setError("");
        setMessage("");

        if (!recoveryId.trim()) {
            setError("Identifiant de récupération manquant.");
            return;
        }

        if (!/^\d{6}$/.test(code.trim())) {
            setError("Le code doit contenir 6 chiffres.");
            return;
        }

        setLoading(true);

        try {
            const result = await API.passwordRecoveryVerify({
                recovery_id: recoveryId.trim(),
                code: code.trim(),
            });

            setMessage(
                result?.message ||
                "Code vérifié. Vous pouvez maintenant définir un nouveau mot de passe."
            );
        } catch (err) {
            setError(
                err?.message ||
                "Le code de vérification est incorrect ou expiré."
            );
        } finally {
            setLoading(false);
        }
    }

    async function handleReset(event) {
        event.preventDefault();

        setError("");
        setMessage("");

        if (!recoveryId.trim()) {
            setError("Identifiant de récupération manquant.");
            return;
        }

        if (!/^\d{6}$/.test(code.trim())) {
            setError("Le code doit contenir 6 chiffres.");
            return;
        }

        if (newPassword.length < 8) {
            setError("Le nouveau mot de passe doit contenir au moins 8 caractères.");
            return;
        }

        if (newPassword !== confirmPassword) {
            setError("Les deux mots de passe ne correspondent pas.");
            return;
        }

        setLoading(true);

        try {
            const result = await API.passwordRecoveryReset({
                recovery_id: recoveryId.trim(),
                code: code.trim(),
                new_password: newPassword,
            });

            sessionStorage.removeItem("nsikay_recovery_id");

            setMessage(
                result?.message ||
                "Votre mot de passe a été réinitialisé avec succès."
            );

            setCode("");
            setNewPassword("");
            setConfirmPassword("");

            setTimeout(() => {
                navigate("/login");
            }, 1200);

        } catch (err) {
            setError(
                err?.message ||
                "La réinitialisation du mot de passe a échoué."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="auth-page password-reset-page">
            <section className="auth-card">
                <h1>Réinitialiser le mot de passe</h1>

                <p>
                    Saisissez le code reçu, puis choisissez un nouveau mot de passe.
                </p>

                {error && (
                    <div role="alert" className="auth-error">
                        {error}
                    </div>
                )}

                {message && (
                    <div role="status" className="auth-success">
                        {message}
                    </div>
                )}

                <form onSubmit={handleVerify}>
                    <div>
                        <label htmlFor="recoveryId">
                            Identifiant de récupération
                        </label>

                        <input
                            id="recoveryId"
                            type="text"
                            value={recoveryId}
                            onChange={(event) =>
                                setRecoveryId(event.target.value)
                            }
                            autoComplete="off"
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="recoveryCode">
                            Code de vérification
                        </label>

                        <input
                            id="recoveryCode"
                            type="text"
                            inputMode="numeric"
                            pattern="[0-9]{6}"
                            maxLength={6}
                            value={code}
                            onChange={(event) =>
                                setCode(
                                    event.target.value
                                        .replace(/\D/g, "")
                                        .slice(0, 6)
                                )
                            }
                            autoComplete="one-time-code"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "Vérification..." : "Vérifier le code"}
                    </button>
                </form>

                <hr />

                <form onSubmit={handleReset}>
                    <div>
                        <label htmlFor="newPassword">
                            Nouveau mot de passe
                        </label>

                        <input
                            id="newPassword"
                            name="newPassword"
                            type="password"
                            value={newPassword}
                            onChange={(event) =>
                                setNewPassword(event.target.value)
                            }
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="confirmPassword">
                            Confirmer le nouveau mot de passe
                        </label>

                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type="password"
                            value={confirmPassword}
                            onChange={(event) =>
                                setConfirmPassword(event.target.value)
                            }
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={
                            loading ||
                            !recoveryId.trim() ||
                            code.length !== 6 ||
                            newPassword.length < 8 ||
                            newPassword !== confirmPassword
                        }
                    >
                        {loading
                            ? "Réinitialisation..."
                            : "Réinitialiser le mot de passe"}
                    </button>
                </form>

                <button
                    type="button"
                    onClick={() => navigate("/mot-de-passe-oublie")}
                >
                    Recommencer la récupération
                </button>
            </section>
        </main>
    );
}
