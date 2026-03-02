<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainDashboard from '@/components/layout/MainDashboard.vue'
import ReadingEditor from '@/components/testLecture/ReadingEditor.vue'
import QuestionsList from '@/components/testLecture/QuestionsList.vue'
import ActionBar from '@/components/testLecture/ActionBar.vue'
import { authService } from '@/services/auth.service'
import { LecturesService } from '@/services/lectures.service'

const route = useRoute()
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
const loading = ref(true)
const isSubmitting = ref(false)
const showFeedback = ref(false)
const sessionId = ref(null)

// Timer
const timeRemaining = ref(900) // 15 minutos
const timerInterval = ref(null)

const lectureData = ref({
  id: null,
  titulo: '',
  contenido: '',
  nivel: 'B1',
  palabras: 0,
  preguntas: []
})

const userAnswers = ref({})

// Computed
const answeredCount = computed(() => Object.keys(userAnswers.value).length)
const totalQuestions = computed(() => lectureData.value.preguntas.length)

// Methods
const loadLecture = async () => {
  loading.value = true
  
  try {
    const lectureId = route.params.id
    const response = await LecturesService.startSession(lectureId)
    const sessionData = response.data

    sessionId.value = sessionData.id
    timeRemaining.value = sessionData.tiempo_restante_segundos ?? 900

    lectureData.value = {
      id: sessionData.lectura?.id,
      titulo: sessionData.lectura?.titulo || '',
      contenido: sessionData.lectura?.contenido || '',
      nivel: sessionData.lectura?.nivel_codigo || 'B1',
      palabras: sessionData.lectura?.palabras_count || 0,
      preguntas: sessionData.preguntas || []
    }

    startTimer()
  } catch (error) {
    console.error('Error loading lecture:', error)
    alert('Error loading lecture. Please try again.')
    router.push({ name: 'AllLectures' })
  } finally {
    loading.value = false
  }
}

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--
    } else {
      handleSubmit() // Auto-submit al acabarse el tiempo
    }
  }, 1000)
}

const stopTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const handleSelectAnswer = ({ questionIndex, answer }) => {
  userAnswers.value[questionIndex] = answer
}

const handleSubmit = async () => {
  if (answeredCount.value !== totalQuestions.value && timeRemaining.value > 0) {
    alert('Please answer all questions before submitting')
    return
  }
  
  stopTimer()
  isSubmitting.value = true

  try {
    const respuestas = Object.entries(userAnswers.value).map(([questionIndex, answer]) => {
      const question = lectureData.value.preguntas[Number(questionIndex)]
      return {
        pregunta_id: question?.id,
        respuesta: answer,
      }
    }).filter((item) => !!item.pregunta_id)

    if (sessionId.value) {
      const response = await LecturesService.finalizeSession(
        sessionId.value,
        respuestas,
        timeRemaining.value
      )
      if (response.data?.preguntas?.length) {
        lectureData.value.preguntas = response.data.preguntas
      }
    }
    
    showFeedback.value = true
  } catch (error) {
    console.error('Error submitting answers:', error)
    alert('Error submitting answers. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

const handleExit = () => {
  if (!showFeedback.value && answeredCount.value > 0) {
    if (!confirm('Are you sure you want to exit? Your progress will be lost.')) {
      return
    }
  }
  stopTimer()
  router.push({ name: 'Dashboard' })
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

onMounted(() => {
  loadLecture()
})

onBeforeUnmount(() => {
  stopTimer()
})
</script>

<template>
  <MainDashboard
    :activeRoute="'LectureTake'"
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
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
        <p class="text-medium-gray">Loading lecture...</p>
      </div>
    </div>

    <div v-else class="flex flex-col lg:flex-row min-h-[calc(100vh-120px)]">
    <!-- Reading Display (Left/Top) -->
    <ReadingEditor
      :title="lectureData.titulo"
      :content="lectureData.contenido"
      :nivel="lectureData.nivel"
      :palabras="lectureData.palabras"
    />

    <!-- Questions List (Right/Bottom) -->
    <QuestionsList
      :questions="lectureData.preguntas"
      :user-answers="userAnswers"
      :show-feedback="showFeedback"
      :time-remaining="timeRemaining"
      @select-answer="handleSelectAnswer"
    />

      <!-- Action Bar (Bottom Fixed) -->
      <ActionBar
        :answered-count="answeredCount"
        :total-questions="totalQuestions"
        :show-feedback="showFeedback"
        :is-submitting="isSubmitting"
        @submit="handleSubmit"
        @exit="handleExit"
      />
    </div>
  </MainDashboard>
</template>

<style scoped>
/* Component-specific styles are in individual components */
</style>
