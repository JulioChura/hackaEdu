<template>
  <div class="group p-6 sm:p-8 rounded-2xl bg-white border border-slate-100 shadow-md hover:shadow-xl transition-all duration-300 relative overflow-hidden">
    <!-- Top border on hover -->
    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
    
    <!-- Icon -->
    <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-xl bg-cyan-50 text-primary flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform duration-300">
      <span class="material-symbols-outlined text-3xl sm:text-4xl">{{ icon }}</span>
    </div>
    
    <!-- Title -->
    <h3 class="text-lg sm:text-xl font-bold text-charcoal mb-2 sm:mb-3">{{ title }}</h3>
    
    <!-- Description -->
    <p class="text-slate-text text-sm sm:text-base leading-relaxed">
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
})
</script>
