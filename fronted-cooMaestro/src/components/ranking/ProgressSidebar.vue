<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  totalPoints: {
    type: Number,
    default: 0
  },
  pointsGrowth: {
    type: Number,
    default: 0
  },
  weeklyRank: {
    type: Number,
    default: 0
  },
  dayStreak: {
    type: Number,
    default: 0
  },
  nextBadge: {
    type: String,
    default: 'Scholar III'
  },
  badgeProgress: {
    type: Number,
    default: 0
  },
  achievements: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['practice-click'])

const handlePracticeClick = () => {
  router.push({ name: 'AllLectures' })
}
</script>

<template>
  <aside class="w-full lg:w-80 flex flex-col gap-4 sm:gap-6">
    <!-- Your Progress Card -->
    <div class="bg-white dark:bg-white/5 rounded-2xl p-4 sm:p-6 border border-slate-200 dark:border-white/10 podium-shadow">
      <div class="flex items-center justify-between mb-4 sm:mb-6">
        <h3 class="text-base sm:text-lg font-black tracking-tight">Your Progress</h3>
        <span class="material-symbols-outlined text-primary">analytics</span>
      </div>
      
      <div class="space-y-4 sm:space-y-6">
        <!-- Total Points -->
        <div class="bg-slate-50 dark:bg-white/5 rounded-xl p-3 sm:p-4">
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Total Points</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl sm:text-3xl font-black text-primary">{{ totalPoints.toLocaleString() }}</span>
            <span v-if="pointsGrowth > 0" class="text-xs font-bold text-green-500 flex items-center">
              <span class="material-symbols-outlined text-xs">arrow_upward</span>
              {{ pointsGrowth }}%
            </span>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-slate-50 dark:bg-white/5 rounded-xl p-3 border border-slate-100 dark:border-white/5">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tight mb-1">Weekly Rank</p>
            <p class="text-base sm:text-lg font-black tracking-tight">#{{ weeklyRank }}</p>
          </div>
          <div class="bg-slate-50 dark:bg-white/5 rounded-xl p-3 border border-slate-100 dark:border-white/5">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tight mb-1">Day Streak</p>
            <p class="text-base sm:text-lg font-black tracking-tight">🔥 {{ dayStreak }}</p>
          </div>
        </div>

        <!-- Badge Progress -->
        <div class="pt-2">
          <div class="flex items-center justify-between mb-2">
            <p class="text-xs font-bold text-slate-500">Next Badge: {{ nextBadge }}</p>
            <p class="text-xs font-bold text-primary">{{ badgeProgress }}%</p>
          </div>
          <div class="w-full h-2 bg-slate-100 dark:bg-white/10 rounded-full overflow-hidden">
            <div 
              class="h-full bg-primary rounded-full transition-all duration-300"
              :style="{ width: `${badgeProgress}%` }"
            ></div>
          </div>
        </div>

        <!-- Practice Button -->
        <button 
          @click="handlePracticeClick"
          class="w-full bg-primary text-white py-3 sm:py-4 rounded-xl font-black text-xs sm:text-sm tracking-wide shadow-lg shadow-primary/25 hover:bg-primary/90 transition-all active:scale-[0.98] flex items-center justify-center gap-2"
        >
          <span>PRACTICAR AHORA</span>
          <span class="material-symbols-outlined text-base sm:text-lg">play_arrow</span>
        </button>
      </div>
    </div>

    <!-- Recent Achievements -->
    <div class="bg-white dark:bg-white/5 rounded-2xl p-4 sm:p-6 border border-slate-200 dark:border-white/10">
      <h3 class="font-black mb-4 text-sm sm:text-base">Recent Achievements</h3>
      <div class="space-y-4">
        <div 
          v-for="achievement in achievements" 
          :key="achievement.id"
          class="flex items-center gap-3"
        >
          <div 
            :class="[
              'h-10 w-10 rounded-full flex items-center justify-center shrink-0',
              achievement.color
            ]"
          >
            <span class="material-symbols-outlined text-lg sm:text-xl">{{ achievement.icon }}</span>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-xs font-bold truncate">{{ achievement.title }}</p>
            <p class="text-[10px] text-slate-400">{{ achievement.earnedDate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Links -->
    <div class="hidden lg:flex flex-col gap-1 px-4">
      <a class="flex items-center gap-3 py-2 text-slate-400 hover:text-primary transition-colors" href="#">
        <span class="material-symbols-outlined text-xl">help</span>
        <span class="text-xs font-bold">Help Center</span>
      </a>
      <a class="flex items-center gap-3 py-2 text-slate-400 hover:text-primary transition-colors" href="#">
        <span class="material-symbols-outlined text-xl">settings</span>
        <span class="text-xs font-bold">Ranking Settings</span>
      </a>
    </div>
  </aside>
</template>

<style scoped>
.podium-shadow {
  box-shadow: 0 20px 25px -5px rgba(79, 65, 230, 0.1), 0 10px 10px -5px rgba(79, 65, 230, 0.04);
}
</style>
