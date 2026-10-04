import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import ProtectedRoleRoute from "./components/ProtectedRoleRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />


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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />



                    <Route
                        path="/connexion"
                        element={<Login />}
                    />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />



                    <Route
                        path="/inscription"
                        element={<Register />}
                    />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
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
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />


                <Route
    path="/camera"
    element={
        <ProtectedRoute>
            <NSIKAYCamera />
        </ProtectedRoute>
    }
/>
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />

            <Route
                path="/mot-de-passe-oublie"
                element={<ForgotPassword />}
            />
            <Route
                path="/reinitialiser-mot-de-passe"
                element={<ResetPassword />}
            />


        <Route path="/media-library" element={<MediaLibrary />} />
      </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}















