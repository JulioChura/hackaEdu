<template>
  <div>
    <!-- Backdrop for mobile when sidebar is open -->
    <div
      v-if="open"
      class="fixed inset-0 md:hidden bg-[rgba(236,232,232,0.44)] z-40"
      @click="$emit('close')"
      aria-hidden="true"
    ></div>

    <aside
      :class="[
          'fixed left-0 top-0 inset-y-0 h-screen flex flex-col w-screen md:w-72 p-4 border-r border-border-light dark:border-border-dark bg-gray-50 dark:bg-gray-50 shadow-lg transform transition-transform duration-200 z-50',
        open ? 'translate-x-0' : '-translate-x-full',
        'md:translate-x-0'
      ]"
      role="navigation"
      aria-label="Panel lateral"
    >
      <!-- Close button visible only on small screens -->
      <button
        class="md:hidden self-end p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 -mr-2 -mt-2"
        @click="$emit('close')"
        aria-label="Cerrar menú"
      >
        <span class="material-symbols-outlined">close</span>
      </button>

      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-3 p-2">
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-12 h-12"
            data-alt="Profile picture of Laura Hernández"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDQqoyi3A00umFhiNc-MmER93L5oqbjnc7l_D1NJpiGAjIaR9QovdrJuZfk-1Hpwd7Xz1YS-fkrZZFYkckzsiHWqSHkFFRc3F2jjx6WZhTAYkyPLvJb4AMAKPZJNux1iHTUDIR_gw3bmYVWFRF4WZcIkKuGKZKqWY2TLx4shyeUP3zYlalyyACDDs6wnmkqTqaO3WcCLiiTVFFyZKPnKqGjFpb2v3TLrHBKLTllMsL5FvGSPQHQTVUXDRq2JbioRl9_Fxa096CCp3I");'
          ></div>
          <div class="flex flex-col">
            <h1 class="text-text-primary-light dark:text-text-primary-dark text-base font-semibold">Laura Hernández</h1>
            <p class="text-text-secondary-light dark:text-text-secondary-dark text-sm">Profesora</p>
          </div>
        </div>
        <nav class="flex flex-col gap-2 mt-4">
          <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-200 dark:hover:bg-blue-800" href="#">
            <span class="material-symbols-outlined text-text-primary-light dark:text-text-primary-dark">dashboard</span>
            <p class="text-text-primary-light dark:text-text-primary-dark text-sm font-medium">Dashboard</p>
          </a>
          <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-gray-200 dark:bg-blue-800 text-blue-900 dark:text-gray-100" href="#">
            <span class="material-symbols-outlined !font-bold">school</span>
            <p class="text-sm font-semibold">Cursos</p>
          </a>
          <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-200 dark:hover:bg-blue-800" href="#">
            <span class="material-symbols-outlined text-text-primary-light dark:text-text-primary-dark">groups</span>
            <p class="text-text-primary-light dark:text-text-primary-dark text-sm font-medium">Estudiantes</p>
          </a>
          <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-200 dark:hover:bg-blue-800" href="#">
            <span class="material-symbols-outlined text-text-primary-light dark:text-text-primary-dark">bar_chart</span>
            <p class="text-text-primary-light dark:text-text-primary-dark text-sm font-medium">Reportes</p>
          </a>
        </nav>
      </div>

      <div class="mt-auto flex flex-col gap-1">
        <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800" href="#">
          <span class="material-symbols-outlined text-text-primary-light dark:text-text-primary-dark">settings</span>
          <p class="text-text-primary-light dark:text-text-primary-dark text-sm font-medium">Configuración</p>
        </a>
        <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800" href="#">
          <span class="material-symbols-outlined text-text-primary-light dark:text-text-primary-dark">help</span>
          <p class="text-text-primary-light dark:text-text-primary-dark text-sm font-medium">Ayuda</p>
        </a>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { computed } from 'vue'

defineProps({
  open: { type: Boolean, default: true }
})
defineEmits(['close'])


function getBgColor() {
  // Fallback background in case utility classes are missing
  return document.documentElement.classList.contains('dark') ? '#0f172a' : '#ffffff'
}
</script>

<style scoped>
/* Tailwind handles the bulk of styles; keep this file scoped-clean. */
</style>
