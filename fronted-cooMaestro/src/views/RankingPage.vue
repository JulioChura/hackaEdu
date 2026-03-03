<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import PodiumCard from '@/components/ranking/PodiumCard.vue'
import RankingTable from '@/components/ranking/RankingTable.vue'
import ProgressSidebar from '@/components/ranking/ProgressSidebar.vue'
import { authService } from '@/services/auth.service'
import { rankingService } from '@/services/ranking.service'
import { dashboardService } from '@/services/dashboard.service'

const router = useRouter()

// ─── Dashboard layout data ────────────────────────────────────────────────────
const studentData = ref({
  userId: 1,
  fullName: '',
  userLevelTitle: 'B1',
  avatarUrl: '',
  isPro: false,
})
const unreadNotificationsCount = ref(0)

// ─── Ranking state ────────────────────────────────────────────────────────────
const loading = ref(true)
const error = ref(null)

const currentUserId = ref(null)
const currentUserRank = ref(0)
const currentUserPoints = ref(0)
const currentUserTopPct = ref(0)
const totalUsers = ref(0)
const dayStreak = ref(0)

const topThree = ref([])
const leaderboard = ref([])
const recentAchievements = ref([])

// ─── Computed sidebar props ───────────────────────────────────────────────────
const badgeProgress = computed(() => {
  const pts = currentUserPoints.value
  return Math.round((pts % 1000) / 10)
})

const nextBadgeName = computed(() => {
  const milestones = [500, 1000, 2500, 5000, 10000, 25000]
  const next = milestones.find((m) => m > currentUserPoints.value)
  return next ? `${next.toLocaleString()} pts` : 'Max Level'
})

