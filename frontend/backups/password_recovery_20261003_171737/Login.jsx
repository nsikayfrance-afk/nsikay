import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setSubmitting(true);

        try {
            await login(username, password);
            navigate("/espace");
        } catch (err) {
            setError(err.message);
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
                        <span>Écosystème international</span>
                    </div>
                </div>

                <h1>Connexion</h1>
                <p className="auth-subtitle">
                    Accédez à votre espace personnel, professionnel
                    et d'engagement.
                </p>

                {error && (
                    <div className="form-error">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <label>
                        Nom d'utilisateur
                        <input
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Votre identifiant"
                            autoComplete="username"
                            required
                        />
                    </label>

                    <label>
                        Mot de passe
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Votre mot de passe"
                            autoComplete="current-password"
                            required
                        />
                    </label>

                    <button
                        className="primary-button"
                        disabled={submitting}
                    >
                        {submitting ? "Connexion..." : "Se connecter"}
                    </button>
                </form>

                <div className="auth-footer">
                    Vous n'avez pas encore de compte ?
                    <Link to="/inscription">
                        Créer mon compte
                    </Link>
                </div>
            </div>
        </div>
    );
}
