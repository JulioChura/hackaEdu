<script setup>
import QuestionCard from './QuestionCard.vue'
import { computed } from 'vue'

const props = defineProps({
  questions: {
    type: Array,
    default: () => []
  },
  userAnswers: {
    type: Object,
    default: () => ({})
  },
  showFeedback: {
    type: Boolean,
    default: false
  },
  timeRemaining: {
    type: Number,
    default: 900
  }
})

const emit = defineEmits(['select-answer'])

const handleSelectAnswer = (payload) => {
  emit('select-answer', payload)
}

const answeredCount = computed(() => {
  return Object.keys(props.userAnswers).length
})

const progressPercentage = computed(() => {
  if (props.questions.length === 0) return 0
  return Math.round((answeredCount.value / props.questions.length) * 100)
})

const formatTime = computed(() => {
  const mins = Math.floor(props.timeRemaining / 60)
  const secs = props.timeRemaining % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
})

const timeColor = computed(() => {
  if (props.timeRemaining < 60) return 'text-red-600 dark:text-red-400'
  if (props.timeRemaining < 300) return 'text-amber-600 dark:text-amber-400'
  return 'text-green-600 dark:text-green-400'
})
</script>

<template>
  <div class="w-full lg:w-1/2 bg-gray-50/50 dark:bg-zinc-900/30 overflow-y-auto custom-scrollbar p-4 sm:p-6 lg:p-8 pb-40 sm:pb-44">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="mb-4 sm:mb-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-start justify-between gap-3 sm:gap-4 mb-2">
          <div class="flex-1">
            <h2 class="text-lg sm:text-xl font-bold flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">quiz</span>
              Answer the Questions
            </h2>
            <p class="text-xs sm:text-sm text-medium-gray mt-1">
              {{ answeredCount }} of {{ questions.length }} questions answered
            </p>
          </div>
          
          <!-- Timer -->
          <div class="flex items-center gap-2 px-3 py-2 rounded-lg bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 self-start">
            <span class="material-symbols-outlined text-base sm:text-lg" :class="timeColor">schedule</span>
            <div>
              <p class="text-[9px] sm:text-[10px] font-bold uppercase tracking-wider text-medium-gray">Time Left</p>
              <p class="text-base sm:text-lg font-bold font-mono" :class="timeColor">{{ formatTime }}</p>
            </div>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-4 h-2 bg-gray-200 dark:bg-zinc-800 rounded-full overflow-hidden">
          <div 
            class="h-full bg-primary transition-all duration-300"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
      </div>

      <!-- Questions List -->
      <div class="space-y-4">
        <QuestionCard
          v-for="(question, index) in questions"
          :key="index"
          :question="question"
          :index="index"
          :selected-answer="userAnswers[index]"
          :show-feedback="showFeedback"
          @select="handleSelectAnswer"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #3f3f46;
}
</style>
