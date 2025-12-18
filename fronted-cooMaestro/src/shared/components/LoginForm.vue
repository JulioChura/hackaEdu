<template>
  <div class="p-6 rounded-xl border border-gray-200 shadow-lg bg-white mx-auto w-full text-center sm:text-left">
    <!-- Role Selector -->
    <div class="flex p-1 bg-background-light rounded-full border border-gray-100 mb-4">
      <label class="flex-1 cursor-pointer">
        <input v-model="role" class="peer sr-only" name="role" type="radio" value="teacher" />
        <div :class="role==='teacher' ? activeClass : inactiveClass" class="flex items-center justify-center gap-2 py-2.5 px-4 rounded-full text-sm font-medium transition-all">
          <span class="material-symbols-outlined text-[18px]">person_apron</span>
          <span>Profesor</span>
        </div>
      </label>
      <label class="flex-1 cursor-pointer">
        <input v-model="role" class="peer sr-only" name="role" type="radio" value="student" />
        <div :class="role==='student' ? activeClass : inactiveClass" class="flex items-center justify-center gap-2 py-2.5 px-4 rounded-full text-sm font-medium transition-all">
          <span class="material-symbols-outlined text-[18px]">backpack</span>
          <span>Alumno</span>
        </div>
      </label>
    </div>

    <form @submit.prevent="submitForm" class="flex flex-col gap-5">
      <div class="flex flex-col gap-1.5">
        <label class="text-sm font-semibold text-brand-dark ml-1">Correo electrónico</label>
        <div class="relative">
          <input v-model="email" class="w-full h-12 rounded-full border border-gray-200 bg-background-light px-4 pl-11 text-brand-dark placeholder:text-gray-400 focus:border-brand-blue focus:ring-2 focus:ring-brand-blue text-sm transition-colors" placeholder="ejemplo@escuela.edu" type="email"/>
          <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-[20px]">mail</span>
        </div>
      </div>

      <div class="flex flex-col gap-1.5">
        <div class="flex justify-between items-center ml-1">
          <label class="text-sm font-semibold text-brand-dark">Contraseña</label>
          <button type="button" class="text-xs font-medium text-brand-blue hover:underline">¿Olvidaste tu contraseña?</button>
        </div>
        <div class="relative">
          <input v-model="password" class="w-full h-12 rounded-full border border-gray-200 bg-background-light px-4 pl-11 text-brand-dark placeholder:text-gray-400 focus:border-brand-blue focus:ring-2 focus:ring-brand-blue text-sm transition-colors" placeholder="Ingresa tu contraseña" type="password"/>
          <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-[20px]">lock</span>
        </div>
      </div>

      <button class="mt-2 w-full h-12 rounded-full bg-blue-800 hover:bg-blue-800 text-white font-bold text-sm transition-all shadow-lg flex items-center justify-center gap-2" type="submit">
        <span>Iniciar sesión</span>
        <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
      </button>
    </form>

    <!-- Social Login Divider -->
    <div class="relative flex py-2 items-center mt-3">
      <div class="flex-grow border-t border-gray-200"></div>
      <span class="flex-shrink-0 mx-4 text-gray-400 text-xs font-medium uppercase">O continúa con</span>
      <div class="flex-grow border-t border-gray-200"></div>
    </div>

    <!-- Social Buttons -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
      <button type="button" class="w-full flex items-center justify-center gap-2 h-10 rounded-full border border-gray-200 hover:bg-gray-50 transition-colors">
        <img alt="Google Logo" class="w-5 h-5" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAuEN5Cz7AShau6TjI93p4wpvmRyI1YLLxrQFv4Rp_XpZoc5-PyU6YpAKNbwlsKdldfM2tB6Egg-zsPflzz-wn4vNf4EsO0PntYOE2SYEtkdG_pqSG0EFdiQ_Nl356QSKCtOyQjVDDVuhvcal65GuF7rr-y1hzYBzHCcADMTbAO8mD9wJrAhWwXl5RRU5FLMLrkIzwYXaZVWPLhNZYLC0JELFqouNspiSyE6axQpAtweJ5TM3evl2_ZqQ4rzC8xLfSG4CLz84N2Hfo"/>
        <span class="text-xs font-semibold text-gray-600">Google</span>
      </button>
      <button type="button" class="w-full flex items-center justify-center gap-2 h-10 rounded-full border border-gray-200 hover:bg-gray-50 transition-colors">
        <img alt="Microsoft Logo" class="w-5 h-5" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDZchz09_XNMrakJlILAkL6Gbqa3w_YnNwRvIiHgxJfaD9LqXAW6xQ0__FpxzPu5SJ--BVJfr1ebxZvMjwyP29ytva_9EAQKfy-8Owv1TUmTzaMEohEKxgc1uxy73Nm7tgavTy7D8McfUwXuDDOkX654YhGzkzJRJiOHCw4rL_VOCFcvY2lH_x5zxchAXVr2__Q-BgkjvsI9Wa3Ojn4cUBcnRKQB0rUQIrxGrGnyJ04Td3owrHZ2-1IjESyjPTCqImJd-McMlm2CVw"/>
        <span class="text-xs font-semibold text-gray-600">Microsoft</span>
      </button>
    </div>

    <div class="mt-4 text-center text-sm text-gray-500">
      <p>¿No tienes una cuenta? <button class="font-bold text-brand-blue ml-1" @click="$emit('show-signup')">Crear cuenta</button></p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const emits = defineEmits(['show-signup', 'submit'])

const props = defineProps({
  selectedRole: { type: String, default: 'teacher' }
})

const role = ref(props.selectedRole || 'teacher')
watch(() => props.selectedRole, (v) => { role.value = v || 'teacher' })
const email = ref('')
const password = ref('')

const activeClass = 'bg-blue-800 text-white shadow-sm hover:shadow-md hover:scale-105 transition-transform duration-150'
const inactiveClass = 'text-gray-500 hover:bg-blue-800 hover:text-white transition-colors duration-150'

function submitForm() {
  emits('submit', { type: 'login', role: role.value, email: email.value, password: password.value })
}
</script>

<style scoped>
</style>
