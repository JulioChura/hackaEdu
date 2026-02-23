<script setup>
import { ref } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const activeTab = ref('prompt')

const setActiveTab = (tab) => {
  activeTab.value = tab
}
</script>

<template>
  <div v-if="props.open" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="emit('close')"></div>

    <div class="relative z-10 w-full max-w-2xl bg-white dark:bg-background-dark rounded-xl shadow-2xl overflow-hidden border border-slate-200 dark:border-slate-800 flex flex-col max-h-[95vh]">
      <header class="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-3">
          <div class="bg-primary/10 p-2 rounded-lg">
            <span class="material-symbols-outlined text-primary text-2xl">auto_stories</span>
          </div>
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100 leading-tight">Create New AI Reading</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400">Choose your input mode to generate material</p>
          </div>
        </div>
        <button class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors group" @click="emit('close')">
          <span class="material-symbols-outlined text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-200">close</span>
        </button>
      </header>

      <div class="px-6 pt-4 border-b border-slate-100 dark:border-slate-800 flex gap-8">
        <button
          class="pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition-colors"
          :class="activeTab === 'prompt' ? 'text-primary border-primary' : 'text-slate-500 dark:text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200'"
          @click="setActiveTab('prompt')"
        >
          <span class="material-symbols-outlined text-lg">psychology</span>
          AI Prompt
        </button>
        <button
          class="pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition-colors"
          :class="activeTab === 'paste' ? 'text-primary border-primary' : 'text-slate-500 dark:text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200'"
          @click="setActiveTab('paste')"
        >
          <span class="material-symbols-outlined text-lg">content_paste</span>
          Paste Text
        </button>
        <button
          class="pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition-colors"
          :class="activeTab === 'pdf' ? 'text-primary border-primary' : 'text-slate-500 dark:text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200'"
          @click="setActiveTab('pdf')"
        >
          <span class="material-symbols-outlined text-lg">upload_file</span>
          Upload PDF
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
        <section>
          <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200 mb-4">Choose Category</label>
          <div class="grid grid-cols-3 gap-4">
            <button class="flex flex-col items-center gap-2 p-4 rounded-xl border-2 border-primary bg-primary/5 transition-all">
              <span class="material-symbols-outlined text-primary text-3xl">memory</span>
              <span class="text-sm font-medium text-primary">Technology</span>
            </button>
            <button class="flex flex-col items-center gap-2 p-4 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-primary/50 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all">
              <span class="material-symbols-outlined text-slate-600 dark:text-slate-400 text-3xl">account_balance</span>
              <span class="text-sm font-medium text-slate-700 dark:text-slate-300">History</span>
            </button>
            <button class="flex flex-col items-center gap-2 p-4 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-primary/50 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all">
              <span class="material-symbols-outlined text-slate-600 dark:text-slate-400 text-3xl">science</span>
              <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Science</span>
            </button>
          </div>
        </section>

        <section>
          <div v-show="activeTab === 'prompt'">
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200" for="prompt">What do you want to learn about?</label>
              <span class="text-[10px] uppercase tracking-wider font-bold text-slate-400">AI Input</span>
            </div>
            <textarea
              id="prompt"
              rows="4"
              class="w-full rounded-lg border border-slate-200 dark:border-slate-700 dark:bg-slate-900/50 focus:border-primary focus:ring-2 focus:ring-primary/30 placeholder:text-slate-400 text-slate-700 dark:text-slate-300 text-sm p-4 resize-none transition-shadow hover:shadow-sm"
              placeholder="Describe a specific topic, paste an article link, or ask for a summary of a complex concept..."
            ></textarea>
            <p class="mt-2 text-xs text-slate-500 italic flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px]">info</span>
              Example: "The impact of renewable energy on urban architecture in Northern Europe."
            </p>
          </div>

          <div v-show="activeTab === 'paste'">
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200" for="pasted-text">Paste your text here</label>
              <span class="text-[10px] uppercase tracking-wider font-bold text-slate-400">0 / 2000 Words</span>
            </div>
            <textarea
              id="pasted-text"
              rows="6"
              class="w-full rounded-lg border border-slate-200 dark:border-slate-700 dark:bg-slate-900/50 focus:border-primary focus:ring-2 focus:ring-primary/30 placeholder:text-slate-400 text-slate-700 dark:text-slate-300 text-sm p-4 resize-none transition-shadow hover:shadow-sm"
              placeholder="Copy and paste an article, essay, or any text you want the AI to analyze and adapt..."
            ></textarea>
          </div>

          <div v-show="activeTab === 'pdf'">
            <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200 mb-2">Upload PDF Document</label>
            <div class="border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl p-8 flex flex-col items-center justify-center bg-slate-50/50 dark:bg-slate-900/20 hover:bg-slate-50 dark:hover:bg-slate-900/40 hover:border-primary/50 transition-all cursor-pointer group">
              <div class="bg-primary/10 p-4 rounded-full mb-3 group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-primary text-3xl">picture_as_pdf</span>
              </div>
              <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Click to upload or drag and drop</p>
              <p class="text-xs text-slate-500 mt-1">Maximum file size: 10MB</p>
              <input type="file" accept=".pdf" class="hidden" />
            </div>
          </div>
        </section>

        <section>
          <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200 mb-2">Skills to improve</label>
          <div class="flex flex-wrap gap-2 p-3 min-h-[52px] bg-slate-50 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-700 rounded-lg focus-within:ring-2 focus-within:ring-primary/30 focus-within:border-primary transition-all">
            <span class="inline-flex items-center gap-1 px-3 py-1 bg-primary text-white text-xs font-semibold rounded-full group cursor-default">
              Inferential Level
              <button class="hover:bg-white/20 rounded-full leading-none flex items-center justify-center p-0.5">
                <span class="material-symbols-outlined text-xs">close</span>
              </button>
            </span>
            <span class="inline-flex items-center gap-1 px-3 py-1 bg-primary text-white text-xs font-semibold rounded-full group cursor-default">
              Academic Vocab
              <button class="hover:bg-white/20 rounded-full leading-none flex items-center justify-center p-0.5">
                <span class="material-symbols-outlined text-xs">close</span>
              </button>
            </span>
            <input
              type="text"
              class="flex-1 bg-transparent border-none p-0 text-sm focus:ring-0 placeholder:text-slate-400 min-w-[120px]"
              placeholder="Type and press Enter..."
            />
          </div>
        </section>

        <section>
          <div class="flex items-center justify-between mb-3">
            <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200">Target Level (CEFR)</label>
            <span class="text-xs text-primary font-medium">Your current level: A2</span>
          </div>
          <div class="flex gap-2">
            <button class="flex-1 py-3 px-2 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 font-bold hover:border-primary/50 hover:bg-primary/5 transition-all text-sm">
              A1
            </button>
            <button class="flex-1 py-3 px-2 rounded-lg border-2 border-primary bg-primary/10 text-primary font-bold text-sm shadow-sm">
              A2
            </button>
            <button class="flex-1 py-3 px-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 font-bold flex flex-col items-center gap-1 grayscale opacity-70 cursor-not-allowed group relative">
              <span class="text-sm">B1</span>
              <span class="material-symbols-outlined text-[16px]">lock</span>
              <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] py-1 px-2 rounded whitespace-nowrap hidden group-hover:block transition-all">Complete A2 to unlock</div>
            </button>
            <button class="flex-1 py-3 px-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 font-bold flex flex-col items-center gap-1 grayscale opacity-70 cursor-not-allowed text-sm">
              B2
              <span class="material-symbols-outlined text-[16px]">lock</span>
            </button>
            <button class="flex-1 py-3 px-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 font-bold flex flex-col items-center gap-1 grayscale opacity-70 cursor-not-allowed text-sm">
              C1
              <span class="material-symbols-outlined text-[16px]">lock</span>
            </button>
            <button class="flex-1 py-3 px-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 font-bold flex flex-col items-center gap-1 grayscale opacity-70 cursor-not-allowed text-sm">
              C2
              <span class="material-symbols-outlined text-[16px]">lock</span>
            </button>
          </div>
        </section>
      </div>

      <footer class="p-6 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
        <button class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-4 px-6 rounded-xl flex items-center justify-center gap-3 shadow-lg shadow-primary/20 transition-all active:scale-[0.98]">
          <span class="material-symbols-outlined">auto_awesome</span>
          Generate Reading with AI
        </button>
        <p class="text-center mt-3 text-[11px] text-slate-400">
          AI can occasionally generate inaccurate information. Please verify important facts.
        </p>
      </footer>
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
  background: #e2e8f0;
  border-radius: 10px;
}
</style>
