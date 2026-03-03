<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

// Configure marked for clean, safe output
marked.setOptions({
  breaks: true,   // single line-break → <br>
  gfm: true,      // GitHub Flavoured Markdown
})

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
  },
  badges: {
    type: Array,
    default: () => []
  }
})

// Parse markdown → HTML; fall back to plain text if content has no markdown
const renderedContent = computed(() => marked.parse(props.content || ''))
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

      <div v-if="badges.length" class="flex flex-wrap gap-2">
        <span
          v-for="(badge, index) in badges"
          :key="`${badge}-${index}`"
          class="px-2.5 py-1 rounded-full text-[10px] sm:text-xs font-semibold bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-200"
        >
          {{ badge }}
        </span>
      </div>

      <!-- Título -->
      <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-charcoal dark:text-white leading-tight">
        {{ title }}
      </h1>

      <!-- Contenido de lectura -->
      <div class="bg-white dark:bg-zinc-900 rounded-xl border border-gray-200 dark:border-zinc-800 shadow-sm p-4 sm:p-6 lg:p-8">
        <div 
          class="prose prose-slate dark:prose-invert prose-headings:font-bold prose-headings:text-charcoal dark:prose-headings:text-white prose-p:leading-relaxed prose-a:text-primary hover:prose-a:text-primary-dark prose-strong:text-charcoal dark:prose-strong:text-white prose-blockquote:border-primary prose-blockquote:text-slate-text prose-code:text-primary prose-code:bg-primary/10 prose-code:rounded prose-code:px-1 prose-code:before:content-none prose-code:after:content-none max-w-none"
          v-html="renderedContent"
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
