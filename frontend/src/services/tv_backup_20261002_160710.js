import API from "./api";

export const getTVChannels = async () => {
    return API.get("/tv/");
};

export const getTVChannel = async (id) => {
    return API.get(`/tv/${id}/`);
};

export const createTVChannel = async (payload) => {
    return API.post("/tv/", payload);
};

export const updateTVChannel = async (id, payload) => {
    return API.patch(`/tv/${id}/`, payload);
};

export const deleteTVChannel = async (id) => {
    return API.delete(`/tv/${id}/`);
};