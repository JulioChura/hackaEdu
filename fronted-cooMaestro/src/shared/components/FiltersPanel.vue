<template>
  <aside class="w-full bg-surface p-4 rounded-xl border border-gray-100 shadow-sm space-y-5">
    
    <!-- Búsqueda -->
    <div>
      <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Search Classroom
      </label>
      <div class="relative">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg">
          search
        </span>
        <input 
          v-model="q" 
          @input="handleChange"
          placeholder="Name, code or semester..."
          class="w-full pl-10 pr-3 h-11 rounded-lg bg-gray-50 border border-gray-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all text-sm"
        />
      </div>
    </div>

    <!-- Filtro de Estado -->
    <div>
      <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Classroom Status
      </label>
      <div class="flex gap-2">
        <button 
          @click="setStatus('all')"
          :class="statusButtonClass('all')"
          class="flex-1 py-2.5 px-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-1.5"
        >
          <span class="material-symbols-outlined text-sm">
            all_inclusive
          </span>
          Todos
        </button>
        <button 
          @click="setStatus('active')"
          :class="statusButtonClass('active')"
          class="flex-1 py-2.5 px-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-1.5"
        >
          <span class="material-symbols-outlined text-sm">
            play_circle
          </span>
          Activos
        </button>
        <button 
          @click="setStatus('archived')"
          :class="statusButtonClass('archived')"
          class="flex-1 py-2.5 px-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-1.5"
        >
          <span class="material-symbols-outlined text-sm">
            archive
          </span>
          Archivados
        </button>
      </div>
    </div>

    <!-- Filtro por Fecha -->
    <div>
      <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Date Range
      </label>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs text-gray-500 mb-1">From</label>
          <input 
            v-model="from" 
            @change="handleChange"
            type="date" 
            class="w-full px-3 h-10 rounded-lg border border-gray-200 bg-white text-sm focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
          />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">To</label>
          <input 
            v-model="to" 
            @change="handleChange"
            type="date" 
            class="w-full px-3 h-10 rounded-lg border border-gray-200 bg-white text-sm focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
          />
        </div>
      </div>
    </div>

    <!-- Acciones -->
    <div class="pt-2">
      <div class="flex gap-3 ">
        <button 
          @click="handleApply"
          class="bg-blue-800 flex-1 py-3 bg-primary hover:bg-primary-dark text-white rounded-lg text-sm font-semibold transition-colors shadow-sm hover:shadow"
        >
          Apply Filters
        </button>
        <button 
          @click="handleReset"
          class="flex-1 py-3 bg-white border border-gray-200 hover:border-gray-300 rounded-lg text-sm font-semibold text-gray-600 hover:text-gray-800 transition-colors"
        >
          Clear
        </button>
      </div>
    </div>

  </aside>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['change', 'apply', 'reset'])

// Internal filter state (classroom terminology)
const q = ref('')
const classroomStatus = ref('all')
const from = ref('')
const to = ref('')

const handleChange = () => {
  emit('change', { 
    q: q.value, 
    status: classroomStatus.value, 
    from: from.value, 
    to: to.value 
  })
}

const setStatus = (status) => {
  classroomStatus.value = status
  handleChange()
}

const handleApply = () => {
  emit('apply', { 
    q: q.value, 
    status: classroomStatus.value, 
    from: from.value, 
    to: to.value 
  })
}

const handleReset = () => {
  q.value = ''
  classroomStatus.value = 'all'
  from.value = ''
  to.value = ''
  emit('reset')
}

const statusButtonClass = (status) => {
  const isActive = classroomStatus.value === status
  return isActive 
    ? 'bg-blue-800 text-white shadow-sm' 
    : 'bg-white text-blue-600 border border-gray-200 hover:border-gray-300'
}
</script>

<style scoped>
/* Mejorar la legibilidad de los placeholders */
input::placeholder {
  color: #9CA3AF;
  opacity: 1;
}

/* Estilo consistente para iconos */
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 20;
}

/* Transiciones suaves */
button, input {
  transition: all 0.2s ease;
}
</style>