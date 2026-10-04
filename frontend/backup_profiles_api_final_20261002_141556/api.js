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

export const api = {
    register(payload) {
        return request("/auth/register/", {
            method: "POST",
            body: JSON.stringify(payload),
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

    profile() {
        return request("/profile/");
    },

    updateProfile(payload) {
        return request("/profile/update/", {
            method: "PATCH",
            body: JSON.stringify(payload),
        });
    },

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

    profiles: async () => {
        return request("/profiles/");
    },

    createProfile: async (data) => {
        return request("/profiles/", {
            method: "POST",
            body: JSON.stringify(data),
        });
    },

    updateProfileItem: async (id, data) => {
        return request(/profiles//, {
            method: "PATCH",
            body: JSON.stringify(data),
        });
    },

    deleteProfileItem: async (id) => {
        return request(/profiles//, {
            method: "DELETE",
        });
    },
};

export default api;

,
      body: JSON.stringify(data),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(
        payload?.display_name?.[0] ||
        payload?.detail ||
        "Impossible de créer le profil."
      );
    }

    return payload;
  },
      body: JSON.stringify(data),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(
        payload?.detail ||
        "Impossible de modifier le profil."
      );
    }

    return payload;
  },

