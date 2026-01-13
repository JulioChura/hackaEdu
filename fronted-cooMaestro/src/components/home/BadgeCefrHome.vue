<template>
  <div class="flex flex-col items-center gap-2 group cursor-pointer">
    <div 
      :class="[
        'w-12 h-12 sm:w-14 sm:h-14 rounded-xl bg-white border flex items-center justify-center shadow-sm transition-all duration-300',
        isActive 
          ? 'border-primary shadow-md' 
          : 'border-slate-200 group-hover:bg-primary group-hover:border-primary'
      ]"
    >
      <!-- Ping indicator para nivel activo -->
      <span v-if="isActive" class="absolute -top-2 -right-2 flex h-3 w-3 sm:h-4 sm:w-4">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 sm:h-4 sm:w-4 bg-primary"></span>
      </span>
      
      <span 
        :class="[
          'text-base sm:text-lg font-bold transition-colors',
          isActive 
            ? 'text-charcoal' 
            : 'text-slate-400 group-hover:text-charcoal'
        ]"
      >
        {{ level }}
      </span>
    </div>
    
    <span 
      :class="[
        'text-xs font-medium transition-colors',
        isActive 
          ? 'text-primary font-bold' 
          : 'text-slate-400 group-hover:text-primary'
      ]"
    >
      {{ label }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  level: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  isActive: {
    type: Boolean,
    default: false,
  },
})
</script>
