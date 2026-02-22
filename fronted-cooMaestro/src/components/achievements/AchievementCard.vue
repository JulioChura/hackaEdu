<script setup>
const props = defineProps({
  achievement: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <!-- Unlocked Achievement -->
  <div 
    v-if="achievement.unlocked"
    class="group relative bg-white dark:bg-white/5 rounded-2xl border border-gray-100 dark:border-white/10 p-4 sm:p-5 shadow-sm hover:shadow-xl transition-all"
  >
    <div class="unlocked-gradient w-full aspect-square rounded-xl mb-3 sm:mb-4 flex items-center justify-center relative overflow-hidden">
      <div class="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.8),transparent)]"></div>
      <span class="text-5xl sm:text-6xl group-hover:scale-110 transition-transform">{{ achievement.emoji }}</span>
      <div class="absolute top-2 sm:top-3 right-2 sm:right-3 bg-white/20 backdrop-blur-md px-2 py-1 rounded text-[9px] sm:text-[10px] font-bold text-white tracking-wider">
        UNLOCKED
      </div>
    </div>
    <h3 class="text-base sm:text-lg font-extrabold mb-1">{{ achievement.title }}</h3>
    <p class="text-[10px] sm:text-xs text-primary font-bold mb-2 sm:mb-3 uppercase tracking-tighter">
      {{ achievement.achievedDate }}
    </p>
    <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
      {{ achievement.description }}
    </p>
  </div>

  <!-- Locked Achievement -->
  <div 
    v-else
    class="relative bg-white dark:bg-white/5 rounded-2xl border border-dashed border-gray-200 dark:border-white/10 p-4 sm:p-5 transition-all group"
  >
    <div class="bg-gray-300 dark:bg-white/10 w-full aspect-square rounded-xl mb-3 sm:mb-4 flex items-center justify-center relative overflow-hidden">
      <span class="text-5xl sm:text-6xl opacity-30 grayscale">{{ achievement.emoji }}</span>
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="material-symbols-outlined text-white text-2xl sm:text-3xl drop-shadow-md">lock</span>
        <span class="text-white text-[9px] sm:text-[10px] font-bold mt-1 uppercase tracking-widest drop-shadow-md">
          LOCKED
        </span>
      </div>
    </div>
    <h3 class="text-base sm:text-lg font-extrabold mb-1">{{ achievement.title }}</h3>
    <p class="text-[10px] sm:text-xs text-gray-400 font-bold mb-2 sm:mb-3 uppercase tracking-tighter">
      {{ achievement.progress }}
    </p>
    <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
      {{ achievement.description }}
    </p>
  </div>
</template>

<style scoped>
.unlocked-gradient {
  background: linear-gradient(135deg, #3022c3 0%, #B33DF2 100%);
}
</style>
