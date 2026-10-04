import API from "./api";

export const getWenzeProducts = () => {
    return API.get("/wenze/");
};

export const getTVChannels = () => {
    return API.get("/api/tv-regie/");
};

export const getFinance = () => {
    return API.get("/finance/");
};

export const getMarketing = () => {
    return API.get("/marketing/");
};

/*
 * Préparation de l'inscription NSIKAY.
 *
 * L'URL exacte du endpoint Django sera raccordée après
 * vérification des routes d'authentification du backend.
 */
export const registerNsikayUser = (formData) => {
    return API.post("/api/auth/register/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
};

export const loginNsikayUser = (payload) => {
    return API.post("/api/auth/login/", payload);
};
