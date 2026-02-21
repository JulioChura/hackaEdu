import { defineStore } from "pinia";
import { authService } from "../services/auth.service";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        loading: false,
        error: null,
        isAuthenticated: !!localStorage.getItem("access_token")
    }),

    getters: {
        isLoggedIn: (state) => state.isAuthenticated,
        getCurrentUser: (state) => state.user,
        getLoading: (state) => state.loading,
        getError: (state) => state.error
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
                this.error = error.response?.data?.detail || "Credenciales inválidas";
                this.isAuthenticated = false;
                throw error;
            } finally {
                this.loading = false;
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
        }
    }
})