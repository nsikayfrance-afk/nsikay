import API from "./api";

export function getMediaAssets(params = {}) {
    return API.get("/media-library/assets/", { params });
}

export function getMediaAsset(id) {
    return API.get(`/media-library/assets/${id}/`);
}

export function createMediaAsset(formData) {
    return API.post("/media-library/assets/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
}

export function updateMediaAsset(id, formData) {
    return API.patch(`/media-library/assets/${id}/`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
}

export function deleteMediaAsset(id) {
    return API.delete(`/media-library/assets/${id}/`);
}

export function getMediaDestinations() {
    return API.get("/media-library/destinations/");
}

export function setMediaDestinations(id, destinationIds) {
    return API.post(
        `/media-library/assets/${id}/set-destinations/`,
        {
            destination_ids: destinationIds,
        }
    );
}

export function getMediaDistributions(params = {}) {
    return API.get("/media-library/distributions/", { params });
}

export function markDistributionLive(id) {
    return API.post(
        `/media-library/distributions/${id}/mark-live/`,
        {}
    );
}

export function markDistributionPublished(id) {
    return API.post(
        `/media-library/distributions/${id}/mark-published/`,
        {}
    );
}

export function markDistributionFailed(id, message = "") {
    return API.post(
        `/media-library/distributions/${id}/mark-failed/`,
        {
            message,
        }
    );
}

export function getMediaSegments(params = {}) {
    return API.get("/media-library/segments/", { params });
}

export function createMediaSegment(payload) {
    return API.post(
        "/media-library/segments/",
        payload
    );
}

export function updateMediaSegment(id, payload) {
    return API.patch(
        `/media-library/segments/${id}/`,
        payload
    );
}

export function deleteMediaSegment(id) {
    return API.delete(
        `/media-library/segments/${id}/`
    );
}