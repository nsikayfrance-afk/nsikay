import api from "./api";

const financeApi = {
    status() {
        return api.get("/nsikay/finance/status/");
    },

    dashboard() {
        return api.get("/finance/");
    },

    wallet() {
        return api.get("/nsikay/wallet/dashboard/");
    },

    walletBalance() {
        return api.get("/nsikay/wallet/balance/");
    },

    banks() {
        return api.get("/banks/");
    },

    countries() {
        return api.get("/countries/");
    },

    transactions() {
        return api.get("/transactions/");
    },

    deposit(amount, currency = "USD") {
        return api.post("/nsikay/wallet/operations/deposit/", {
            amount,
            currency,
        });
    },

    withdraw(amount, currency = "USD") {
        return api.post("/nsikay/wallet/operations/withdraw/", {
            amount,
            currency,
        });
    },

    transfer(amount, currency = "USD", recipient = "") {
        return api.post("/nsikay/wallet/operations/transfer/", {
            amount,
            currency,
            recipient,
        });
    },

    walletBanks(walletId) {
        return api.get(`/nsikay/wallet/banks/${walletId}/`);
    },
};

export default financeApi;
