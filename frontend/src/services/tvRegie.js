import API from "./api";

/*
 * ============================================================
 * NSIKAY TV REGIE
 * Connexion React -> Django
 * ============================================================
 */

/* ------------------------------------------------------------
 * CAMERAS
 * ------------------------------------------------------------ */

export function getCameras() {
    return API.get("/tv-regie/cameras/");
}

export function getCamera(id) {
    return API.get(`/tv-regie/cameras/${id}/`);
}

export function createCamera(payload) {
    return API.post("/tv-regie/cameras/", payload);
}

export function updateCamera(id, payload) {
    return API.patch(`/tv-regie/cameras/${id}/`, payload);
}

export function deleteCamera(id) {
    return API.delete(`/tv-regie/cameras/${id}/`);
}


/* ------------------------------------------------------------
 * LIVE STREAMS
 * ------------------------------------------------------------ */

export function getStreams() {
    return API.get("/tv-regie/streams/");
}

export function getStream(id) {
    return API.get(`/tv-regie/streams/${id}/`);
}

export function createStream(payload) {
    return API.post("/tv-regie/streams/", payload);
}

export function updateStream(id, payload) {
    return API.patch(`/tv-regie/streams/${id}/`, payload);
}

export function deleteStream(id) {
    return API.delete(`/tv-regie/streams/${id}/`);
}


/* ------------------------------------------------------------
 * PUBLICATION TV
 * ------------------------------------------------------------ */

export function publishStream(id, channelId) {
    return API.post(
        `/tv-regie/streams/${id}/publish/`,
        {
            channel_id: channelId,
        }
    );
}

export function unpublishStream(id) {
    return API.post(
        `/tv-regie/streams/${id}/unpublish/`,
        {}
    );
}


/* ------------------------------------------------------------
 * EFFETS
 * ------------------------------------------------------------ */

export function getEffects() {
    return API.get("/tv-regie/effects/");
}

export function createEffect(payload) {
    return API.post("/tv-regie/effects/", payload);
}

export function updateEffect(id, payload) {
    return API.patch(`/tv-regie/effects/${id}/`, payload);
}

export function deleteEffect(id) {
    return API.delete(`/tv-regie/effects/${id}/`);
}


/* ------------------------------------------------------------
 * ANIMATIONS
 * ------------------------------------------------------------ */

export function getAnimations() {
    return API.get("/tv-regie/animations/");
}

export function createAnimation(payload) {
    return API.post("/tv-regie/animations/", payload);
}

export function updateAnimation(id, payload) {
    return API.patch(`/tv-regie/animations/${id}/`, payload);
}

export function deleteAnimation(id) {
    return API.delete(`/tv-regie/animations/${id}/`);
}


/* ------------------------------------------------------------
 * AUDIO
 * ------------------------------------------------------------ */

export function getAudioControls() {
    return API.get("/tv-regie/audio/");
}

export function createAudioControl(payload) {
    return API.post("/tv-regie/audio/", payload);
}

export function updateAudioControl(id, payload) {
    return API.patch(`/tv-regie/audio/${id}/`, payload);
}

export function deleteAudioControl(id) {
    return API.delete(`/tv-regie/audio/${id}/`);
}


/* ------------------------------------------------------------
 * SCENES
 * ------------------------------------------------------------ */

export function getScenes() {
    return API.get("/tv-regie/scenes/");
}

export function createScene(payload) {
    return API.post("/tv-regie/scenes/", payload);
}

export function updateScene(id, payload) {
    return API.patch(`/tv-regie/scenes/${id}/`, payload);
}

export function deleteScene(id) {
    return API.delete(`/tv-regie/scenes/${id}/`);
}


/* ------------------------------------------------------------
 * PROGRAMMATION
 * ------------------------------------------------------------ */

export function getSchedules() {
    return API.get("/tv-regie/schedules/");
}

export function createSchedule(payload) {
    return API.post("/tv-regie/schedules/", payload);
}

export function updateSchedule(id, payload) {
    return API.patch(`/tv-regie/schedules/${id}/`, payload);
}

export function deleteSchedule(id) {
    return API.delete(`/tv-regie/schedules/${id}/`);
}

/* ============================================================
   NSIKAY BROADCAST CENTRAL
   API DIFFUSION EDITORIALE
   ============================================================ */

export function getCentralBroadcasts() {
    return API.get("/tv-regie/broadcasts/");
}

export function getCentralBroadcast(id) {
    return API.get(`/tv-regie/broadcasts/${id}/`);
}

export function createCentralBroadcast(payload) {
    return API.post("/tv-regie/broadcasts/", payload);
}

export function updateCentralBroadcast(id, payload) {
    return API.patch(`/tv-regie/broadcasts/${id}/`, payload);
}

export function startCentralBroadcast(id) {
    return API.post(`/tv-regie/broadcasts/${id}/start/`, {});
}

export function stopCentralBroadcast(id) {
    return API.post(`/tv-regie/broadcasts/${id}/stop/`, {});
}

export function deleteCentralBroadcast(id) {
    return API.delete(`/tv-regie/broadcasts/${id}/`);
}
