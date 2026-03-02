<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import LectureFilters from '@/components/lectures/LectureFilters.vue'
import LectureCard from '@/components/lectures/LectureCard.vue'
import ReadingGenerationModal from '@/components/lectures/ReadingGenerationModal.vue'
import { authService } from '@/services/auth.service'
import { LecturesService } from '@/services/lectures.service'
import { dashboardService } from '@/services/dashboard.service'

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
const showGenerateModal = ref(false)
const loading = ref(false)
const error = ref('')
const userLevel = ref('B1')

const allLectures = ref([])

const normalizeImageUrl = (url) => {
  if (!url) return 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=200&h=200&fit=crop'
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  return `http://localhost:8000${url}`
}

const mapLecture = (lecture) => ({
  id: lecture.id,
  category: lecture.categoria_nombre || 'General',
  title: lecture.titulo || 'Untitled Reading',
  level: lecture.nivel_codigo || 'B1',
  status: lecture.estado_usuario || 'not-started',
  progress: Number(lecture.progreso_usuario ?? 0),
  thumbnail: normalizeImageUrl(lecture.imagen_url_final || lecture.imagen_url),
})

const fetchLectures = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await LecturesService.getMine()
    const lectures = Array.isArray(response.data) ? response.data : (response.data.results || [])
    allLectures.value = lectures.map(mapLecture)
    console.log('Lectures loaded:', allLectures.value)
  } catch (apiError) {
    console.error('Error loading user lectures:', apiError)
    error.value = 'No se pudieron cargar tus lecturas'
    allLectures.value = []
  } finally {
    loading.value = false
  }
}

const fetchUserLevel = async () => {
  try {
    const response = await dashboardService.getFullDashboard()
    const raw = response.data.progressData?.currentLevel || 'B1'
    const rawStr = String(raw || 'B1')
    // Extract CEFR code (A1, A2, B1, B2, C1, C2) if backend returns a full label
    const match = rawStr.match(/(A1|A2|B1|B2|C1|C2)/i)
    const code = match ? match[0].toUpperCase() : rawStr.toUpperCase().trim()
    userLevel.value = code
    console.log('User level loaded (raw):', rawStr, '→ parsed:', userLevel.value)
  } catch (err) {
    console.error('Error loading user level:', err)
    userLevel.value = 'B1'
  }
}

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
        (lecture.title || '').toLowerCase().includes(query) ||
        (lecture.category || '').toLowerCase().includes(query)
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

const handleOpenGenerateModal = () => {
  showGenerateModal.value = true
}

const handleCloseGenerateModal = () => {
  showGenerateModal.value = false
}

const handleReadingGenerated = async () => {
  await fetchLectures()
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

onMounted(async () => {
  await Promise.all([fetchUserLevel(), fetchLectures()])
})
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
        <div class="flex items-center justify-between gap-4 mb-2">
          <div
            @click="handleGoBack"
            class="flex items-center gap-3 group cursor-pointer hover:text-primary transition-colors"
          >
            <span class="material-symbols-outlined text-slate-400 group-hover:text-primary transition-colors">arrow_back</span>
            <h1 class="text-2xl sm:text-3xl font-bold font-display leading-tight">Explore Readings</h1>
          </div>
          <button
            class="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-xl font-bold text-sm shadow-sm hover:bg-primary/90 transition"
            @click="handleOpenGenerateModal"
          >
            <span class="material-symbols-outlined text-lg">add</span>
            New Reading
          </button>
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
      <div v-if="loading" class="py-12 text-center">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto mb-3"></div>
        <p class="text-slate-500 dark:text-slate-400">Cargando lecturas...</p>
      </div>

      <div v-else-if="error" class="py-12 text-center">
        <p class="text-red-500 font-medium">{{ error }}</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
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

    <ReadingGenerationModal
      :open="showGenerateModal"
      :user-level="userLevel"
      @close="handleCloseGenerateModal"
      @reading-generated="handleReadingGenerated"
    />
  </MainDashboard>
</template>
