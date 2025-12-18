<template>
  <div class="p-6 rounded-xl border border-gray-200 shadow-lg bg-white">
    <!-- Simple Signup Form -->
    <form @submit.prevent="submitSignup" class="flex flex-col gap-5">
      <div class="flex flex-col gap-1.5">
        <label class="text-sm font-semibold text-brand-dark ml-1">Nombre completo</label>
        <input v-model="name" class="w-full h-12 rounded-full border border-gray-200 bg-background-light px-4 text-brand-dark placeholder:text-gray-400 focus:border-brand-blue focus:ring-0 text-sm transition-colors" placeholder="Tu nombre completo" type="text"/>
      </div>

      <div class="flex flex-col gap-1.5">
        <label class="text-sm font-semibold text-brand-dark ml-1">Correo electrónico</label>
        <input v-model="email" class="w-full h-12 rounded-full border border-gray-200 bg-background-light px-4 text-brand-dark placeholder:text-gray-400 focus:border-brand-blue focus:ring-0 text-sm transition-colors" placeholder="ejemplo@escuela.edu" type="email"/>
      </div>

      <div class="flex flex-col gap-1.5">
        <label class="text-sm font-semibold text-brand-dark ml-1">Contraseña</label>
        <input v-model="password" class="w-full h-12 rounded-full border border-gray-200 bg-background-light px-4 text-brand-dark placeholder:text-gray-400 focus:border-brand-blue focus:ring-0 text-sm transition-colors" placeholder="Crear una contraseña" type="password"/>
      </div>

      <div class="flex flex-col sm:flex-row gap-2">
        <button type="button" class="w-full sm:flex-1 h-12 rounded-full border border-gray-200 hover:bg-gray-50">Cancelar</button>
        <button type="submit" class="w-full sm:flex-1 h-12 rounded-full bg-blue-700 hover:bg-blue-800 text-white font-bold shadow-lg">Crear cuenta</button>
      </div>
    </form>

    <div class="mt-4 text-center text-sm text-gray-500">
      <p>¿Ya tienes cuenta? <button class="font-bold text-brand-blue ml-1" @click="$emit('show-login')">Inicia sesión</button></p>
    </div>
  </div>
</template>

<script setup>
const emits = defineEmits(['show-login', 'submit'])
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')

function submitSignup() {
  emits('submit', { type: 'signup', name: name.value, email: email.value, password: password.value })
}
</script>

<style scoped>
</style>
