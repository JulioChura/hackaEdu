<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import LectureFilters from '@/components/lectures/LectureFilters.vue'
import LectureCard from '@/components/lectures/LectureCard.vue'
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

// State
const activeTab = ref('all')
const selectedLevel = ref('all')
const searchQuery = ref('')

// Mock data
const allLectures = ref([
  {
    id: 1,
    category: 'Grammar Master',
    title: 'Past Tense & Irregular Verbs',
    level: 'B1',
    status: 'in-progress',
    progress: 75,
    thumbnail: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=200&h=200&fit=crop'
  },
  {
    id: 2,
    category: 'Vocabulary Builder',
    title: 'Daily Life & Social Scenarios',
    level: 'A2',
    status: 'in-progress',
    progress: 40,
    thumbnail: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=200&h=200&fit=crop'
  },
  {
    id: 3,
    category: 'Listening Practice',
    title: 'Understanding Native Accents',
    level: 'B2',
    status: 'in-progress',
    progress: 15,
    thumbnail: 'https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=200&h=200&fit=crop'
  },
  {
    id: 4,
    category: 'Business Communication',
    title: 'Negotiation Strategies',
    level: 'C1',
    status: 'not-started',
    progress: 0,
    thumbnail: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=200&h=200&fit=crop'
  },
  {
    id: 5,
    category: 'Science & Technology',
    title: 'Artificial Intelligence in Modern Society',
    level: 'B2',
    status: 'completed',
    progress: 100,
    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200&h=200&fit=crop'
  },
  {
    id: 6,
    category: 'Culture & Society',
    title: 'Global Trends in Modern Culture',
    level: 'C2',
    status: 'completed',
    progress: 100,
    thumbnail: 'https://images.unsplash.com/photo-1516321318423-f06f70504c0a?w=200&h=200&fit=crop'
  }
])

// Computed
const filteredLectures = computed(() => {
  return allLectures.value.filter(lecture => {
    // Filter by tab
    if (activeTab.value === 'completed' && lecture.status !== 'completed') return false
    if (activeTab.value === 'not-started' && lecture.status !== 'not-started') return false
    
    // Filter by level
    if (selectedLevel.value !== 'all' && lecture.level !== selectedLevel.value) return false
    
    // Filter by search
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      return (
        lecture.title.toLowerCase().includes(query) ||
        lecture.category.toLowerCase().includes(query)
      )
    }
    
    return true
  })
})

const totalLectures = computed(() => allLectures.value.length)

// Methods
const handleTabChange = (tab) => {
  activeTab.value = tab
}

const handleLevelChange = (level) => {
  selectedLevel.value = level
}

const handleSearch = (query) => {
  searchQuery.value = query
}

const handlePlayLecture = (lectureId) => {
  router.push({ name: 'LectureTake', params: { id: lectureId } });
}

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
    :activeRoute="'AllLectures'"
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
      <!-- Header -->
      <div class="mb-8 sm:mb-10">
        <div 
          @click="handleGoBack"
          class="flex items-center gap-3 mb-2 group cursor-pointer hover:text-primary transition-colors"
        >
          <span class="material-symbols-outlined text-slate-400 group-hover:text-primary transition-colors">arrow_back</span>
          <h1 class="text-2xl sm:text-3xl font-bold font-display leading-tight">Explore Readings</h1>
        </div>
        <p class="text-slate-500 dark:text-slate-400 font-medium text-sm sm:text-base">
          Total: {{ totalLectures }} readings
        </p>
      </div>

      <!-- Filters Section -->
      <div class="mb-6 sm:mb-8">
        <LectureFilters
          :active-tab="activeTab"
          :selected-level="selectedLevel"
          :search-query="searchQuery"
          @tab-change="handleTabChange"
          @level-change="handleLevelChange"
          @search="handleSearch"
        />
      </div>

      <!-- Lectures List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <LectureCard
          v-for="lecture in filteredLectures"
          :key="lecture.id"
          :lecture="lecture"
          @play="handlePlayLecture"
        />

        <!-- Empty State -->
        <div v-if="filteredLectures.length === 0" class="text-center py-12">
          <span class="material-symbols-outlined text-5xl text-slate-300 dark:text-slate-600 mx-auto block mb-4">
            auto_stories
          </span>
          <p class="text-slate-500 dark:text-slate-400 font-medium">No readings found</p>
          <p class="text-slate-400 dark:text-slate-500 text-sm mt-1">Try adjusting your filters or search</p>
        </div>
      </div>

      <!-- View All Button -->
      <div v-if="filteredLectures.length > 0" class="mt-8 sm:mt-10 flex justify-center">
        <button class="group flex items-center gap-2 px-6 sm:px-8 py-2.5 sm:py-3 bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl text-sm font-bold hover:border-primary/50 hover:text-primary transition-all shadow-sm">
          <span>View All {{ totalLectures }} Readings</span>
          <span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform">arrow_forward</span>
        </button>
      </div>
    </div>
  </MainDashboard>
</template>
