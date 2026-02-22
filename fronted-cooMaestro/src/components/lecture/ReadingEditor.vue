<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  nivel: {
    type: String,
    default: 'B1'
  },
  palabras: {
    type: Number,
    default: 0
  }
})
</script>

<template>
  <div class="w-full lg:w-1/2 p-4 sm:p-6 lg:p-8 pb-40 sm:pb-44 lg:border-r border-gray-200 dark:border-zinc-800 overflow-y-auto custom-scrollbar">
    <div class="max-w-2xl mx-auto space-y-4 sm:space-y-6">
      <!-- Header con metadata -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 sm:gap-3">
          <span class="bg-primary/10 text-primary px-2 sm:px-3 py-1 rounded-full text-[10px] sm:text-xs font-bold uppercase">
            {{ nivel }}
          </span>
          <span class="text-[10px] sm:text-xs text-medium-gray">
            {{ palabras }} words
          </span>
        </div>
        <button class="p-1.5 sm:p-2 text-medium-gray hover:text-primary transition-colors" title="Bookmark">
          <span class="material-symbols-outlined text-xl sm:text-2xl">bookmark</span>
        </button>
      </div>

      <!-- Título -->
      <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-charcoal dark:text-white leading-tight">
        {{ title }}
      </h1>

      <!-- Contenido de lectura -->
      <div class="bg-white dark:bg-zinc-900 rounded-xl border border-gray-200 dark:border-zinc-800 shadow-sm p-4 sm:p-6 lg:p-8">
        <div 
          class="prose dark:prose-invert max-w-none text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap"
          v-html="content"
        >
        </div>
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

.prose {
  font-size: 0.875rem;
  line-height: 1.8;
}

@media (min-width: 640px) {
  .prose {
    font-size: 1rem;
  }
}
</style>
