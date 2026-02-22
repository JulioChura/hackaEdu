<template>
  <MainDashboard
    :activeRoute="currentRoute"
    :userData="studentData"
    :userRole="'Student'"
    :userIsPro="studentData.isPro"
    :unreadNotificationsCount="unreadNotificationsCount"
    @navigate="handleNavigate"
    @upgrade-to-pro="handleUpgradeToPro"
    @open-settings="handleOpenSettings"
    @search="handleSearch"
    @open-notifications="handleNotificationsClick"
    @logout="handleLogout"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
        <p class="text-gray-600">Cargando dashboard...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
      <div class="text-center bg-red-50 p-8 rounded-xl">
        <span class="material-symbols-outlined text-6xl text-red-500 mb-4">error</span>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Error al cargar el dashboard</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button 
          @click="fetchFullDashboard"
          class="bg-primary text-white px-6 py-2 rounded-lg font-bold hover:bg-primary-dark transition-colors"
        >
          Reintentar
        </button>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="max-w-7xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
        <!-- LEFT COLUMN (2/3) -->
        <div class="lg:col-span-2 space-y-4 md:space-y-6 lg:space-y-8">
          <!-- Progress Card -->
          <ProgressCard
            :studentName="studentData.fullName"
            :currentLevel="progressData.currentLevel"
            :levelTitle="progressData.levelTitle"
            :currentPoints="progressData.currentPoints"
            :nextLevelPoints="progressData.nextLevelPoints"
            :nextLevel="progressData.nextLevel"
            @continue-path="handleContinuePath"
            @view-roadmap="handleViewRoadmap"
          />

          <!-- Streak Card -->
          <StreakCard
            :currentStreak="streakData.currentStreak"
            :completedDaysThisWeek="streakData.completedDaysThisWeek"
          />

          <!-- Continue Learning Section -->
          <section>
            <div class="flex items-center justify-between mb-3 md:mb-4">
              <h3 class="text-lg md:text-xl font-bold">Continue Learning</h3>
              <a 
                href="#" 
                @click.prevent="handleSeeAllCourses"
                class="text-primary text-xs md:text-sm font-bold hover:underline"
              >
                See all
              </a>
            </div>

            <div class="space-y-3 md:space-y-4">
              <CourseItem
                v-for="course in activeCourses"
                :key="course.courseId"
                :courseId="course.courseId"
                :courseTitle="course.courseTitle"
                :courseCategory="course.courseCategory"
                :courseThumbnail="course.courseThumbnail"
                :courseProgress="course.courseProgress"
                @play-course="handlePlayCourse"
              />
            </div>
          </section>
        </div>

        <!-- RIGHT COLUMN (1/3) -->
        <div class="space-y-4 md:space-y-6 lg:space-y-8">
          <!-- Global Ranking -->
          <RankingCard
            :userRank="rankingData.userRank"
            :userTopPercentage="rankingData.userTopPercentage"
            :topPlayers="rankingData.topPlayers"
            @view-full-leaderboard="handleViewFullLeaderboard"
          />

          <!-- Latest Achievements -->
          <AchievementsCard
            :latestAchievements="achievementsData"
            @show-all-badges="handleShowAllBadges"
          />

          <!-- Community Card -->
          <section class="bg-gradient-to-br from-primary to-[#7a6ff5] p-4 md:p-6 rounded-xl text-white shadow-lg relative overflow-hidden">
            <div class="relative z-10">
              <h3 class="text-base md:text-lg font-bold mb-2">Join a Study Group</h3>
              <p class="text-xs opacity-90 mb-3 md:mb-4 leading-relaxed">
                Collaborate with other {{ progressData.currentLevel }} students and practice your speaking skills in real-time.
              </p>
              <button 
                @click="handleFindGroups"
                class="bg-white text-primary text-xs font-bold px-4 py-2 rounded-lg shadow-md hover:bg-gray-100 transition-colors"
              >
                Find Groups
              </button>
            </div>
            <!-- Decorative Circle -->
            <div class="absolute -right-8 -bottom-8 w-32 h-32 bg-white/10 rounded-full blur-2xl"></div>
            <span class="material-symbols-outlined absolute right-4 top-4 text-4xl md:text-6xl opacity-20 rotate-12">groups</span>
          </section>
        </div>
      </div>
    </div>
  </MainDashboard>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import MainDashboard from '@/components/layout/MainDashboard.vue';
