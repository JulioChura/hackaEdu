<template>
  <div class="min-h-screen flex flex-col bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 overflow-x-hidden">
    <!-- Floating badges and background effects -->
    <div class="fixed inset-0 z-0 pointer-events-none overflow-hidden">
      <div class="absolute top-[10%] left-[5%] px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-primary font-bold rounded-full floating-badge rotate-[-12deg] opacity-40">A2 - Elementary</div>
      <div class="absolute top-[40%] left-[25%] px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 font-bold rounded-full floating-badge rotate-[15deg] opacity-30">B2 - Upper Intermediate</div>
      <div class="absolute bottom-[15%] left-[8%] px-4 py-2 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 font-bold rounded-full floating-badge rotate-[-8deg] opacity-50">C1 - Advanced</div>
      <div class="absolute top-[-10%] right-[-10%] w-96 h-96 bg-primary/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-[-10%] right-[30%] w-80 h-80 bg-secondary/10 rounded-full blur-3xl"></div>
    </div>
    <main class="flex-grow flex items-stretch min-h-screen relative z-10">
      <!-- Left panel for large screens -->
      <div class="hidden lg:flex lg:w-1/2 relative bg-primary items-center justify-center p-12 overflow-hidden">
        <div class="absolute inset-0 opacity-10 pointer-events-none">
          <svg height="100%" width="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern height="40" id="grid" patternUnits="userSpaceOnUse" width="40">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="1" />
              </pattern>
            </defs>
            <rect fill="url(#grid)" height="100%" width="100%" />
          </svg>
        </div>
        <div class="relative z-10 text-white max-w-lg text-center">
          <div class="mb-10 inline-flex items-center justify-center p-4 bg-white/20 backdrop-blur-md rounded-2xl">
            <span class="material-symbols-outlined text-[64px] text-white">auto_stories</span>
          </div>
          <h2 class="text-4xl font-extrabold mb-6 leading-tight">Master the Language with HackaEdu</h2>
          <p class="text-xl text-white/80 mb-12">Unlock achievements, track your CEFR progression, and access thousands of curated reading materials tailored for your level.</p>
          <div class="relative mx-auto w-full aspect-video bg-white/10 rounded-2xl border border-white/20 p-8 flex items-center justify-center shadow-2xl">
            <div class="relative flex flex-col items-center">
              <div class="w-32 h-32 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce shadow-lg">
                <span class="material-symbols-outlined text-white text-[64px]">trophy</span>
              </div>
              <div class="mt-6 space-y-3">
                <div class="h-2 w-48 bg-white/30 rounded-full overflow-hidden">
                  <div class="h-full bg-white w-3/4"></div>
                </div>
                <p class="font-bold text-lg">Level Up: B2 Reached!</p>
              </div>
            </div>
          </div>
        </div>
        <a href="#" class="absolute top-8 left-8 flex items-center gap-2 text-white/90 hover:text-white font-medium transition-colors group">
          <span class="material-symbols-outlined text-xl transition-transform group-hover:-translate-x-1">arrow_back</span>
          Back to Home
        </a>
      </div>
      <!-- Registration form -->
      <div class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 lg:p-20 bg-background-light dark:bg-background-dark">
        <div class="w-full max-w-[520px]">
          <div class="mb-8 lg:hidden flex justify-center">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-3xl">school</span>
              <span class="text-2xl font-bold tracking-tight text-primary">HackaEdu</span>
            </div>
          </div>
          <div class="mb-10">
            <h1 class="text-3xl font-bold text-slate-900 mb-3">Crear cuenta</h1>
            <p class="text-slate-500 dark:text-slate-400">Únete a la comunidad y comienza tu viaje de lectura hoy.</p>
          </div>
          <form class="space-y-5" @submit.prevent="handleRegister">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-800" for="firstName">Nombre</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 material-symbols-outlined text-xl">person</span>
                  <input v-model="form.firstName" class="w-full h-12 pl-12 pr-4 rounded-xl border-slate-200 bg-white text-slate-900 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition duration-200 ease-in-out focus:shadow-lg" id="firstName" placeholder="Alex" type="text" required />
                </div>
              </div>
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-800" for="lastName">Apellido</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 material-symbols-outlined text-xl">person</span>
                  <input v-model="form.lastName" class="w-full h-12 pl-12 pr-4 rounded-xl border-slate-200 bg-white text-slate-900 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition duration-200 ease-in-out focus:shadow-lg" id="lastName" placeholder="Smith" type="text" required />
                </div>
              </div>
            </div>
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-800" for="email">Correo electrónico</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 material-symbols-outlined text-xl">mail</span>
                <input v-model="form.email" class="w-full h-12 pl-12 pr-4 rounded-xl border-slate-200 bg-white text-slate-900 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition duration-200 ease-in-out focus:shadow-lg" id="email" placeholder="alex.smith@university.edu" type="email" required />
              </div>
            </div>
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-800" for="password">Contraseña</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 material-symbols-outlined text-xl">lock</span>
                <input v-model="form.password" class="w-full h-12 pl-12 pr-12 rounded-xl border-slate-200 bg-white text-slate-900 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition duration-200 ease-in-out focus:shadow-lg" id="password" placeholder="••••••••" type="password" required />
                <button class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-primary transition-colors" type="button" @click="togglePassword">
                  <span class="material-symbols-outlined text-xl">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
                </button>
              </div>
            </div>
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-800" for="confirmPassword">Confirmar contraseña</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 material-symbols-outlined text-xl">lock_reset</span>
                <input v-model="form.confirmPassword" class="w-full h-12 pl-12 pr-4 rounded-xl border-slate-200 bg-white text-slate-900 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition duration-200 ease-in-out focus:shadow-lg" id="confirmPassword" placeholder="••••••••" type="password" required />
              </div>
            </div>
            <!-- Preferencias de categorías -->
            <div class="space-y-3 pt-2">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-xl">bookmark</span>
                <label class="text-sm font-semibold text-gray-800">
                  ¿Qué temas te interesan? 
                  <span class="text-slate-500 font-normal text-xs">(opcional, puedes seleccionar varios)</span>
                </label>
              </div>
              <div v-if="loadingCategories" class="text-center py-4">
                <svg class="animate-spin h-6 w-6 mx-auto text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                </svg>
              </div>
              <div v-else-if="categoriesError" class="text-center py-4 text-red-500 text-sm">
                {{ categoriesError }}
              </div>
              <div v-else-if="categories.length > 0" class="flex flex-wrap gap-2">
                <button
                  v-for="category in categories"
                  :key="category?.codigo || Math.random()"
                  type="button"
                  @click="category?.codigo && toggleCategory(category.codigo)"
                  :class="[
                    'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border-2',
                    category?.codigo && selectedCategories.includes(category.codigo)
                      ? 'bg-primary text-white border-primary shadow-md shadow-primary/25 scale-105'
                      : 'bg-white text-slate-700 border-slate-200 hover:border-primary hover:text-primary hover:shadow-sm'
                  ]"
                >
                  {{ category?.nombre || 'Categoría sin nombre' }}
                </button>
              </div>
              <div v-else class="text-center py-4 text-slate-500 text-sm">
                No hay categorías disponibles en este momento
              </div>
            </div>
            <div class="flex items-start gap-3 py-2">
              <input v-model="form.terms" class="mt-1 h-5 w-5 rounded border-slate-300 text-primary focus:ring-primary dark:border-slate-600 dark:bg-slate-800 cursor-pointer" id="terms" type="checkbox" required />
              <label class="text-sm text-gray-800 dark:text-slate-400 leading-relaxed cursor-pointer" for="terms">
                Acepto los <a class="text-primary font-semibold hover:underline" href="#">Términos y Condiciones</a> y reconozco la <a class="text-primary font-semibold hover:underline" href="#">Política de Privacidad</a>.
              </label>
            </div>
            <button :disabled="loading" class="w-full h-14 bg-primary hover:bg-primary/90 text-white font-bold rounded-xl shadow-lg shadow-primary/25 transition-all active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed transition duration-200 ease-in-out" type="submit">
              <span v-if="!loading">Crear cuenta</span>
              <span v-else class="flex items-center gap-2"><svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>Registrando...</span>
              <span class="material-symbols-outlined text-xl">person_add</span>
            </button>
            <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
            <p v-if="success" class="text-green-600 text-sm mt-2">¡Registro exitoso! Ahora puedes iniciar sesión.</p>
          </form>
          <div class="mt-8 pt-8 border-t border-slate-200 dark:border-slate-800 text-center">
            <p class="text-slate-600 dark:text-slate-400">
              ¿Ya tienes una cuenta?
              <router-link class="text-primary font-bold hover:underline ml-1" to="/login">Inicia sesión aquí</router-link>
            </p>
          </div>
        </div>
      </div>
    </main>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/auth.service'
