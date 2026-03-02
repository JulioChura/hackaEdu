<script setup>
import { ref, watch, computed } from 'vue'
import { categoriesService } from '@/services/categories.service'
import { llmService } from '@/services/llm.service'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'reading-generated'])

// UI State
const activeTab = ref('prompt')
const categories = ref([])
const selectedCategory = ref(null)
const loadingCategories = ref(false)
const isGenerating = ref(false)

// Form data
const formData = ref({
  tema: '',
  nivel: 'B1',
  cantidad_preguntas: 5,
  tags: []
})
const tagInput = ref('')

const setActiveTab = (tab) => {
  activeTab.value = tab
}

const selectCategory = (category) => {
  selectedCategory.value = category
}

const selectLevel = (level) => {
  formData.value.nivel = level
}

// Tags management
const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !formData.value.tags.includes(tag)) {
    formData.value.tags.push(tag)
    tagInput.value = ''
  }
}

const removeTag = (index) => {
  formData.value.tags.splice(index, 1)
}

const handleTagKeydown = (event) => {
  if (event.key === 'Enter') {
    event.preventDefault()
    addTag()
  }
}

// Form validation
const isFormValid = computed(() => {
  return formData.value.tema.trim() !== '' && selectedCategory.value !== null
})

// Generate reading
const handleGenerate = async () => {
  if (!isFormValid.value) {
    alert('Por favor completa el tema y selecciona una categoría')
    return
  }

  try {
    isGenerating.value = true

    const payload = {
      tema: formData.value.tema.trim(),
      nivel: formData.value.nivel,
      categoria: selectedCategory.value.codigo,
      modalidad: 'IA_GENERADA',
      cantidad_preguntas: formData.value.cantidad_preguntas,
      tags: formData.value.tags
    }

    console.log('Generating reading with payload:', payload)
    
    const response = await llmService.createReadingWithQuestions(payload)
    
    console.log('Reading generated:', response.data)
    
    // Emitir evento de éxito
    emit('reading-generated', response.data)
    
    // Cerrar el modal
    emit('close')
    
    // Limpiar formulario
    resetForm()
    
  } catch (error) {
    console.error('Error generating reading:', error)
    alert(error.response?.data?.error || 'Error al generar la lectura. Por favor intenta de nuevo.')
  } finally {
    isGenerating.value = false
  }
}

const resetForm = () => {
  formData.value = {
    tema: '',
    nivel: 'B1',
    cantidad_preguntas: 5,
    tags: []
  }
  tagInput.value = ''
  selectedCategory.value = categories.value[0] || null
}

// Cargar categorías cuando se abre el modal
watch(() => props.open, async (isOpen) => {
  if (isOpen && categories.value.length === 0) {
    await loadCategories()
  }
})

const loadCategories = async () => {
  try {
    loadingCategories.value = true
    const response = await categoriesService.getAll()
    console.log('Categories response:', response.data)
    // El backend devuelve un objeto paginado con 'results'
    categories.value = response.data.results || response.data || []
    console.log('Categories loaded:', categories.value)
    // Pre-seleccionar la primera categoría si existe
    if (categories.value.length > 0 && !selectedCategory.value) {
      selectedCategory.value = categories.value[0]
    }
  } catch (error) {
    console.error('Error loading categories:', error)
    categories.value = []
  } finally {
    loadingCategories.value = false
  }
}