import ProgressCard from '@/components/mainDashboard/ProgressCard.vue';
import StreakCard from '@/components/mainDashboard/StreakCard.vue';
import CourseItem from '@/components/mainDashboard/CourseItem.vue';
import RankingCard from '@/components/mainDashboard/RankingCard.vue';
import AchievementsCard from '@/components/mainDashboard/AchievementsCard.vue';
import { dashboardService } from '@/services/dashboard.service';
import { authService } from '@/services/auth.service';

const router = useRouter();
const currentRoute = ref('dashboard');
const unreadNotificationsCount = ref(3);
const isLoading = ref(true);
const error = ref(null);

// Datos del estudiante - Valores iniciales mientras carga
const studentData = ref({
  userId: 0,
  fullName: 'Loading...',
  userLevelTitle: 'Loading...',
  avatarUrl: '',
  isPro: false
});

// Datos de progreso - Valores iniciales
const progressData = ref({
  currentLevel: '',
  levelTitle: 'Loading...',
  currentPoints: 0,
  nextLevelPoints: 100,
  nextLevel: ''
});

// Datos de racha - Valores iniciales
const streakData = ref({
  currentStreak: 0,
  completedDaysThisWeek: [false, false, false, false, false, false, false]
});

// Cursos activos - Vacío mientras carga
const activeCourses = ref([]);

// Datos de ranking - Valores iniciales
const rankingData = ref({
  userRank: 0,
  userTopPercentage: 0,
  topPlayers: []
});

// Datos de logros - Vacío mientras carga
const achievementsData = ref([]);


onMounted(async () => {
  await fetchFullDashboard();
});

// EVENT HANDLERS
// ============================================

const handleNavigate = (routeName) => {
  currentRoute.value = routeName;
  router.push({ name: routeName });
};

const handleSearch = (query) => {
  console.log('Search query:', query);
  // TODO: Implementar búsqueda
};

const handleNotificationsClick = () => {
  console.log('Open notifications');
  // TODO: Abrir panel de notificaciones
};

const handleOpenSettings = () => {
  console.log('Open settings');
  // TODO: Navegar a configuración
};

const handleContinuePath = () => {
  console.log('Continue learning path');
  // TODO: Navegar al siguiente curso recomendado
};

const handleViewRoadmap = () => {
  console.log('View roadmap');
  // TODO: Mostrar roadmap de aprendizaje
};

const handleSeeAllCourses = () => {
  console.log('See all courses');
  // TODO: Navegar a página de cursos
};

const handlePlayCourse = (courseData) => {
  console.log('Play course:', courseData);
  // TODO: Navegar a la página del curso
  // router.push({ name: 'course-detail', params: { id: courseData.courseId } });
};

const handleViewFullLeaderboard = () => {
  console.log('View full leaderboard');
  // TODO: Navegar a ranking completo
};

const handleShowAllBadges = () => {
  console.log('Show all badges');
  // TODO: Navegar a página de logros
};

const handleFindGroups = () => {
  console.log('Find study groups');
  // TODO: Navegar a grupos de estudio
};

const handleUpgradeToPro = () => {
  console.log('Upgrade to PRO');
  // TODO: Abrir modal de upgrade
};

const handleLogout = async () => {
  try {
    // Llamar al servicio de logout (limpia tokens)
    authService.logout();
    
    // Redirigir a la página de login
    router.push({ name: 'Login' });
  } catch (err) {
    console.error('Error during logout:', err);
  }
};

// ============================================
// API FUNCTIONS
// ============================================

/**
 * Carga todos los datos del dashboard en una sola llamada
 * Más eficiente que hacer múltiples llamadas individuales
 */
const fetchFullDashboard = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    
    const response = await dashboardService.getFullDashboard();
    
    // Asignar datos a las variables reactivas
    studentData.value = response.data.studentData;
    progressData.value = response.data.progressData;
    streakData.value = response.data.streakData;
    rankingData.value = response.data.rankingData;
    achievementsData.value = response.data.achievementsData;
    activeCourses.value = response.data.activeCourses;
    
    console.log('Dashboard data loaded successfully');
  } catch (err) {
    console.error('Error loading dashboard data:', err);
    error.value = 'Error al cargar los datos del dashboard';
    
    // Mostrar mensaje de error al usuario
    // TODO: Implementar un toast o notificación de error
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Container queries para ProgressCard */
@container (min-width: 480px) {
  /* Estilos aplicados cuando el contenedor tiene al menos 480px */
}
</style>
