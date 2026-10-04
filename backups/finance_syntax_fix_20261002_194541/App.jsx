import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profiles from "./pages/Profiles";
import MyProfile from "./pages/MyProfile";`r`nimport Finance from "./pages/Finance";

import TV from "./pages/TV";
import TVRegie from "./pages/TVRegie";
import NSIKAYCamera from "./pages/NSIKAYCamera";
import MediaLibrary from "./pages/MediaLibrary";
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
                Ã¢â€ Â Retour ÃƒÂ  mon espace
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
                        element={<Login />}
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
                                    title="MÃƒÂ©tiers"
                                    icon="Ã°Å¸Â§â€˜Ã¢â‚¬ÂÃ°Å¸â€™Â¼"
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
                                    icon="Ã°Å¸â€ºÂ¡Ã¯Â¸Â"
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
                                    icon="Ã°Å¸â€ºâ€™"
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
                                    icon="Ã°Å¸â€™Â°"
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/events"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="Ãƒâ€°vÃƒÂ©nements"
                                    icon="Ã°Å¸Å½Â«"
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
                                    icon="Ã¢Å¡â„¢Ã¯Â¸Â"
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
        <Route path="/media-library" element={<MediaLibrary />} />
      </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}





