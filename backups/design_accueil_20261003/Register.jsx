import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
    const navigate = useNavigate();
    const { register } = useAuth();

    const [form, setForm] = useState({
        username: "",
        email: "",
        password: "",
        password_confirm: "",
    });

    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    function update(name, value) {
        setForm((current) => ({
            ...current,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setSubmitting(true);

        try {
            await register(form);
            navigate("/espace");
        } catch (err) {
            setError(err.message);
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card auth-card-wide">
                <div className="auth-brand">
                    <div className="brand-mark">N</div>
                    <div>
                        <strong>NSIKAY</strong>
                        <span>Créer votre identité numérique</span>
                    </div>
                </div>

                <h1>Créer un compte</h1>

                <p className="auth-subtitle">
                    Une identité NSIKAY pour votre profil, vos activités
                    et votre engagement.
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
                            value={form.username}
                            onChange={(e) =>
                                update("username", e.target.value)
                            }
                            required
                        />
                    </label>

                    <label>
                        Adresse e-mail
                        <input
                            type="email"
                            value={form.email}
                            onChange={(e) =>
                                update("email", e.target.value)
                            }
                            required
                        />
                    </label>

                    <label>
                        Mot de passe
                        <input
                            type="password"
                            value={form.password}
                            onChange={(e) =>
                                update("password", e.target.value)
                            }
                            required
                        />
                    </label>

                    <label>
                        Confirmation du mot de passe
                        <input
                            type="password"
                            value={form.password_confirm}
                            onChange={(e) =>
                                update(
                                    "password_confirm",
                                    e.target.value
                                )
                            }
                            required
                        />
                    </label>

                    <button
                        className="primary-button"
                        disabled={submitting}
                    >
                        {submitting
                            ? "Création..."
                            : "Créer mon compte"}
                    </button>
                </form>

                <div className="auth-footer">
                    Vous avez déjà un compte ?
                    <Link to="/connexion">
                        Se connecter
                    </Link>
                </div>
            </div>
        </div>
    );
}
