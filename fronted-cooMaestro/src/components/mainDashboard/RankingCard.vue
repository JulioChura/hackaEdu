<template>
  <section>
    <div class="bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800 overflow-hidden">
      <!-- Header with User Rank -->
      <div class="p-4 md:p-6 border-b border-gray-100 dark:border-zinc-800">
        <h3 class="font-bold mb-3 md:mb-4 flex items-center gap-2 text-sm md:text-base">
          <span class="material-symbols-outlined text-primary text-lg md:text-xl">emoji_events</span>
          Global Ranking
        </h3>
        
        <div class="bg-primary rounded-xl p-3 md:p-4 text-white flex items-center justify-between">
          <div>
            <p class="text-[9px] md:text-[10px] font-bold uppercase opacity-80">Your Rank</p>
            <p class="text-xl md:text-2xl font-bold">#{{ userRank }}</p>
          </div>
          <div class="text-right">
            <p class="text-[9px] md:text-[10px] font-bold uppercase opacity-80">Top</p>
            <p class="text-base md:text-lg font-bold">{{ userTopPercentage }}%</p>
          </div>
        </div>
      </div>

      <!-- Top 3 Leaderboard -->
      <div class="p-4 space-y-4">
        <div 
          v-for="(player, index) in topPlayers" 
          :key="player.userId"
          class="flex items-center gap-3"
        >
          <!-- Rank Number -->
          <span 
            class="text-sm font-bold w-4"
            :class="{
              'text-accent': index === 0,
              'text-gray-400': index === 1,
              'text-orange-400': index === 2
            }"
          >
            {{ index + 1 }}
          </span>

          <!-- User Avatar -->
          <div 
            class="w-8 h-8 rounded-full bg-cover bg-center"
            :style="{ backgroundImage: `url(${player.avatarUrl})` }"
            :alt="`${player.userName} avatar`"
          >
            <div 
              v-if="!player.avatarUrl" 
              class="w-full h-full bg-gray-300 dark:bg-zinc-700 rounded-full flex items-center justify-center"
            >
              <span class="material-symbols-outlined text-xs text-white">person</span>
            </div>
          </div>

          <!-- User Name -->
          <span class="text-sm font-medium flex-1 truncate">
            {{ player.userName }}
          </span>

          <!-- Points -->
          <span class="text-xs font-bold text-medium-gray">
            {{ formatPoints(player.points) }} pts
          </span>
        </div>
      </div>

      <!-- View Full Leaderboard Button -->
      <button 
        @click="handleViewFullLeaderboard"
        class="w-full py-3 text-xs font-bold text-primary bg-primary/5 hover:bg-primary/10 transition-colors"
      >
        View Full Leaderboard
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  userRank: {
    type: Number,
    default: 0
  },
  userTopPercentage: {
    type: Number,
    default: 0
  },
  topPlayers: {
    type: Array,
    default: () => [
      // Estructura de datos esperada:
      // {
      //   userId: 1,
      //   userName: 'Player Name',
      //   avatarUrl: 'https://...',
      //   points: 2450
      // }
    ]
  }
});

const emit = defineEmits(['view-full-leaderboard']);

const formatPoints = (points) => {
  return new Intl.NumberFormat('en-US').format(points);
};

const handleViewFullLeaderboard = () => {
  emit('view-full-leaderboard');
};
</script>
