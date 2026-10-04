import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import api from "../services/api";

const AuthContext = createContext(null);

const CERTIFICATION_AUTHORITY_GROUPS = [
    "Autorité Certification",
    "Super Administrateur",
];

function getUserGroups(user) {
    if (!user) {
        return [];
    }

    if (Array.isArray(user.groups)) {
        return user.groups;
    }

    if (Array.isArray(user.group_names)) {
        return user.group_names;
    }

    if (user.user && Array.isArray(user.user.groups)) {
        return user.user.groups;
    }

    return [];
}

function hasGroup(user, allowedGroups) {
    const groups = getUserGroups(user);

    return groups.some(
        (group) => allowedGroups.includes(group)
    );
}

function isCertificationAuthorityUser(user) {
    if (!user) {
        return false;
    }

    if (user.is_superuser === true) {
        return true;
    }

    return hasGroup(
        user,
        CERTIFICATION_AUTHORITY_GROUPS
    );
}

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

    const isCertificationAuthority =
        isCertificationAuthorityUser(user);

    const userGroups = getUserGroups(user);

    return (
        <AuthContext.Provider
            value={{
                user,
                profile,
                loading,

                userGroups,

                isAuthenticated:
                    Boolean(user) || isAuthenticated,

                isCertificationAuthority,

                isSuperuser:
                    Boolean(user?.is_superuser),

                isStaff:
                    Boolean(user?.is_staff),

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
