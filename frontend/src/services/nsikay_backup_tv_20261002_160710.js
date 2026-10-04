import API from "./api";

/*
 * ============================================================
 * SERVICES NSIKAY EXISTANTS
 * ============================================================
 *
 * Les modules Django suivants sont montÃ©s Ã  la racine :
 *
 * /wenze/
 * /finance/
 * /marketing/
 *
 * Ils ne doivent donc pas recevoir automatiquement /api.
 */

export const getWenzeProducts = () => {
    return API.rootGet("/wenze/");
};

export const getTVChannels = () => {
    return API.get("/tv/");
};

export const getFinance = () => {
    return API.rootGet("/finance/");
};

export const getMarketing = () => {
    return API.rootGet("/marketing/");
};

/*
 * Authentification
 */
export const registerNsikayUser = (formData) => {
    return API.post("/auth/register/", formData, {
        headers:
            formData instanceof FormData
                ? {}
                : {
                      "Content-Type": "application/json",
                  },
    });
};

export const loginNsikayUser = (payload) => {
    return API.post("/auth/login/", payload);
};