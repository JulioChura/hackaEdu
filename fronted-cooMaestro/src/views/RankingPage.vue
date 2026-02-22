<script setup>
import { ref } from 'vue'
import PodiumCard from '@/components/ranking/PodiumCard.vue'
import RankingTable from '@/components/ranking/RankingTable.vue'
import ProgressSidebar from '@/components/ranking/ProgressSidebar.vue'

// Mock data - TODO: Replace with API call
const currentUserId = ref(7)
const currentUserRank = ref(142)

const topThree = ref([
  {
    id: 1,
    rank: 1,
    name: 'Maria Garcia',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria',
    level: 'C2',
    points: 15840
  },
  {
    id: 2,
    rank: 2,
    name: 'Alex Thompson',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
    level: 'C1',
    points: 14210
  },
  {
    id: 3,
    rank: 3,
    name: 'Kenji Sato',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Kenji',
    level: 'B2',
    points: 13950
  }
])

const rankingList = ref([
  {
    id: 4,
    rank: 4,
    name: 'Elena Rodriguez',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Elena',
    level: 'C1',
    points: 11200
  },
  {
    id: 5,
    rank: 5,
    name: 'David Chen',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=David',
    level: 'B2',
    points: 10850
  },
  {
    id: 7,
    rank: 142,
    name: 'You',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=You',
    level: 'B2',
    points: 5420
  },
  {
    id: 6,
    rank: 6,
    name: 'Sarah Jenkins',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
    level: 'C2',
    points: 10500
  },
  {
    id: 8,
    rank: 7,
    name: 'Lukas Muller',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Lukas',
    level: 'B1',
    points: 9900
  }
])

const userProgress = ref({
  totalPoints: 12450,
  pointsGrowth: 12,
  weeklyRank: 82,
  dayStreak: 14,
  nextBadge: 'Scholar III',
  badgeProgress: 85
})

const recentAchievements = ref([
  {
    id: 1,
    icon: 'emoji_events',
    title: 'Top 5% Monthly',
    earnedDate: 'Earned 2 days ago',
    color: 'bg-yellow-100 text-yellow-600'
  },
  {
    id: 2,
    icon: 'bolt',
    title: 'Speed Demon',
    earnedDate: 'Earned 5 days ago',
    color: 'bg-blue-100 text-blue-600'
  }
])

const handlePracticeClick = () => {
  console.log('Practice clicked')
  // TODO: Navigate to practice page
}
</script>

<template>
  <div class="w-full px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
    <div class="flex flex-col lg:flex-row gap-6 sm:gap-8">
      <!-- Main Ranking Area -->
      <div class="flex-1 space-y-6 sm:space-y-8">
        <!-- Page Heading -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h2 class="text-3xl sm:text-4xl font-black tracking-tight mb-2">Global Ranking</h2>
            <p class="text-slate-500 dark:text-slate-400 font-medium text-sm sm:text-base">
              Compete with the best students worldwide and climb the ranks.
            </p>
          </div>
          
          <!-- Current Rank Card -->
          <div class="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl p-3 sm:p-4 flex items-center gap-3 sm:gap-4 podium-shadow self-start">
            <div class="bg-primary/10 text-primary h-10 w-10 sm:h-12 sm:w-12 rounded-xl flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-2xl sm:text-3xl font-bold">trending_up</span>
            </div>
            <div>
              <p class="text-[10px] sm:text-xs uppercase tracking-wider font-bold text-slate-400">Your Current Rank</p>
              <p class="text-lg sm:text-xl font-extrabold text-primary">
                #{{ currentUserRank }} 
                <span class="text-xs sm:text-sm font-medium text-slate-500">Global</span>
              </p>
            </div>
          </div>
        </div>

        <!-- Podium Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 items-end pt-4 sm:pt-8">
          <PodiumCard
            v-for="user in topThree"
            :key="user.id"
            :rank="user.rank"
            :user="user"
          />
        </div>

        <!-- Ranking Table -->
        <RankingTable 
          :users="rankingList"
          :current-user-id="currentUserId"
        />
      </div>

      <!-- Sidebar -->
      <ProgressSidebar
        :total-points="userProgress.totalPoints"
        :points-growth="userProgress.pointsGrowth"
        :weekly-rank="userProgress.weeklyRank"
        :day-streak="userProgress.dayStreak"
        :next-badge="userProgress.nextBadge"
        :badge-progress="userProgress.badgeProgress"
        :achievements="recentAchievements"
        @practice-click="handlePracticeClick"
      />
    </div>

    <!-- Floating Mobile CTA -->
    <div class="lg:hidden fixed bottom-6 right-6 z-50">
      <button 
        @click="handlePracticeClick"
        class="bg-primary text-white size-12 sm:size-14 rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform active:scale-95"
      >
        <span class="material-symbols-outlined">play_arrow</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.podium-shadow {
  box-shadow: 0 20px 25px -5px rgba(79, 65, 230, 0.1), 0 10px 10px -5px rgba(79, 65, 230, 0.04);
}
</style>
