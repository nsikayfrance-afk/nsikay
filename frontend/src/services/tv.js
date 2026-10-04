import API from "./api";

export const getTVChannels = async () => {
    return API.get("/tv/channels/");
};
