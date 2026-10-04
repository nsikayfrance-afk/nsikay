import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import MediaLibrary from './pages/MediaLibrary';
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profiles from "./pages/Profiles";
import MyProfile from "./pages/MyProfile";

import TV from "./pages/TV";
import TVRegie from "./pages/TVRegie";
import NSIKAYCamera from "./pages/NSIKAYCamera";
import "./index.css";

function Placeholder({ title, icon }) {
    return (
        <div className="placeholder-page">
            <div className="placeholder-icon">
                {icon}
            </div>

            <span className="eyebrow">
                NSIKAY
            </span>

            <h1>{title}</h1>

            <p>
                Module visuel en cours de construction.
            </p>

            <a href="/espace">
                â† Retour Ã  mon espace
            </a>
        </div>
    );
}

export default function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    <Route
                        path="/"
                        element={
                            <Navigate
                                to="/espace"
                                replace
                            />
                        }
                    />

                    <Route
                        path="/connexion"
                        element={<Login />
        <Route path="/media-library" element={<MediaLibrary />} />}
                    />

                    <Route
                        path="/inscription"
                        element={<Register />}
                    />

                    <Route
                        path="/espace"
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/profils"
                        element={
                            <ProtectedRoute>
                                <Profiles />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/mon-profil"
                        element={
                            <ProtectedRoute>
                                <MyProfile />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/metiers"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="MÃ©tiers"
                                    icon="ðŸ§‘â€ðŸ’¼"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/certification"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="Certification"
                                    icon="ðŸ›¡ï¸"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/wenze"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="WENZE"
                                    icon="ðŸ›’"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/libenga"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="Libenga"
                                    icon="ðŸ’°"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/events"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="Ã‰vÃ©nements"
                                    icon="ðŸŽ«"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/tv"
                        element={
                            <ProtectedRoute>
                                <TV />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/tv-regie"
                        element={
                            <ProtectedRoute>
                                <TVRegie />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/admin"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="Administration"
                                    icon="âš™ï¸"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="*"
                        element={
                            <Navigate
                                to="/"
                                replace
                            />
                        }
                    />
                <Route
    path="/camera"
    element={
        <ProtectedRoute>
            <NSIKAYCamera />
        </ProtectedRoute>
    }
/>
</Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}



