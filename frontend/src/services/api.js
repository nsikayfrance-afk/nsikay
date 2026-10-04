const API_BASE = "/api";

async function request(url, options = {}) {
    const token = localStorage.getItem("nsikay_token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (token) {
        headers.Authorization = `Token ${token}`;
    }

    const response = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers,
    });

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.message ||
            data?.error ||
            "Une erreur est survenue.";

        throw new Error(message);
    }

    return data;
}

/*
 * Routes Django hors prÃ©fixe /api/
 * Exemple :
 *   /wenze/
 *   /finance/
 *   /marketing/
 *   /banking/
 *   /certification/
 */
async function rootRequest(url, options = {}) {
    const token = localStorage.getItem("nsikay_token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (token) {
        headers.Authorization = `Token ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers,
    });

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.message ||
            data?.error ||
            "Une erreur est survenue.";

        throw new Error(message);
    }

    return data;
}

export const api = {
    /*
     * --------------------------------------------------------
     * API /api/
     * --------------------------------------------------------
     */

    get(url, options = {}) {
        return request(url, {
            ...options,
            method: "GET",
        });
    },

    post(url, payload, options = {}) {
        return request(url, {
            ...options,
            method: "POST",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
        });
    },

    patch(url, payload, options = {}) {
        return request(url, {
            ...options,
            method: "PATCH",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
        });
    },

    put(url, payload, options = {}) {
        return request(url, {
            ...options,
            method: "PUT",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
        });
    },

    delete(url, options = {}) {
        return request(url, {
            ...options,
            method: "DELETE",
        });
    },

    /*
     * --------------------------------------------------------
     * Routes Django racine
     * --------------------------------------------------------
     */

    rootGet(url, options = {}) {
        return rootRequest(url, {
            ...options,
            method: "GET",
        });
    },

    rootPost(url, payload, options = {}) {
        return rootRequest(url, {
            ...options,
            method: "POST",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
        });
    },

    rootPatch(url, payload, options = {}) {
        return rootRequest(url, {
            ...options,
            method: "PATCH",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
        });
    },

    rootDelete(url, options = {}) {
        return rootRequest(url, {
            ...options,
            method: "DELETE",
        });
    },

    /*
     * --------------------------------------------------------
     * AUTHENTIFICATION
     * --------------------------------------------------------
     */

    register(payload) {
        return request("/auth/register/", {
            method: "POST",
            body:
                payload instanceof FormData
                    ? payload
                    : JSON.stringify(payload),
            headers:
                payload instanceof FormData
                    ? {}
                    : undefined,
        });
    },

    login(payload) {
        return request("/auth/login/", {
            method: "POST",
            body: JSON.stringify(payload),
        });
    },

    logout() {
        return request("/auth/logout/", {
            method: "POST",
        });
    },

    me() {
        return request("/auth/me/");
    },

    /*
     * --------------------------------------------------------
     * PROFIL
     * --------------------------------------------------------
     */

    profile() {
        return request("/profile/");
    },

    updateProfile(payload) {
        return request("/profile/update/", {
            method: "PATCH",
            body: JSON.stringify(payload),
        });
    },

    /*
     * --------------------------------------------------------
     * DONNEES API EXISTANTES
     * --------------------------------------------------------
     */

    users() {
        return request("/users/");
    },

    banks() {
        return request("/banks/");
    },

    countries() {
        return request("/countries/");
    },

    certifications() {
        return request("/certifications/");
    },

    transactions() {
        return request("/transactions/");
    },

    finance() {
        return request("/finance/");
    },

    /*
     * --------------------------------------------------------
     * PROFILS SPECIALISES
     * --------------------------------------------------------
     */

    profiles() {
        return request("/profiles/");
    },

    createProfile(data) {
        return request("/profiles/", {
            method: "POST",
            body: JSON.stringify(data),
        });
    },

    updateProfileItem(id, data) {
        return request(`/profiles/${id}/`, {
            method: "PATCH",
            body: JSON.stringify(data),
        });
    },

    deleteProfileItem(id) {
        return request(`/profiles/${id}/`, {
            method: "DELETE",
        });
    },
};


/* ============================================================
 * NSIKAY - RECUPERATION SECURISEE DU MOT DE PASSE
 * ============================================================ */

api.passwordRecoveryRequest = function(identifier) {
    return request("/auth/password-recovery/request/", {
        method: "POST",
        body: JSON.stringify({
            identifier,
        }),
    });
};

api.passwordRecoveryVerify = function(recoveryId, code) {
    return request("/auth/password-recovery/verify/", {
        method: "POST",
        body: JSON.stringify({
            recovery_id: recoveryId,
            code,
        }),
    });
};

api.passwordRecoveryReset = function(
    recoveryId,
    code,
    password,
    passwordConfirm
) {
    return request("/auth/password-recovery/reset/", {
        method: "POST",
        body: JSON.stringify({
            recovery_id: recoveryId,
            code,
            password,
            password_confirm: passwordConfirm,
        }),
    });
};
export default api;
