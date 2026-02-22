<script setup>
const props = defineProps({
  answeredCount: {
    type: Number,
    default: 0
  },
  totalQuestions: {
    type: Number,
    default: 0
  },
  showFeedback: {
    type: Boolean,
    default: false
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'exit'])

const handleSubmit = () => {
  emit('submit')
}

const handleExit = () => {
  emit('exit')
}

const canSubmit = () => {
  return props.answeredCount === props.totalQuestions && !props.showFeedback
}
</script>

<template>
  <div class="fixed bottom-0 right-0 left-0 bg-white/90 dark:bg-zinc-900/90 backdrop-blur-md border-t border-gray-200 dark:border-zinc-800 p-3 sm:p-4 z-30">
    <div class="max-w-4xl mx-auto flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 sm:gap-0">
      <!-- Progress Status -->
      <div class="flex items-center gap-2 sm:gap-4">
        <div class="flex -space-x-2">
          <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-full border-2 border-white dark:border-zinc-900 bg-gray-200 flex items-center justify-center text-[9px] sm:text-[10px] font-bold">
            {{ answeredCount }}/{{ totalQuestions }}
          </div>
          <div
            v-if="canSubmit()"
            class="w-7 h-7 sm:w-8 sm:h-8 rounded-full border-2 border-white dark:border-zinc-900 bg-green-500 flex items-center justify-center text-white"
          >
            <span class="material-symbols-outlined text-xs sm:text-sm">check</span>
          </div>
        </div>
        <p class="text-xs sm:text-sm font-medium text-medium-gray">
          {{ answeredCount }} of {{ totalQuestions }} answered
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2 sm:gap-3">
        <button
          v-if="showFeedback"
          @click="handleExit"
          class="px-4 sm:px-6 py-2 sm:py-2.5 text-xs sm:text-sm font-bold text-medium-gray hover:text-charcoal dark:hover:text-white transition-colors"
        >
          <span class="hidden sm:inline">Back to Courses</span>
          <span class="sm:hidden">Back</span>
        </button>
        <button
          v-else
          @click="handleExit"
          class="px-4 sm:px-6 py-2 sm:py-2.5 text-xs sm:text-sm font-bold text-medium-gray hover:text-charcoal dark:hover:text-white transition-colors"
        >
          <span class="hidden sm:inline">Exit Test</span>
          <span class="sm:hidden">Exit</span>
        </button>
        <button
          v-if="!showFeedback"
          @click="handleSubmit"
          :disabled="!canSubmit() || isSubmitting"
          :class="[
            'px-4 sm:px-8 py-2 sm:py-2.5 rounded-xl text-xs sm:text-sm font-bold shadow-lg transition-all flex items-center gap-1 sm:gap-2 flex-1 sm:flex-initial justify-center',
            canSubmit() && !isSubmitting
              ? 'bg-primary text-white shadow-primary/20 hover:scale-[1.02] active:scale-[0.98]'
              : 'bg-gray-300 dark:bg-zinc-700 text-gray-500 cursor-not-allowed'
          ]"
        >
          <template v-if="isSubmitting">
            <span>Submitting...</span>
          </template>
          <template v-else>
            <span class="hidden sm:inline">Submit Answers</span>
            <span class="sm:hidden">Submit</span>
          </template>
          <span class="material-symbols-outlined text-base sm:text-xl">arrow_forward</span>
        </button>
      </div>
    </div>
  </div>
</template>
