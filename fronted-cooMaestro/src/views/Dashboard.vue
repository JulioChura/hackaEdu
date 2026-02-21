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
  >
    <!-- Dashboard Content -->
    <div class="max-w-7xl mx-auto">
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
import MainDashboard from '@/components/layout/MainDashboard.vue';
import ProgressCard from '@/components/mainDashboard/ProgressCard.vue';
import StreakCard from '@/components/mainDashboard/StreakCard.vue';
import CourseItem from '@/components/mainDashboard/CourseItem.vue';
import RankingCard from '@/components/mainDashboard/RankingCard.vue';
import AchievementsCard from '@/components/mainDashboard/AchievementsCard.vue';

// ============================================
// REACTIVE DATA (Reemplazar con API calls)
// ============================================

const currentRoute = ref('dashboard');
const unreadNotificationsCount = ref(3);

// Datos del estudiante
const studentData = ref({
  userId: 1,
  fullName: 'Alex Chen',
  userLevelTitle: 'Advanced Learner',
  avatarUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDBE66TKuNHKTpzX9oBtpikVOWSw17WhCV7InnSv5LfJc_p9-6cbAkIkdf8dfmrdovHenWVQYih6QsdW6zhjzop5pYtibOM6MmikKqiPY5y0RcPCWTG_YFpo4j4_ooGJ9H8US3NYgZTm6e8_-A52BL4-sOo2D8Xgbdd7qhBK0GJoGAwi7XoQUY5idMnjPAXnNCzvW7JU0sbfxHvd2UR9ubr50WykFdBwnioDaYnXuYheo_7tm74rymt7s787GdliOlv9LV9EagydNVF',
  isPro: false
});

// Datos de progreso
const progressData = ref({
  currentLevel: 'A2',
  levelTitle: 'Elementary Mastery',
  currentPoints: 25,
  nextLevelPoints: 40,
  nextLevel: 'B1 Intermediate'
});

// Datos de racha
const streakData = ref({
  currentStreak: 5,
  completedDaysThisWeek: [true, true, true, true, true, false, false]
});

// Cursos activos
const activeCourses = ref([
  {
    courseId: 1,
    courseTitle: 'Past Tense & Irregular Verbs',
    courseCategory: 'Grammar Master',
    courseThumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC2Wo_U3KavoLct1SbgdahqIm6HCI4g9JOmGbI1g23x-FkwqsbMxfC3TyCk8q7ixTgsMWKLB0Lha7LaVznu3qlgoGD1gjcJlDpf3FvDZ9bhizVmpaQsB8t-vtdjNhXlJ6T31WdzOMX_gdivXzUEIUt7jy8d4Bzt3bEQ6zH2mPvUtGLiVSler8iBb2qzOn5SDEzpnZWPOL-Baldh6tJ2Yp0G9HjhaWYD6ea3MrzWVGGIg324WRjyPTk9InhTKXJlnSjSthhbhtJXrtB3',
    courseProgress: 75
  },
  {
    courseId: 2,
    courseTitle: 'Daily Life & Social Scenarios',
    courseCategory: 'Vocabulary Builder',
    courseThumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAk2vO0zmelLtijAtGyODH2yMpwT9OTMYsM6R_juJFmOUKUTi4PzdsZbGkI9b9GW-xQFSRoDbJXJDMSSgf_-diz1fWz0Q6vQet0ixX-9Hksco40D-H-OfRKBQDe08_G8IyZozHyyz099NHh5oCGxV0dxJCFSUltadbzjpuAMEbAcL9enynus29rVxDd9N-Gu8SGJAyi2MfiAh48y5TqOwzROfHDv4bLYwv5ROaKrM5BlKNArxNiVcgrB7Kd24XCLgXTqbmgMRduhAkM',
    courseProgress: 40
  },
  {
    courseId: 3,
    courseTitle: 'Understanding Native Accents',
    courseCategory: 'Listening Practice',
    courseThumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBOhU9e1hdCqOaDEGHv-2EAlLyzkIWr72NB16N6-EGjo2riUCTpdRsgF_SP1eqabxBQjf4avPftq5D4pUwSKWzFymMiTu7Asxh5k6bLxbLDkjR-GAC1VIeu4du3pEV-BLz-NhHsZ9gr6nk3W-HQBgdu6-h5A3UGF2Brearx8iQ5o6CwlPbdsx1xilPCqXgNaFAosCKuMVY2cZzPneOTnrdiWF5nt2zAvzRrFyUzzEwB_2LmgasZW1fTnqLDYUlxdFDTI08_LVOcVXKs',
    courseProgress: 15
  }
]);

