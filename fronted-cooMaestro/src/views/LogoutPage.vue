<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-background-light dark:bg-background-dark px-4 py-8">
    <div class="w-full max-w-md bg-white dark:bg-slate-900 rounded-2xl shadow-glass p-8 flex flex-col items-center gap-6 transition-all duration-300 ease-in-out">
      <span class="material-symbols-outlined text-primary text-6xl mb-2">logout</span>
      <h1 class="text-2xl font-bold text-primary mb-2">¿Seguro que quieres cerrar sesión?</h1>
      <p class="text-slate-600 dark:text-slate-300 text-center mb-4">Tu progreso se guardará y podrás volver a iniciar sesión cuando quieras.</p>
      <div class="flex flex-col sm:flex-row gap-3 w-full">
        <button @click="handleLogout" class="w-full sm:w-auto h-12 px-6 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow transition-all duration-200 ease-in-out active:scale-95 flex items-center justify-center gap-2">
          <span>Cerrar sesión</span>
          <span class="material-symbols-outlined text-xl">logout</span>
        </button>
        <router-link to="/" class="w-full sm:w-auto h-12 px-6 bg-background-subtle hover:bg-background-light text-primary font-bold rounded-xl shadow transition-all duration-200 ease-in-out active:scale-95 flex items-center justify-center gap-2 border border-primary/20">
          Cancelar
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'
const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.shadow-glass {
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
}
@media (max-width: 540px) {
  .max-w-md {
    max-width: 95vw;
  }
}
</style>
