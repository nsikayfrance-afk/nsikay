import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import Home from "./pages/Home";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import ProtectedRoleRoute from "./components/ProtectedRoleRoute";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import Admin from "./pages/Admin";
import Home from "./pages/Home";
import Profiles from "./pages/Profiles";
import Home from "./pages/Home";
import Activities from "./pages/Activities";
import Home from "./pages/Home";
import ActivityCertificationAuthority from "./pages/ActivityCertificationAuthority";
import Home from "./pages/Home";
import MyProfile from "./pages/MyProfile";
import Home from "./pages/Home";
import Finance from "./pages/Finance";

import Home from "./pages/Home";
import TV from "./pages/TV";
import Home from "./pages/Home";
import TVRegie from "./pages/TVRegie";
import Home from "./pages/Home";
import NSIKAYCamera from "./pages/NSIKAYCamera";
import Home from "./pages/Home";
import MediaLibrary from "./pages/MediaLibrary";
import Home from "./pages/Home";
import Membership from "./pages/Membership";
import Home from "./pages/Home";
import "./index.css";
import Home from "./pages/Home";
import ForgotPassword from "./pages/ForgotPassword";
import Home from "./pages/Home";
import ResetPassword from "./pages/ResetPassword";
import Home from "./pages/Home";
import Transport from "./pages/Transport";
import Home from "./pages/Home";
import TransportOnboarding from "./pages/TransportOnboarding";

import Home from "./pages/Home";
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


function AdminGate({ children }) {
    const { loading, isSuperuser, isStaff } = useAuth();

    if (loading) {
        return null;
    }

    if (!isSuperuser && !isStaff) {
        return <Navigate to="/espace" replace />;
    }

    return children;
}
export default function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            /><Route path="/" element={<Home />} />
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
          path="/certification-activites"
          element={
            <ProtectedRoleRoute
              allowed={["certification_authority"]}
            >
              <ActivityCertificationAuthority />
            </ProtectedRoleRoute>
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
                        path="/activities"
                        element={
                            <ProtectedRoute>
                                <Activities />
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
    path="/publicite"
    element={
        <ProtectedRoute>
            <Placeholder
                title="Publicité"
                icon="📢"
            />
        </ProtectedRoute>
    }
/>
        <Route
          path="/transport"
          element={<Transport section="home" />}
        />
        <Route
          path="/transport/marchandises"
          element={<Transport section="marchandises" />}
        />
        <Route
          path="/transport/personnes"
          element={<Transport section="personnes" />}
        />
        <Route path="/transport/inscription" element={<TransportOnboarding />} /><Route
    path="/admin"
    element={
        <AdminGate>
            <Admin />
        </AdminGate>
    }
/>
<Route
                        path="/adhesion"
                        element={
                            <ProtectedRoute>
                                <Membership />
                            </ProtectedRoute>
                        }
                    />                    <Route
                        path="/finance"
                        element={
                            <ProtectedRoute>
                                <Finance />
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
















