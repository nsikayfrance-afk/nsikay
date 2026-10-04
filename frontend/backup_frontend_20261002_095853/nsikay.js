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
