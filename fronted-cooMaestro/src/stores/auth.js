// stores/auth.js - Store de autenticación con Pinia
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '../services/auth';

export const useAuthStore = defineStore('auth', () => {
  // Estado
  const user = ref(null);
  const isLoading = ref(false);
  const error = ref(null);
  const isAuthenticated = computed(() => !!user.value);

  // Acciones
  const register = async (userData) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await authService.register(userData);
      user.value = {
        id: response.id,
        email: response.email,
        nombre: response.nombre,
        apellido: response.apellido,
      };
      return response;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error en el registro';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (email, password) => {
    isLoading.value = true;
    error.value = null;
    try {
      await authService.login(email, password);
      // Obtener datos del perfil
      const profileData = await authService.getProfile();
      user.value = profileData;
      return profileData;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error en el login';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    authService.logout();
    user.value = null;
    error.value = null;
  };

  const loadProfile = async () => {
    if (!authService.isAuthenticated()) {
      return;
    }
    isLoading.value = true;
    try {
      const profileData = await authService.getProfile();
      user.value = profileData;
    } catch (err) {
      logout();
    } finally {
      isLoading.value = false;
    }
  };

  const updateProfile = async (profileData) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await authService.updateProfile(profileData);
      user.value = { ...user.value, ...response };
      return response;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al actualizar perfil';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const changePassword = async (oldPassword, newPassword, newPasswordConfirm) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await authService.changePassword(
        oldPassword,
        newPassword,
        newPasswordConfirm
      );
      return response;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al cambiar contraseña';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Inicializar: cargar perfil si hay token
  if (authService.isAuthenticated()) {
    loadProfile();
  }

  return {
    // Estado
    user,
    isLoading,
    error,
    isAuthenticated,

    // Acciones
    register,
    login,
    logout,
    loadProfile,
    updateProfile,
    changePassword,
  };
});
