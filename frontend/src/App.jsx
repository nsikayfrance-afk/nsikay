import "./styles/nsikay-global.css";
import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import ProtectedRoleRoute from "./components/ProtectedRoleRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Admin from "./pages/Admin";
import Profiles from "./pages/Profiles";
import Activities from "./pages/Activities";
import ActivityCertificationAuthority from "./pages/ActivityCertificationAuthority";
import MyProfile from "./pages/MyProfile";
import Finance from "./pages/Finance";

import TV from "./pages/TV";
import TVRegie from "./pages/TVRegie";
import NSIKAYCamera from "./pages/NSIKAYCamera";
import MediaLibrary from "./pages/MediaLibrary";
import Membership from "./pages/Membership";
import "./index.css";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Transport from "./pages/Transport";
import TransportOnboarding from "./pages/TransportOnboarding";
import Home from "./pages/Home";
import Editorial from "./pages/Editorial";
import "./styles/nsikay-auth.css";

import "./styles/nsikay-modules-v2.css";
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
                ÃƒÂ¢Ã¢â‚¬Â Ã‚Â Retour ÃƒÆ’Ã‚Â  mon espace
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
<Route path="/editorial" element={<Editorial />} />
<Route path="/editorial/:category" element={<Editorial />} />
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
                                    title="MÃƒÆ’Ã‚Â©tiers"
                                    icon="ÃƒÂ°Ã…Â¸Ã‚Â§Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ°Ã…Â¸Ã¢â‚¬â„¢Ã‚Â¼"
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
                                    icon="ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂºÃ‚Â¡ÃƒÂ¯Ã‚Â¸Ã‚Â"
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
                                    icon="ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂºÃ¢â‚¬â„¢"
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
                                    icon="ÃƒÂ°Ã…Â¸Ã¢â‚¬â„¢Ã‚Â°"
                                />
                            </ProtectedRoute>
                        }
                    />
<Route
                        path="/events"
                        element={
                            <ProtectedRoute>
                                <Placeholder
                                    title="ÃƒÆ’Ã¢â‚¬Â°vÃƒÆ’Ã‚Â©nements"
                                    icon="ÃƒÂ°Ã…Â¸Ã…Â½Ã‚Â«"
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
                title="PublicitÃ©"
                icon="ðŸ“¢"
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



















