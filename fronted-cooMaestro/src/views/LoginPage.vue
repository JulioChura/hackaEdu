<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const showPassword = ref(false)

const handleLogin = async (e) => {
  e.preventDefault()
  errorMessage.value = ''
  loading.value = true

  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })
    
    // Redirigir al dashboard después del login exitoso
    router.push({ name: 'Dashboard' })
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Invalid email or password'
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="min-h-screen bg-background-light text-slate-900 relative overflow-x-hidden font-sans">
    <!-- Floating badges / blobs -->
    <div class="fixed inset-0 pointer-events-none z-0">
      <span class="cefr-badge absolute w-12 h-12 bg-emerald-100 text-emerald-600 top-[15%] left-[5%] rotate-[-15deg]">A1</span>
      <span class="cefr-badge absolute w-14 h-14 bg-blue-100 text-blue-600 top-[60%] left-[8%] rotate-[10deg]">B2</span>
      <span class="cefr-badge absolute w-12 h-12 bg-amber-100 text-amber-600 top-[40%] right-[35%] rotate-[-5deg]">B1</span>
      <span class="cefr-badge absolute w-16 h-16 bg-purple-100 text-purple-600 bottom-[15%] right-[5%] rotate-[12deg]">C2</span>
      <div class="absolute top-1/4 left-1/3 w-64 h-64 bg-primary/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-80 sm:w-96 h-80 sm:h-96 bg-indigo-500/5 rounded-full blur-3xl"></div>
    </div>

    <div class="flex min-h-screen relative z-10">
      <!-- Left visual panel -->
      <section class="hidden lg:flex lg:w-1/2 bg-primary text-white items-center justify-center p-10 xl:p-12 relative overflow-hidden">
        <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 32px 32px;"></div>
        <div class="relative z-10 max-w-lg text-center space-y-6">
          <div class="relative inline-block mb-10">
            <img
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuC2uGxFSy9PoqIgKLmzGC9bv3z-eGm4Z9aufBjcj7r8k0aW5f5oXsNhhNn74s3MnSBL_I_Iju_IEpciaHPGBfcxpWoaKMueE0yGqjMEz2ueIQGhRx4rqHzIZNMuq7Q2_YGil_kxYOyoqv32Nr7zH7JjiqUx6BHFJJzQ4jjnEOnmUTkJwiI3orkU1P9KjrxyUVNR3vWA6RJ7Wca7Cd6qitCJ5MUl8PYT4c8FpdIIApxkfONlUqrXVlx6FJhxicEd8Q6DMBUH4ZxlOilz"
              alt="Student reading"
              class="rounded-3xl shadow-2xl border-4 border-white/10 aspect-[4/3] object-cover"
              loading="lazy"
            />
            <div class="absolute -bottom-6 -right-6 bg-white/95 text-slate-900 p-4 rounded-xl shadow-xl border border-slate-100 flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center">
                <span class="material-symbols-outlined text-emerald-600">auto_stories</span>
              </div>
              <div class="text-left leading-tight">
                <p class="text-xs font-bold text-slate-400 uppercase">Progress</p>
                <p class="text-sm font-bold text-slate-800">85% Mastery reached</p>
              </div>
            </div>
          </div>

          <h2 class="text-3xl xl:text-4xl font-extrabold tracking-tight">Master English through Reading</h2>
          <p class="text-indigo-100 text-lg leading-relaxed">
            Access curated content tailored to your CEFR level. Track your progress and expand your vocabulary with HackaEdu's interactive library.
          </p>
        </div>

        <RouterLink to="/" class="absolute top-8 left-8 flex items-center gap-2 text-white/90 hover:text-white font-medium transition-colors group">
          <span class="material-symbols-outlined text-xl transition-transform group-hover:-translate-x-1">arrow_back</span>
          Back to Home
        </RouterLink>
      </section>

      <!-- Right form panel -->
      <section class="w-full lg:w-1/2 flex flex-col items-center justify-center p-6 sm:p-10 lg:p-12 xl:p-16 bg-background-light">
        <RouterLink to="/" class="lg:hidden absolute top-6 left-6 flex items-center gap-2 text-slate-500 hover:text-primary font-medium transition-colors">
          <span class="material-symbols-outlined text-xl">arrow_back</span>
          Home
        </RouterLink>

        <main class="w-full max-w-[460px] bg-white backdrop-blur-sm rounded-2xl shadow-xl border border-slate-100 overflow-hidden">
          <div class="pt-10 pb-6 px-8 sm:px-10 flex flex-col items-center text-center">
            <div class="mb-6 text-primary">
              <div class="w-14 h-14">
                <svg class="w-full h-full" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M36.7273 44C33.9891 44 31.6043 39.8386 30.3636 33.69C29.123 39.8386 26.7382 44 24 44C21.2618 44 18.877 39.8386 17.6364 33.69C16.3957 39.8386 14.0109 44 11.2727 44C7.25611 44 4 35.0457 4 24C4 12.9543 7.25611 4 11.2727 4C14.0109 4 16.3957 8.16144 17.6364 14.31C18.877 8.16144 21.2618 4 24 4C26.7382 4 29.123 8.16144 30.3636 14.31C31.6043 8.16144 33.9891 4 36.7273 4C40.7439 4 44 12.9543 44 24C44 35.0457 40.7439 44 36.7273 44Z" fill="currentColor" />
                </svg>
              </div>
            </div>
            <h1 class="text-2xl font-bold text-slate-900 mb-2 tracking-tight">Welcome back to HackaEdu</h1>
            <p class="text-sm text-slate-500">Your journey to fluency continues here.</p>
          </div>

          <div class="px-8 sm:px-10 pb-10">
            <!-- Error Message -->
            <div v-if="errorMessage" class="mb-5 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-600 font-medium">{{ errorMessage }}</p>
            </div>

            <form class="space-y-5" @submit="handleLogin">
              <div class="space-y-1.5">
                <label for="email" class="text-sm font-semibold text-slate-700">Email Address</label>
                <div class="relative group">
                  <input
                    id="email"
                    v-model="email"
                    type="email"
                    placeholder="name@example.com"
                    required
                    class="w-full h-12 px-4 rounded-xl border border-slate-200 bg-white text-slate-900 text-base focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all placeholder:text-slate-400"
                  />
                  <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors text-xl">
                    mail
                  </span>
                </div>
              </div>

              <div class="space-y-1.5">
                <label for="password" class="text-sm font-semibold text-slate-700">Password</label>
                <div class="relative group">
                  <input
                    id="password"
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="••••••••"
                    required
                    class="w-full h-12 px-4 rounded-xl border border-slate-200 bg-white text-slate-900 text-base focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all placeholder:text-slate-400"
                  />
                  <button
                    type="button"
                    @click="togglePasswordVisibility"
                    class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors text-xl hover:text-slate-600 cursor-pointer"
                  >
                    {{ showPassword ? 'visibility_off' : 'lock' }}
                  </button>
                </div>
              </div>

              <div class="flex items-center justify-between mt-1">
                <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
                  <input v-model="rememberMe" type="checkbox" class="h-4 w-4 text-primary focus:ring-primary border-slate-300 rounded cursor-pointer transition-colors" />
                  Remember me
                </label>
                <RouterLink to="/forgot-password" class="text-sm font-semibold text-primary hover:text-primary/80 transition-colors">Forgot password?</RouterLink>
              </div>

              <button 
                type="submit" 
                :disabled="loading"
                class="w-full h-12 bg-primary hover:bg-primary-dark disabled:bg-slate-300 text-white font-bold rounded-xl shadow-lg shadow-primary/25 hover:shadow-primary/40 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
              >
                <span v-if="loading" class="material-symbols-outlined animate-spin">progress_activity</span>
                <span>{{ loading ? 'Signing In...' : 'Sign In' }}</span>
              </button>

              <div class="relative flex items-center py-2">
                <div class="flex-grow border-t border-slate-100"></div>
                <span class="flex-shrink-0 mx-4 text-xs font-bold text-slate-400 uppercase tracking-widest">or</span>
                <div class="flex-grow border-t border-slate-100"></div>
              </div>

              <button type="button" class="w-full h-12 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-bold rounded-xl transition-all flex items-center justify-center gap-3">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                </svg>
                Continue with Google
              </button>
            </form>

            <div class="mt-8 text-center pt-6 border-t border-slate-100">
              <p class="text-sm text-slate-500">
                Don't have an account?
                <RouterLink to="/register" class="font-bold text-primary hover:underline ml-1">Create free account</RouterLink>
              </p>
            </div>
          </div>
        </main>

        <footer class="mt-8 flex flex-wrap gap-4 sm:gap-6 text-sm text-slate-400 font-medium justify-center">
          <a href="#" class="hover:text-primary transition-colors">Terms of Service</a>
          <a href="#" class="hover:text-primary transition-colors">Privacy Policy</a>
          <a href="#" class="hover:text-primary transition-colors">Contact Support</a>
        </footer>
      </section>
    </div>
  </div>
</template>

<style scoped>
.cefr-badge {
  @apply flex items-center justify-center rounded-full font-bold text-xs shadow-lg backdrop-blur-md border border-white/60 select-none;
}
</style>
