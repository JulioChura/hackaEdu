import axios from "axios";

const URL = "http://localhost:8000";

const api = axios.create({
    baseURL: URL,
});

// ─── Request interceptor: attach access token ─────────────────────────────────
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ─── Token refresh logic ───────────────────────────────────────────────────────
// Track whether a refresh is already in-flight so we don't send multiple at once.
let _isRefreshing = false;
// Queue of { resolve, reject } pairs for requests that arrived while refreshing.
let _refreshQueue = [];

function _processQueue(error, token = null) {
    _refreshQueue.forEach(({ resolve, reject }) => {
        if (error) {
            reject(error);
        } else {
            resolve(token);
        }
    });
    _refreshQueue = [];
}

function _clearSession() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
}

// ─── Response interceptor: auto-refresh on 401 ───────────────────────────────
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Not a 401, or already tried to refresh once → give up.
        if (error.response?.status !== 401 || originalRequest._retried) {
            return Promise.reject(error);
        }

        const refreshToken = localStorage.getItem("refresh_token");

        // No refresh token available → logout immediately.
        if (!refreshToken) {
            _clearSession();
            return Promise.reject(error);
        }

        // If a refresh is already running, queue this request.
        if (_isRefreshing) {
            return new Promise((resolve, reject) => {
                _refreshQueue.push({
                    resolve: (newToken) => {
                        originalRequest.headers.Authorization = `Bearer ${newToken}`;
                        resolve(api(originalRequest));
                    },
                    reject,
                });
            });
        }

        // Start a fresh refresh cycle.
        originalRequest._retried = true;
        _isRefreshing = true;

        try {
            const { data } = await axios.post(`${URL}/auth/token/refresh/`, {
                refresh: refreshToken,
            });

            const newAccess = data.access;
            localStorage.setItem("access_token", newAccess);

            // Update the default header for future requests.
            api.defaults.headers.common["Authorization"] = `Bearer ${newAccess}`;

            // Unblock all queued requests.
            _processQueue(null, newAccess);

            // Retry the original request.
            originalRequest.headers.Authorization = `Bearer ${newAccess}`;
            return api(originalRequest);
        } catch (refreshError) {
            // Refresh failed → clear everything and redirect to login.
            _processQueue(refreshError, null);
            _clearSession();
            return Promise.reject(refreshError);
        } finally {
            _isRefreshing = false;
        }
    }
);

export default api;