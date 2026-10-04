import { Link } from "react-router-dom";
import { profileTypes } from "../data/nsikayData";

export default function Profiles() {
    return (
        <div className="ns-app">
            <header className="simple-header">
                <Link to="/espace" className="ns-logo">
                    <span className="logo-symbol">N</span>
                    <span>
                        <strong>NSIKAY</strong>
                        <small>Profils</small>
                    </span>
                </Link>

                <Link to="/espace" className="back-link">
                    ← Mon espace
                </Link>
            </header>

            <main className="content-page">
                <div className="page-intro">
                    <span className="eyebrow">
                        IDENTITÉS NSIKAY
                    </span>

                    <h1>Profils</h1>

                    <p>
                        NSIKAY accueille les personnes, professionnels,
                        entreprises, banques, écoles, institutions et
                        organisations.
                    </p>
                </div>

                <section className="profile-type-grid">
                    {profileTypes.map((item) => (
                        <article
                            key={item.key}
                            className="profile-type-card"
                        >
                            <span className="profile-type-icon">
                                {item.icon}
                            </span>

                            <h2>{item.title}</h2>

                            <p>{item.description}</p>

                            <button>
                                Découvrir →
                            </button>
                        </article>
                    ))}
                </section>
            </main>
        </div>
    );
}
