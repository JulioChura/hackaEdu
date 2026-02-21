<template>
  <section>
    <div class="bg-white dark:bg-zinc-900 p-4 md:p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800">
      <!-- Header -->
      <h3 class="font-bold mb-4 md:mb-6 flex items-center gap-2 text-sm md:text-base">
        <span class="material-symbols-outlined text-primary text-lg md:text-xl">military_tech</span>
        Latest Achievements
      </h3>

      <!-- Achievements List -->
      <div class="space-y-4 md:space-y-6">
        <div 
          v-for="achievement in latestAchievements" 
          :key="achievement.achievementId"
          class="flex items-center gap-3 md:gap-4"
        >
          <!-- Achievement Icon -->
          <div class="w-10 h-10 md:w-12 md:h-12 rounded-full bg-accent/10 flex items-center justify-center text-accent shrink-0">
            <span class="material-symbols-outlined text-xl md:text-2xl fill-icon">
              {{ achievement.iconName }}
            </span>
          </div>

          <!-- Achievement Info -->
          <div class="flex-1 min-w-0">
            <p class="text-xs md:text-sm font-bold truncate">{{ achievement.title }}</p>
            <p class="text-[10px] md:text-xs text-medium-gray truncate">{{ achievement.description }}</p>
          </div>
        </div>

        <!-- Empty State -->
        <div 
          v-if="latestAchievements.length === 0"
          class="text-center py-8"
        >
          <span class="material-symbols-outlined text-4xl text-gray-300 dark:text-zinc-700 mb-2 block">
            workspace_premium
          </span>
          <p class="text-sm text-medium-gray">No achievements yet</p>
          <p class="text-xs text-medium-gray mt-1">Start learning to earn badges!</p>
        </div>
      </div>

      <!-- Show All Button -->
      <button 
        @click="handleShowAllBadges"
        class="w-full mt-6 py-2.5 border border-primary/20 text-primary text-xs font-bold rounded-lg hover:bg-primary hover:text-white transition-all"
      >
        Show All Badges
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  latestAchievements: {
    type: Array,
    default: () => [
      // Estructura de datos esperada:
      // {
      //   achievementId: 1,
      //   title: 'First Step',
      //   description: 'Completed first lesson',
      //   iconName: 'footprint'
      // }
    ]
  },
  maxDisplayed: {
    type: Number,
    default: 3
  }
});

const emit = defineEmits(['show-all-badges']);

const handleShowAllBadges = () => {
  emit('show-all-badges');
};
</script>
