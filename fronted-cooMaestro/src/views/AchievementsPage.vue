<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import AchievementsHeader from '@/components/achievements/AchievementsHeader.vue'
import AchievementCard from '@/components/achievements/AchievementCard.vue'
import { authService } from '@/services/auth.service'

const router = useRouter()

// User data for MainDashboard
const studentData = ref({
  userId: 1,
  fullName: 'Student User',
  userLevelTitle: 'B1 - Intermediate',
  avatarUrl: '',
  isPro: false
})

const unreadNotificationsCount = ref(3)

// Mock data - TODO: Replace with API call
const achievements = ref([
  {
    id: 1,
    emoji: '🎯',
    title: 'First Step',
    unlocked: true,
    achievedDate: 'Achieved Oct 12, 2023',
    description: "Bravo! You've successfully completed your first module and joined the community."
  },
  {
    id: 2,
    emoji: '📚',
    title: 'Dedicated Student',
    unlocked: true,
    achievedDate: 'Achieved Nov 05, 2023',
    description: "Consistency is key! You've maintained a 5-day study streak without missing a beat."
  },
  {
    id: 3,
    emoji: '🏆',
    title: 'A1 Master',
    unlocked: true,
    achievedDate: 'Achieved Dec 01, 2023',
    description: 'Perfect score! You completed the A1 level assessment with 100% accuracy.'
  },
  {
    id: 4,
    emoji: '🚀',
    title: 'In Progress',
    unlocked: false,
    progress: 'Need 15 more pts',
    description: 'Complete 5 more advanced quizzes to launch into the next phase of your journey.'
  },
  {
    id: 5,
    emoji: '🤝',
    title: 'Social Butterfly',
    unlocked: false,
    progress: '2/5 Referrals',
    description: 'Invite more friends to join HackaEdu and earn exclusive collaborative rewards.'
  },
  {
    id: 6,
    emoji: '🦉',
    title: 'Night Owl',
    unlocked: false,
    progress: '0% Complete',
    description: 'Study for at least 1 hour after 10:00 PM to unlock this nocturnal badge.'
  }
])

const userLevel = ref(4)
const unlockedCount = ref(3)
const totalCount = ref(7)

const handleGoBack = () => {
  router.push({ name: 'Dashboard' });
}

// MainDashboard handlers
const handleNavigate = (routeName) => {
  router.push({ name: routeName });
}

const handleSearchMain = (query) => {
  console.log('Search query:', query);
}

const handleNotificationsClick = () => {
  console.log('Open notifications');
}

const handleOpenSettings = () => {
  console.log('Open settings');
}

const handleUpgradeToPro = () => {
  console.log('Upgrade to PRO');
}

const handleLogout = async () => {
  authService.logout();
  router.push({ name: 'Login' });
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

    <!-- Achievements Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5 lg:gap-6">
      <AchievementCard
        v-for="achievement in achievements"
        :key="achievement.id"
        :achievement="achievement"
      />
    </div>
    </div>
  </MainDashboard>
</template>
