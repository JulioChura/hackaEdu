<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import AchievementsHeader from '@/components/achievements/AchievementsHeader.vue'
import AchievementCard from '@/components/achievements/AchievementCard.vue'
import { authService } from '@/services/auth.service'
import { achievementsService } from '@/services/achievements.service'
import { dashboardService } from '@/services/dashboard.service'

const router = useRouter()

// User data for MainDashboard
const studentData = ref({
  userId: 1,
  fullName: '',
  userLevelTitle: 'B1',
  avatarUrl: '',
  isPro: false
})

const unreadNotificationsCount = ref(0)

// Achievements data
const achievements = ref([])
const unlockedCount = ref(0)
const totalCount = ref(0)
const userLevel = ref('B1')
const loading = ref(true)
const error = ref(null)

// Load data
onMounted(async () => {
  try {
    // Load achievements and student data in parallel
    const [achievementsRes, dashboardRes] = await Promise.all([
      achievementsService.getAll(),
      dashboardService.getFullDashboard().catch(() => null),
    ])

    const data = achievementsRes.data
    achievements.value = data.achievements || []
    unlockedCount.value = data.unlockedCount || 0
    totalCount.value = data.totalCount || 0

    if (dashboardRes) {
      const d = dashboardRes.data
      studentData.value = d.studentData || studentData.value
      userLevel.value = d.progressData?.currentLevel || 'B1'
    }
  } catch (err) {
    console.error('Error loading achievements:', err)
    error.value = 'Could not load achievements.'
  } finally {
    loading.value = false
  }
})

const handleGoBack = () => {
  router.push({ name: 'Dashboard' })
}

const handleNavigate = (routeName) => {
  router.push({ name: routeName })
}
const handleSearchMain = (query) => console.log('Search:', query)
const handleNotificationsClick = () => console.log('Open notifications')
const handleOpenSettings = () => console.log('Open settings')
const handleUpgradeToPro = () => console.log('Upgrade to PRO')

const handleLogout = async () => {
  authService.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <MainDashboard
    :activeRoute="'Achievements'"
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

      <!-- Header -->
      <AchievementsHeader
        :level="userLevel"
        :unlocked-count="unlockedCount"
        :total-count="totalCount"
      />

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5 lg:gap-6">
        <div
          v-for="n in 6"
          :key="n"
          class="animate-pulse bg-slate-100 dark:bg-zinc-800 rounded-2xl aspect-[3/4]"
        ></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-16 text-slate-500">
        <span class="material-symbols-outlined text-4xl mb-2 block">error_outline</span>
        {{ error }}
      </div>

      <!-- Achievements Grid -->
      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5 lg:gap-6"
      >
        <AchievementCard
          v-for="achievement in achievements"
          :key="achievement.achievementId"
          :achievement="achievement"
        />
      </div>
    </div>
  </MainDashboard>
</template>
