<template>
  <div class="font-display bg-background-light text-brand-dark overflow-hidden h-screen flex flex-col md:flex-row">
    <!-- Left Side: Hero / Brand Showcase (60%) -->
    <div class="relative hidden md:flex md:w-[60%] flex-col justify-end p-12 lg:p-20 overflow-hidden bg-brand-blue">
      <div class="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-30" data-alt="Students collaborating" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuAY8gr4mJBl74H1K8HPe30uCOBF_SCi-fR9qFvPkKQ6Q_WW946cGuabhNqRv_Hyqi422lrAvzdt4TVnGrUlHfKlvsMhWodZXD2SO8phorbIpMIORCOlBbuF3ZFNhph-_YUzdNwcRVJszHybAsztbi5Okp0haOlZFHASsHVveTUzAxUAi1osktW5CEpzySgMn9CUp1olc4WuXu3czyIRlM5o5pSrDCPvI75bVMozFD1uXv5u4U_Cw75mHpTmw3JwC41LRRudCZ9dHP8')"></div>
      <div class="absolute inset-0 z-10 bg-gradient-to-t from-[#001B34]/95 via-[#063a6b]/85 to-transparent backdrop-blur-sm"></div>
      <div class="relative z-20 max-w-2xl text-white">
        <div class="mb-6 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 backdrop-blur-md border border-white/20">
          <span class="material-symbols-outlined text-primary text-[20px]">smart_toy</span>
          <span class="text-sm font-semibold tracking-wide">ReConéctate IA</span>
        </div>
        <h1 class="text-4xl lg:text-5xl font-bold leading-tight tracking-tight mb-6">
          Evalúa, comprende y acompaña el aprendizaje en <span class="text-primary">tiempo real</span>
        </h1>
        <p class="text-lg text-white/80 max-w-lg leading-relaxed">
          Potencia tu aula con herramientas inteligentes diseñadas para transformar datos en experiencias educativas personalizadas.
        </p>
        <div class="mt-12 flex gap-4 opacity-70">
          <div class="h-2 w-12 rounded-full bg-primary"></div>
          <div class="h-2 w-2 rounded-full bg-white/30"></div>
          <div class="h-2 w-2 rounded-full bg-white/30"></div>
        </div>
      </div>
    </div>
    <!-- Right Side: Login Form (40%) -->
    <div class="w-full md:w-[40%] flex flex-col justify-center items-center bg-white p-4 sm:p-6 md:p-12 lg:p-20 overflow-y-auto">
      <div class="w-full max-w-md sm:max-w-lg flex flex-col gap-8">
        <!-- Heading Section -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-blue to-brand-teal flex items-center justify-center text-white">
              <span class="material-symbols-outlined icon-bold text-black">school</span>
            </div>
            <span class="text-2xl font-bold tracking-tight text-brand-dark">CooMaestro</span>
          </div>
          <h2 class="text-3xl font-bold text-brand-dark">Bienvenido de nuevo</h2>
          <p class="text-gray-500 text-sm">Ingresa tus credenciales para acceder a tu panel.</p>
        </div>



        <component :is="showSignup ? SignupForm : LoginForm"
             :selected-role="selectedRole"
             @show-signup="showSignup = true"
             @show-login="showSignup = false"
             @submit="onSubmit"
             />        

        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from '../shared/components/LoginForm.vue'
import SignupForm from '../shared/components/SignupForm.vue'

const showSignup = ref(false)
const selectedRole = ref('Profesor')

function onSubmit(payload) {
  console.log('Auth submit', payload)
}

function socialLogin(provider) {
  console.log('Social login with', provider)
  // Implement social login logic here
}
</script>

<style scoped>
/* Add smooth transitions */
* {
  transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

/* Improve focus styles */
:focus-visible {
  outline: 2px solid #0f4c81;
  outline-offset: 2px;
}

/* Make Material Symbols icons appear bolder using variable font axis */
.icon-bold {
  font-variation-settings: 'FILL' 0, 'wght' 700, 'GRAD' 0, 'opsz' 24;
}
</style>