// Datos de ranking
const rankingData = ref({
  userRank: 142,
  userTopPercentage: 5,
  topPlayers: [
    {
      userId: 101,
      userName: 'Sarah Jenkins',
      avatarUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAXJQbIvbSB5XNROvCHqd75suo-26ebQTv1Rg6QeTI53qzIwC9DsarrEtX5-mbwZkrzYSglQ7YupBaVWFe15ki1lksrCklrDIw7WR0V87g3nOaO9AX6Gn7nOzIpBRzvnHpwECuZJrWJI2XZr6m8Tee5iutRmI4ioC--W2Opp8lpmZOmJ9KNUv-nJbqA3p52GWTsr3pqJ7ou1_zaOXHMfusnSVgmdjiBv8udXdRZT9tpFl7wb2uG-pT9wV0j8RTO20yYRNYsgF3sWbgu',
      points: 2450
    },
    {
      userId: 102,
      userName: 'Marco Rossi',
      avatarUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDoMjF__P8Enp6qGdc6vZr4FijROzDyN2dswn2Ff3IlJx4oFmJuFglAgj8ZDBTgjX7tIRg5pBqhyENlisb5JEXQD5sxusKmPkrtyprndmeWM_cNR6inHtLRrCYrZf3lF0sKt4umlVIFbGb95HClY-Z7zYNEuozRR1gJa3arw8brJEJlK2mY9YdtjRXwaMcLSAZI3a4DPfswMUah9Hian2Ym7jTzTqJuy8b4AlmGuWLpdsvumzlxSccZTmTkt7MTkEtDSIOgxHZKQ-O1',
      points: 2120
    },
    {
      userId: 103,
      userName: 'Lisa Wang',
      avatarUrl: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDCJ-o2pNfXpOUVMRPMCDVfGNnCDIQlEEOQFvc9pwpMYTGHf6bEyeKlOswbOvJz1zwraTZgpNOyiL157LOLmUwJF1EDFOEHeoU4EhU5XESzNlKsQt7uWagqzCQPvCrXevnkboRJYGpSjcKKdMSAzakWk4mjmzrmJDts3qPvhKTzDb4l0e1t_Gf_lHZD-3XEsIg74CCphz4FYK9E573myzEIoHtH7rJTnsV0g6vW3ePDenBcDWaM3HSyocCBvcq_vRa0xq8VArvb0wPA',
      points: 1980
    }
  ]
});

// Datos de logros
const achievementsData = ref([
  {
    achievementId: 1,
    title: 'First Step',
    description: 'Completed first lesson',
    iconName: 'footprint'
  },
  {
    achievementId: 2,
    title: 'Dedicated Learner',
    description: 'Study for 7 days straight',
    iconName: 'calendar_month'
  },
  {
    achievementId: 3,
    title: 'A1 Master',
    description: 'Certified in Elementary English',
    iconName: 'stars'
  }
]);

// ============================================
// LIFECYCLE HOOKS
// ============================================

onMounted(() => {
  // TODO: Cargar datos del estudiante desde API
  // fetchStudentData();
  // fetchProgressData();
  // fetchActiveCourses();
  // fetchRankingData();
  // fetchAchievementsData();
  console.log('Dashboard mounted - Ready to connect to API');
});

// ============================================
// EVENT HANDLERS
// ============================================

const handleNavigate = (routeName) => {
  currentRoute.value = routeName;
  console.log('Navigate to:', routeName);
  // TODO: Implementar navegación con Vue Router
  // router.push({ name: routeName });
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

// ============================================
// API FUNCTIONS (Para implementar después)
// ============================================

// const fetchStudentData = async () => {
//   try {
//     const response = await axios.get('/api/student/profile');
//     studentData.value = response.data;
//   } catch (error) {
//     console.error('Error fetching student data:', error);
//   }
// };

// const fetchProgressData = async () => {
//   try {
//     const response = await axios.get('/api/student/progress');
//     progressData.value = response.data;
//   } catch (error) {
//     console.error('Error fetching progress data:', error);
//   }
// };

// const fetchActiveCourses = async () => {
//   try {
//     const response = await axios.get('/api/student/active-courses');
//     activeCourses.value = response.data;
//   } catch (error) {
//     console.error('Error fetching active courses:', error);
//   }
// };

// const fetchRankingData = async () => {
//   try {
//     const response = await axios.get('/api/ranking/global');
//     rankingData.value = response.data;
//   } catch (error) {
//     console.error('Error fetching ranking data:', error);
//   }
// };

// const fetchAchievementsData = async () => {
//   try {
//     const response = await axios.get('/api/student/achievements');
//     achievementsData.value = response.data;
//   } catch (error) {
//     console.error('Error fetching achievements:', error);
//   }
// };
</script>

<style scoped>
/* Container queries para ProgressCard */
@container (min-width: 480px) {
  /* Estilos aplicados cuando el contenedor tiene al menos 480px */
}
</style>
