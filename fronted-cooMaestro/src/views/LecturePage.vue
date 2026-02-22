<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ReadingEditor from '@/components/lecture/ReadingEditor.vue'
import QuestionsList from '@/components/lecture/QuestionsList.vue'
import ActionBar from '@/components/lecture/ActionBar.vue'

const route = useRoute()
const router = useRouter()

// State
const loading = ref(true)
const isSubmitting = ref(false)
const showFeedback = ref(false)

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
    // TODO: Llamar API real
    // const lectureId = route.params.id
    // const response = await lectureService.getLecture(lectureId)
    
    // Mock data por ahora
    lectureData.value = {
      id: 1,
      titulo: 'The Impact of Artificial Intelligence on Modern Education',
      contenido: `Artificial intelligence (AI) is transforming education in profound ways. From personalized learning paths to automated grading systems, AI technologies are helping teachers and students achieve better outcomes.

One of the most significant benefits of AI in education is personalization. Traditionally, teachers have struggled to meet the individual needs of every student in a large classroom. AI-powered platforms can analyze a student's performance in real-time and adjust the difficulty level of materials accordingly.

However, the rise of AI also brings challenges. Ethical considerations regarding data privacy and the potential for algorithmic bias must be addressed. Furthermore, there is a growing debate about the role of human teachers in an increasingly automated environment. While AI can handle administrative tasks and basic instruction, the mentorship and emotional support provided by educators remain irreplaceable.

As we look to the future, the goal is not to replace teachers with machines but to create a collaborative environment where AI acts as a powerful assistant, enabling a more inclusive and effective educational experience for all learners worldwide.`,
      nivel: 'B1',
      palabras: 245,
      preguntas: [
        {
          texto: "What is cited as one of the most significant benefits of AI in education?",
          opciones: ["Personalized learning", "Replacing human teachers", "Lowering school budgets", "Increasing homework volume"],
          respuesta_correcta: "Personalized learning"
        },
        {
          texto: "Which concern is NOT mentioned regarding the rise of AI?",
          opciones: ["Data privacy", "Algorithmic bias", "Teacher's role", "Cost of internet access"],
          respuesta_correcta: "Cost of internet access"
        },
        {
          texto: "What role should AI take according to the concluding paragraph?",
          opciones: ["Lead administrator", "Powerful assistant", "Total replacement", "Strict examiner"],
          respuesta_correcta: "Powerful assistant"
        }
      ]
    }
  } catch (error) {
    console.error('Error loading lecture:', error)
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
    // TODO: Enviar respuestas al backend
    // const response = await lectureService.submitAnswers({
    //   lectureId: lectureData.value.id,
    //   answers: userAnswers.value
    // })
    
    // Simular delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
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

onMounted(() => {
  loadLecture()
  startTimer()
})

onBeforeUnmount(() => {
  stopTimer()
})
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center min-h-screen bg-background-light dark:bg-background-dark">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-medium-gray">Loading lecture...</p>
    </div>
  </div>

  <div v-else class="flex flex-col lg:flex-row min-h-screen bg-background-light dark:bg-background-dark">
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
</template>

<style scoped>
/* Component-specific styles are in individual components */
</style>