import { categoriesService } from '../services/categories.service'

const router = useRouter()
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: false
})
const loading = ref(false)
const error = ref('')
const success = ref(false)
const showPassword = ref(false)

// Categorías
const categories = ref([])
const selectedCategories = ref([])
const loadingCategories = ref(false)
const categoriesError = ref('')

// Cargar categorías al montar el componente
onMounted(async () => {
  loadingCategories.value = true
  categoriesError.value = ''
  try {
    const response = await categoriesService.getAll()
    console.log('Categories response:', response)
    // DRF ViewSets retornan datos paginados: {count, results, next, previous}
    const data = response.data.results || response.data
    if (data && Array.isArray(data)) {
      categories.value = data.filter(cat => cat !== null && cat !== undefined)
      console.log('Loaded categories:', categories.value)
    } else {
      categoriesError.value = 'Error: formato de respuesta inválido'
      console.error('Invalid response format:', response)
    }
  } catch (e) {
    console.error('Error loading categories:', e)
    categoriesError.value = 'No se pudieron cargar las categorías. Por favor, intenta más tarde.'
  } finally {
    loadingCategories.value = false
  }
})

const toggleCategory = (codigo) => {
  const index = selectedCategories.value.indexOf(codigo)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(codigo)
  }
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
  const pwd = document.getElementById('password')
  if (pwd) pwd.type = showPassword.value ? 'text' : 'password'
}

const handleRegister = async () => {
  error.value = ''
  success.value = false
  
  // Validación de contraseña mínimo 8 caracteres
  if (form.value.password.length < 8) {
    error.value = 'La contraseña debe tener mínimo 8 caracteres.'
    return
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Las contraseñas no coinciden.'
    return
  }
  
  loading.value = true
  try {
    console.log('Registering user with data:', form.value)
    await authService.register({
      nombre: form.value.firstName,
      apellido: form.value.lastName,
      email: form.value.email,
      password: form.value.password,
      password_confirm: form.value.confirmPassword,
      telefono: '',
      categorias_preferidas: selectedCategories.value
    })
    
    success.value = true
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    console.error('Registration error:', e)
    error.value = e.response?.data?.detail || e.response?.data?.email?.[0] || e.message || 'Error al registrar. Intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
.glass-effect {
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(255,255,255,0.2);
}
.floating-badge {
  box-shadow: 0 10px 20px -5px rgba(29, 124, 165, 0.2);
}
</style>