// ─── Helpers ──────────────────────────────────────────────────────────────────
function normalisePlayer(p) {
  return {
    id: p.userId,
    userId: p.userId,
    rank: p.rank,
    name: p.isCurrentUser ? 'You' : p.name,
    avatar: p.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(p.name)}`,
    level: p.level,
    points: p.points,
    isCurrentUser: p.isCurrentUser,
  }
}

// ─── Load data ────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const [rankRes, dashRes] = await Promise.all([
      rankingService.getGlobalRanking(50),
      dashboardService.getFullDashboard().catch(() => null),
    ])

    const r = rankRes.data
    currentUserRank.value = r.userRank || 0
    currentUserPoints.value = r.userPoints || 0
    currentUserTopPct.value = r.userTopPercentage || 0
    totalUsers.value = r.totalUsers || 0
    topThree.value = (r.topThree || []).map(normalisePlayer)
    leaderboard.value = (r.leaderboard || []).map(normalisePlayer)

    if (dashRes) {
      const d = dashRes.data
      studentData.value = d.studentData || studentData.value
      currentUserId.value = d.studentData?.userId ?? null
      dayStreak.value = d.streakData?.currentStreak ?? 0
      recentAchievements.value = (d.achievementsData || []).slice(0, 3).map((a, i) => ({
        id: i,
        icon: 'emoji_events',
        title: a.title,
        earnedDate: '',
        color: 'bg-yellow-100 text-yellow-600',
      }))
    }
  } catch (err) {
    console.error('Error loading ranking:', err)
    error.value = 'Could not load ranking. Please try again.'
  } finally {
    loading.value = false
  }
})

// ─── Navigation ───────────────────────────────────────────────────────────────
const handleGoBack = () => router.push({ name: 'Dashboard' })
const handleNavigate = (routeName) => router.push({ name: routeName })
const handleSearchMain = (query) => console.log('Search:', query)
const handleNotificationsClick = () => console.log('Open notifications')
const handleOpenSettings = () => console.log('Open settings')
const handleUpgradeToPro = () => console.log('Upgrade to PRO')
const handleLogout = () => {
  authService.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <MainDashboard
    :activeRoute="'Ranking'"
    :userData="studentData"
    :userRole="'Student'"
    :userIsPro="studentData.isPro"
    :unreadNotificationsCount="unreadNotificationsCount"
    @navigate="handleNavigate"
    @upgrade-to-pro="handleUpgradeToPro"
    @open-settings="handleOpenSettings"
    @search="handleSearchMain"
    @open-notifications="handleNotificationsClick"
    @logout="handleLogout"
  >
    <div class="max-w-7xl mx-auto">

      <!-- Back Button -->
      <button
        @click="handleGoBack"
        class="flex items-center gap-2 mb-4 text-slate-500 hover:text-primary transition-colors group"
      >
        <span class="material-symbols-outlined text-slate-400 group-hover:text-primary transition-colors">arrow_back</span>
        <span class="text-sm font-medium">Back to Dashboard</span>
      </button>

      <!-- Loading skeleton -->
      <div v-if="loading" class="flex flex-col lg:flex-row gap-6 sm:gap-8 animate-pulse">
        <div class="flex-1 space-y-6">
          <div class="h-16 bg-slate-100 dark:bg-zinc-800 rounded-2xl" />
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="n in 3" :key="n" class="h-56 bg-slate-100 dark:bg-zinc-800 rounded-2xl" />
          </div>
          <div class="h-64 bg-slate-100 dark:bg-zinc-800 rounded-2xl" />
        </div>
        <div class="w-full lg:w-80 space-y-4">
          <div class="h-80 bg-slate-100 dark:bg-zinc-800 rounded-2xl" />
          <div class="h-48 bg-slate-100 dark:bg-zinc-800 rounded-2xl" />
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="flex flex-col items-center justify-center py-24 gap-4 text-slate-500">
        <span class="material-symbols-outlined text-5xl text-slate-300">leaderboard</span>
        <p class="font-medium">{{ error }}</p>
      </div>

      <!-- Main content -->
      <div v-else class="flex flex-col lg:flex-row gap-6 sm:gap-8">

        <!-- Left / Main column -->
        <div class="flex-1 space-y-6 sm:space-y-8">

          <!-- Page Heading + rank pill -->
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h2 class="text-3xl sm:text-4xl font-black tracking-tight mb-2">Global Ranking</h2>
              <p class="text-slate-500 dark:text-slate-400 font-medium text-sm sm:text-base">
                Compete with the best students worldwide and climb the ranks.
                <span v-if="totalUsers > 0" class="text-slate-400">
                  · {{ totalUsers.toLocaleString() }} students
                </span>
              </p>
            </div>

            <!-- Current-rank card -->
            <div
              v-if="currentUserRank > 0"
              class="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl p-3 sm:p-4 flex items-center gap-3 sm:gap-4 podium-shadow self-start"
            >
              <div class="bg-primary/10 text-primary h-10 w-10 sm:h-12 sm:w-12 rounded-xl flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-2xl sm:text-3xl font-bold">trending_up</span>
              </div>
              <div>
                <p class="text-[10px] sm:text-xs uppercase tracking-wider font-bold text-slate-400">Your Current Rank</p>
                <p class="text-lg sm:text-xl font-extrabold text-primary">
                  #{{ currentUserRank }}
                  <span class="text-xs sm:text-sm font-medium text-slate-500">
                    · Top {{ currentUserTopPct }}%
                  </span>
                </p>
              </div>
            </div>
          </div>

          <!-- Podium -->
          <div
            v-if="topThree.length"
            class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 items-end pt-4 sm:pt-8"
          >
            <PodiumCard
              v-for="player in topThree"
              :key="player.id"
              :rank="player.rank"
              :user="player"
            />
          </div>
          <div v-else class="flex flex-col items-center gap-3 py-16 text-slate-400">
            <span class="material-symbols-outlined text-5xl">emoji_events</span>
            <p class="text-sm font-medium">No ranking data yet. Start reading to appear here!</p>
          </div>

          <!-- Leaderboard table -->
          <RankingTable
            v-if="leaderboard.length"
            :users="leaderboard"
            :current-user-id="currentUserId"
          />
        </div>

        <!-- Sidebar -->
        <ProgressSidebar
          :total-points="currentUserPoints"
          :points-growth="0"
          :weekly-rank="currentUserRank"
          :day-streak="dayStreak"
          :next-badge="nextBadgeName"
          :badge-progress="badgeProgress"
          :achievements="recentAchievements"
          @practice-click="() => router.push({ name: 'AllLectures' })"
        />
      </div>

      <!-- Floating mobile CTA -->
      <div class="lg:hidden fixed bottom-6 right-6 z-50">
        <button
          @click="router.push({ name: 'AllLectures' })"
          class="bg-primary text-white size-12 sm:size-14 rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform active:scale-95"
        >
          <span class="material-symbols-outlined">play_arrow</span>
        </button>
      </div>

    </div>
  </MainDashboard>
</template>

<style scoped>
.podium-shadow {
  box-shadow: 0 20px 25px -5px rgba(79, 65, 230, 0.1), 0 10px 10px -5px rgba(79, 65, 230, 0.04);
}
</style>
