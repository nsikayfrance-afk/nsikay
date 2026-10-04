import { Navigate } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoleRoute({
    children,
    allowed,
    redirectTo = "/espace",
}) {
    const { loading } = useAuth();

    if (loading) {
        return null;
    }

    return (
        <ProtectedRoute>
            <RoleGate
                allowed={allowed}
                redirectTo={redirectTo}
            >
                {children}
            </RoleGate>
        </ProtectedRoute>
    );
}

function RoleGate({
    children,
    allowed,
    redirectTo,
}) {
    const {
        isCertificationAuthority,
    } = useAuth();

    const authorized =
        allowed?.includes("certification_authority")
            ? isCertificationAuthority
            : false;

    if (!authorized) {
        return (
            <Navigate
                to={redirectTo}
                replace
            />
        );
    }

    return children;
}
