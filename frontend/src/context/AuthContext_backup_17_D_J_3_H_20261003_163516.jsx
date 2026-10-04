import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    const isAuthenticated = Boolean(
        localStorage.getItem("nsikay_token")
    );

    async function loadSession() {
        const token = localStorage.getItem("nsikay_token");

        if (!token) {
            setUser(null);
            setProfile(null);
            setLoading(false);
            return;
        }

        try {
            const me = await api.me();

            setUser(me);

            try {
                const currentProfile = await api.profile();
                setProfile(currentProfile);
            } catch {
                setProfile(null);
            }
        } catch {
            localStorage.removeItem("nsikay_token");
            setUser(null);
            setProfile(null);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadSession();
    }, []);

    async function login(username, password) {
        const result = await api.login({
            username,
            password,
        });

        if (result.token) {
            localStorage.setItem("nsikay_token", result.token);
        }

        await loadSession();

        return result;
    }

    async function register(payload) {
        const result = await api.register(payload);

        if (result.token) {
            localStorage.setItem("nsikay_token", result.token);
            await loadSession();
        }

        return result;
    }

    async function logout() {
        try {
            await api.logout();
        } catch {
            // La session locale sera tout de même supprimée.
        }

        localStorage.removeItem("nsikay_token");

        setUser(null);
        setProfile(null);
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                profile,
                loading,
                isAuthenticated: Boolean(user) || isAuthenticated,
                login,
                register,
                logout,
                reload: loadSession,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
