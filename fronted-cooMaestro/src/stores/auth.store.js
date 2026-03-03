import { defineStore } from "pinia";
import { authService } from "../services/auth.service";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        loading: false,
        error: null,
        isAuthenticated: !!localStorage.getItem("access_token"),
    }),

    getters: {
        isLoggedIn: (state) => state.isAuthenticated,
        getCurrentUser: (state) => state.user,
        getLoading: (state) => state.loading,
        getError: (state) => state.error,
    },

    actions: {
        async login(credentials) {
            this.loading = true;
            this.error = null;
            try {
                const response = await authService.login(credentials);
                const data = response.data;

                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh);

                this.isAuthenticated = true;
                await this.loadProfile();

                return data;
            } catch (error) {
                this.error = error.response?.data?.detail || "Invalid credentials";
                this.isAuthenticated = false;
                throw error;
            } finally {
                this.loading = false;
            }
        },

        // Call this once at app startup to restore session state.
        async initSession() {
            const token = localStorage.getItem("access_token");
            if (!token) {
                this.isAuthenticated = false;
                return;
            }
            // Try to load the profile using the stored token.
            // The axios interceptor will transparently refresh it if expired.
            try {
                await this.loadProfile();
                this.isAuthenticated = true;
            } catch {
                // Profile load failed even after potential refresh → session dead.
                this.isAuthenticated = false;
                this.user = null;
            }
        },

        async loadProfile() {
            try {
                const response = await authService.profile();
                this.user = response.data;
                return response.data;
            } catch (error) {
                console.error("Error loading profile:", error);
                this.user = null;
                throw error;
            }
        },

        logout() {
            authService.logout();
            this.user = null;
            this.isAuthenticated = false;
            this.error = null;
        },

        clearError() {
            this.error = null;
        },
    },
});
