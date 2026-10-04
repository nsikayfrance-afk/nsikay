import axios from "axios";

const API = axios.create({
    baseURL: "",
    headers: {
        "Accept": "application/json",
    },
    timeout: 15000,
});

export default API;
