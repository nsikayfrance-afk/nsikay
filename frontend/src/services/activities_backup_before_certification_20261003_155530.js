import API from "./api";

/*
 * ============================================================
 * NSIKAY - ACTIVITES
 * ============================================================
 *
 * Django :
 *
 * /api/activities/
 * /api/activities/<id>/
 * /api/activities/dashboard/
 *
 * Services :
 *
 * /api/activities/services/
 * /api/activities/services/<id>/
 *
 * Projets :
 *
 * /api/activities/projects/
 * /api/activities/projects/<id>/
 */

export const listActivities = (params = {}) => {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (
            value !== undefined &&
            value !== null &&
            String(value).trim() !== ""
        ) {
            query.set(key, value);
        }
    });

    const suffix = query.toString()
        ? `?${query.toString()}`
        : "";

    return API.get(`/activities/${suffix}`);
};

export const getActivity = (id) => {
    return API.get(`/activities/${id}/`);
};

export const createActivity = (payload) => {
    return API.post("/activities/", payload);
};

export const updateActivity = (id, payload) => {
    return API.patch(`/activities/${id}/`, payload);
};

export const deleteActivity = (id) => {
    return API.delete(`/activities/${id}/`);
};

export const getActivityDashboard = () => {
    return API.get("/activities/dashboard/");
};

/*
 * ------------------------------------------------------------
 * SERVICES
 * ------------------------------------------------------------
 */

export const listServices = (params = {}) => {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (
            value !== undefined &&
            value !== null &&
            String(value).trim() !== ""
        ) {
            query.set(key, value);
        }
    });

    const suffix = query.toString()
        ? `?${query.toString()}`
        : "";

    return API.get(`/activities/services/${suffix}`);
};

export const getService = (id) => {
    return API.get(`/activities/services/${id}/`);
};

export const createService = (payload) => {
    return API.post("/activities/services/", payload);
};

export const updateService = (id, payload) => {
    return API.patch(`/activities/services/${id}/`, payload);
};

export const deleteService = (id) => {
    return API.delete(`/activities/services/${id}/`);
};

/*
 * ------------------------------------------------------------
 * PROJETS
 * ------------------------------------------------------------
 */

export const listProjects = (params = {}) => {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (
            value !== undefined &&
            value !== null &&
            String(value).trim() !== ""
        ) {
            query.set(key, value);
        }
    });

    const suffix = query.toString()
        ? `?${query.toString()}`
        : "";

    return API.get(`/activities/projects/${suffix}`);
};

export const getProject = (id) => {
    return API.get(`/activities/projects/${id}/`);
};

export const createProject = (payload) => {
    return API.post("/activities/projects/", payload);
};

export const updateProject = (id, payload) => {
    return API.patch(`/activities/projects/${id}/`, payload);
};

export const deleteProject = (id) => {
    return API.delete(`/activities/projects/${id}/`);
};