<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  selectedAnswer: {
    type: String,
    default: null
  },
  showFeedback: {
    type: Boolean,
    default: false
  }
  ,
  readOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])

const selectOption = (option) => {
  if (props.readOnly) return
  if (!props.showFeedback) {
    emit('select', { questionIndex: props.index, answer: option })
  }
}

const isCorrect = computed(() => {
  if (!props.showFeedback) return null
  return props.selectedAnswer === props.question.respuesta_correcta
})

const getOptionClass = (option) => {
  const baseClass = 'relative cursor-pointer transition-all border-2 rounded-lg p-4'
  
  if (!props.showFeedback) {
    // Modo respuesta
    if (props.selectedAnswer === option) {
      return `${baseClass} border-primary bg-primary/10`
    }
    return `${baseClass} border-gray-200 dark:border-zinc-800 hover:border-primary/50`
  } else {
    // Modo feedback
    if (option === props.question.respuesta_correcta) {
      return `${baseClass} border-green-500 bg-green-50 dark:bg-green-500/10`
    }
    if (props.selectedAnswer === option && option !== props.question.respuesta_correcta) {
      return `${baseClass} border-red-500 bg-red-50 dark:bg-red-500/10`
    }
    return `${baseClass} border-gray-200 dark:border-zinc-800 opacity-50`
  }
}
</script>

<template>
  <div class="bg-white dark:bg-zinc-900 rounded-xl border border-gray-200 dark:border-zinc-800 shadow-sm p-4 sm:p-6">
    <!-- Header -->
    <div class="flex items-start justify-between mb-3 sm:mb-4">
      <span class="bg-primary/10 text-primary text-[9px] sm:text-[10px] font-bold px-2 py-0.5 rounded uppercase">
        Question {{ index + 1 }}
      </span>
      <div v-if="showFeedback" class="flex items-center gap-1 sm:gap-2">
        <span v-if="isCorrect" class="text-green-500 flex items-center gap-1">
          <span class="material-symbols-outlined text-base sm:text-lg">check_circle</span>
          <span class="text-[10px] sm:text-xs font-bold">Correct!</span>
        </span>
        <span v-else class="text-red-500 flex items-center gap-1">
          <span class="material-symbols-outlined text-base sm:text-lg">cancel</span>
          <span class="text-[10px] sm:text-xs font-bold">Incorrect</span>
        </span>
      </div>
    </div>

    <!-- Question Text -->
    <p class="text-sm sm:text-base font-semibold text-charcoal dark:text-white mb-4 sm:mb-6">
      {{ question.texto }}
    </p>

    <!-- Options -->
    <div class="space-y-2 sm:space-y-3">
      <div
        v-for="(option, optionIndex) in question.opciones"
        :key="optionIndex"
        :class="getOptionClass(option)"
        @click="selectOption(option)"
      >
        <div class="flex items-center gap-2 sm:gap-3">
          <div class="w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0"
               :class="{
                 'border-primary bg-primary': selectedAnswer === option && !showFeedback,
                 'border-green-500 bg-green-500': showFeedback && option === question.respuesta_correcta,
                 'border-red-500 bg-red-500': showFeedback && selectedAnswer === option && option !== question.respuesta_correcta,
                 'border-gray-300': selectedAnswer !== option && !showFeedback,
               }">
            <span v-if="selectedAnswer === option || (showFeedback && option === question.respuesta_correcta)" 
                  class="material-symbols-outlined text-white text-xs sm:text-sm">
              check
            </span>
          </div>
          <span class="text-[9px] sm:text-[10px] font-bold text-medium-gray mr-1 sm:mr-2">
            {{ String.fromCharCode(65 + optionIndex) }}
          </span>
          <span class="text-xs sm:text-sm flex-1">{{ option }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