// Mapeo de iconos por categoría (puedes ajustar según tus necesidades)
const getCategoryIcon = (categoria) => {
  if (!categoria) return 'folder'
  
  const iconMap = {
    'technology': 'memory',
    'tecnologia': 'memory',
    'ciencia': 'science',
    'historia': 'account_balance',
    'arte': 'palette',
    'negocios': 'business_center',
    'literatura': 'menu_book',
    'salud': 'health_and_safety',
    'deportes': 'sports_soccer',
    'viajes': 'flight',
    'politica': 'gavel',
    'cuentos': 'auto_stories',
    'cultura': 'language',
    'educacion': 'school',
    'general': 'category'
  }
  const codigo = (categoria.codigo || '').toLowerCase()
  return iconMap[codigo] || 'folder'
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
          <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200 mb-4">
            Choose Category
            <span class="text-xs text-slate-400 ml-2">({{ categories.length }} available)</span>
          </label>
          
          <!-- Loading state -->
          <div v-if="loadingCategories" class="grid grid-cols-3 gap-4">
            <div v-for="n in 6" :key="n" class="flex flex-col items-center gap-2 p-4 rounded-xl border border-slate-200 dark:border-slate-700 animate-pulse">
              <div class="w-8 h-8 bg-slate-200 dark:bg-slate-700 rounded-full"></div>
              <div class="w-16 h-4 bg-slate-200 dark:bg-slate-700 rounded"></div>
            </div>
          </div>

          <!-- Categories grid -->
          <div v-else-if="categories.length > 0" class="grid grid-cols-3 gap-4">
            <button
              v-for="category in categories"
              :key="category.codigo"
              class="flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all"
              :class="selectedCategory?.codigo === category.codigo 
                ? 'border-primary bg-primary/5'
                : 'border-slate-200 dark:border-slate-700 hover:border-primary/50 hover:bg-slate-50 dark:hover:bg-slate-800'"
              @click="selectCategory(category)"
            >
              <span 
                class="material-symbols-outlined text-3xl"
                :class="selectedCategory?.codigo === category.codigo 
                  ? 'text-primary'
                  : 'text-slate-600 dark:text-slate-400'"
              >{{ getCategoryIcon(category) }}</span>
              <span 
                class="text-sm font-medium text-center leading-tight"
                :class="selectedCategory?.codigo === category.codigo 
                  ? 'text-primary'
                  : 'text-slate-700 dark:text-slate-300'"
              >{{ category.nombre }}</span>
            </button>
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-8">
            <span class="material-symbols-outlined text-4xl text-slate-300 dark:text-slate-600">category</span>
            <p class="text-slate-500 dark:text-slate-400 text-sm mt-2">No categories available</p>
            <p class="text-xs text-slate-400 mt-1">Check console for errors</p>
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
              v-model="formData.tema"
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
          <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200 mb-2">
            Skills to improve (tags)
            <span v-if="formData.tags.length > 0" class="text-xs text-slate-400 font-normal ml-2">({{ formData.tags.length }})</span>
          </label>
          <div class="flex flex-wrap gap-2 p-3 min-h-[52px] bg-slate-50 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-700 rounded-lg focus-within:ring-2 focus-within:ring-primary/30 focus-within:border-primary transition-all">
            <transition-group name="tag">
              <span
                v-for="(tag, index) in formData.tags"
                :key="tag"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-primary to-primary/90 text-white text-xs font-semibold rounded-full shadow-sm hover:shadow transition-all cursor-default animate-in"
              >
                {{ tag }}
                <button 
                  @click="removeTag(index)" 
                  class="hover:bg-white/20 rounded-full leading-none flex items-center justify-center w-4 h-4 transition-colors group"
                  type="button"
                >
                  <span class="material-symbols-outlined text-[14px] group-hover:rotate-90 transition-transform duration-200">close</span>
                </button>
              </span>
            </transition-group>
            <input
              v-model="tagInput"
              @keydown="handleTagKeydown"
              type="text"
              class="flex-1 bg-transparent border-none p-0 text-sm focus:ring-0 placeholder:text-slate-400 min-w-[120px] outline-none"
              placeholder="Type and press Enter..."
            />
          </div>
          <p class="mt-2 text-xs text-slate-500 dark:text-slate-400 italic flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px]">info</span>
            Example: "simple past", "vocabulary:technology", "level:inferential"
          </p>
        </section>

        <section>
          <div class="flex items-center justify-between mb-3">
            <label class="block text-sm font-semibold text-slate-900 dark:text-slate-200">Target Level (CEFR)</label>
            <span class="text-xs text-slate-400">Selected: <span class="text-primary font-semibold">{{ formData.nivel }}</span></span>
          </div>
          <div class="flex gap-2">
            <button
              v-for="level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']"
              :key="level"
              @click="selectLevel(level)"
              class="flex-1 py-3 px-2 rounded-lg border-2 font-bold text-sm transition-all"
              :class="formData.nivel === level 
                ? 'border-primary bg-primary/10 text-primary shadow-sm' 
                : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:border-primary/50 hover:bg-primary/5'"
            >
              {{ level }}
            </button>
          </div>
        </section>
      </div>

      <footer class="p-6 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
        <button
          @click="handleGenerate"
          :disabled="!isFormValid || isGenerating"
          class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-4 px-6 rounded-xl flex items-center justify-center gap-3 shadow-lg shadow-primary/20 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary"
        >
          <span v-if="isGenerating" class="material-symbols-outlined animate-spin">progress_activity</span>
          <span v-else class="material-symbols-outlined">auto_awesome</span>
          {{ isGenerating ? 'Generating...' : 'Generate Reading with AI' }}
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

/* Tag animations */
.tag-enter-active {
  animation: tagIn 0.3s ease-out;
}

.tag-leave-active {
  animation: tagOut 0.2s ease-in;
}

@keyframes tagIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes tagOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.8);
  }
}

.tag-move {
  transition: transform 0.3s ease;
}
</style>
