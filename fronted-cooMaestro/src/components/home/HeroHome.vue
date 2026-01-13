<template>
  <section class="relative min-h-screen sm:min-h-[90vh] flex items-center justify-center py-16 sm:py-20 overflow-hidden">
    <!-- Background Decoration -->
    <div class="hidden lg:block absolute top-0 right-0 w-1/2 h-full bg-slate-50 -z-10 skew-x-12 origin-top transform translate-x-1/4"></div>
    <div class="absolute bottom-0 left-10 sm:left-20 w-48 h-48 sm:w-64 sm:h-64 bg-primary/5 rounded-full blur-3xl -z-10"></div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-10 sm:gap-16 items-center w-full">
      <!-- Text Content -->
      <div class="md:col-span-1 lg:col-span-5 flex flex-col gap-6 sm:gap-8">
        <BadgeHome />
        
        <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight sm:leading-[0.95] tracking-tight text-charcoal">
          Master Reading <br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-500">Comprehension</span> <br/>
          with AI.
        </h1>
        
        <p class="text-base sm:text-lg md:text-xl text-slate-text leading-relaxed max-w-lg">
          Personalized reading passages tailored strictly to your CEFR level. From A1 beginners to C2 mastery, visualize your growth with real-time analytics.
        </p>
        
        <!-- Buttons -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 mt-2">
          <button class="bg-primary hover:bg-primary-dark transition-all text-white font-bold text-sm sm:text-base px-6 sm:px-8 py-3 sm:py-4 rounded-lg shadow-lg hover:shadow-xl hover:-translate-y-1 flex items-center justify-center gap-2 group">
            Start Learning
            <span class="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
          </button>
          <button class="bg-white border-2 border-slate-200 hover:border-primary text-slate-700 hover:text-primary transition-all font-bold text-sm sm:text-base px-6 sm:px-8 py-3 sm:py-4 rounded-lg flex items-center justify-center gap-2">
            For Educators
          </button>
        </div>
        
        <AvatarsHome />
      </div>
      
      <!-- Visual Mockup -->
      <div class="md:col-span-1 lg:col-span-7 relative">
        <div class="absolute -top-10 -right-10 w-32 h-32 sm:w-40 sm:h-40 bg-primary/20 rounded-full blur-2xl"></div>
        <MockupHome />
      </div>
    </div>
  </section>
</template>

<script setup>
import BadgeHome from './BadgeHome.vue'
import AvatarsHome from './AvatarsHome.vue'
import MockupHome from './MockupHome.vue'
</script>
