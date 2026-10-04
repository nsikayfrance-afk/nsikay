import API from "./api";

const membershipApi = {
    types() {
        return API.get("/association/membership/types/");
    },

    me() {
        return API.get("/association/membership/");
    },

    apply(membershipType, message = "") {
        return API.post(
            "/association/membership/apply/",
            {
                membership_type: membershipType,
                message,
            }
        );
    },

    async card() {
        try {
            return await API.get(
                "/association/membership/card/"
            );
        } catch {
            return null;
        }
    },

    verify(token) {
        return API.get(
            `/association/membership/verify/${token}/`
        );
    },

    applications() {
        return API.get(
            "/association/membership/applications/"
        );
    },
};

export default membershipApi;
