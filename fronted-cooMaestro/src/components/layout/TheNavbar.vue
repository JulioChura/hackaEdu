<template>
  <nav class="fixed top-0 left-0 right-0 z-50 border-b border-gray-100 bg-white/90 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex flex-wrap justify-between items-center h-16 sm:h-20">
        <!-- Logo -->
        <a href="#" class="flex items-center gap-2 sm:gap-3">
          <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-primary flex items-center justify-center text-white">
            <span class="material-symbols-outlined text-base sm:text-lg font-bold">school</span>
          </div>
          <h1 class="text-lg sm:text-xl font-bold tracking-tight text-charcoal">HackaEdu</h1>
        </a>

        <!-- Actions + Hamburger -->
        <div class="flex items-center gap-3 sm:gap-4 lg:order-2">
          <a href="#login" class="hidden sm:block text-sm font-bold text-charcoal hover:text-primary transition-colors">
            Log In
          </a>
          <button class="bg-primary hover:bg-primary-dark transition-colors text-white font-bold text-xs sm:text-sm px-4 sm:px-5 py-2 sm:py-2.5 rounded-lg shadow-sm">
            Start Learning
          </button>
          
          <!-- Hamburger Button -->
          <button 
            @click="isMenuOpen = !isMenuOpen"
            type="button" 
            class="inline-flex items-center p-2 ml-1 text-sm text-slate-text rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
            aria-controls="mobile-menu"
            :aria-expanded="isMenuOpen"
          >
            <span class="sr-only">Open main menu</span>
            <!-- Hamburger Icon -->
            <svg v-show="!isMenuOpen" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
            </svg>
            <!-- Close Icon -->
            <svg v-show="isMenuOpen" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <!-- Navigation Links -->
        <div 
          :class="[
            'w-full lg:flex lg:w-auto lg:order-1 lg:bg-transparent',
            isMenuOpen ? 'block' : 'hidden'
          ]"
          id="mobile-menu"
          class="absolute left-0 right-0 top-full bg-white border-b border-gray-100 shadow-md lg:relative lg:top-auto lg:shadow-none lg:border-0"
        >
          <ul class="flex flex-col py-4 px-4 font-medium lg:flex-row lg:space-x-8 lg:py-0 lg:px-0 lg:items-center">
            <li>
              <a 
                href="#features" 
                class="block py-2.5 px-4 text-slate-text hover:bg-primary hover:text-white lg:hover:bg-transparent lg:hover:text-primary lg:p-0 transition-all rounded-lg lg:rounded-none"
              >
                Features
              </a>
            </li>
            <li>
              <a 
                href="#pricing" 
                class="block py-2.5 px-4 text-slate-text hover:bg-primary hover:text-white lg:hover:bg-transparent lg:hover:text-primary lg:p-0 transition-all rounded-lg lg:rounded-none"
              >
                Pricing
              </a>
            </li>
            <li>
              <a 
                href="#about" 
                class="block py-2.5 px-4 text-slate-text hover:bg-primary hover:text-white lg:hover:bg-transparent lg:hover:text-primary lg:p-0 transition-all rounded-lg lg:rounded-none"
              >
                About
              </a>
            </li>
            <!-- Log In mobile only -->
            <li class="sm:hidden border-t border-gray-100 mt-2 pt-2">
              <a 
                href="#login" 
                class="block py-2.5 px-4 text-charcoal font-bold hover:bg-primary hover:text-white transition-all rounded-lg"
              >
                Log In
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)
</script>
