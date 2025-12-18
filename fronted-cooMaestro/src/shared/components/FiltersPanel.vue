<template>
  <aside class="w-full bg-surface p-4 rounded-xl border border-gray-100 shadow-sm space-y-5">
    
    <!-- Búsqueda -->
    <div>
      <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Buscar Curso
      </label>
      <div class="relative">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg">
          search
        </span>
        <input 
          v-model="searchQuery" 
          @input="handleChange"
          placeholder="Nombre, código o semestre..."
          class="w-full pl-10 pr-3 h-11 rounded-lg bg-gray-50 border border-gray-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all text-sm"
        />
      </div>
    </div>

    <!-- Filtro de Estado -->
    <div>
      <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Estado del Curso
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
        Rango de Fechas
      </label>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs text-gray-500 mb-1">Desde</label>
          <input 
            v-model="startDate" 
            @change="handleChange"
            type="date" 
            class="w-full px-3 h-10 rounded-lg border border-gray-200 bg-white text-sm focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
          />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">Hasta</label>
          <input 
            v-model="endDate" 
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
          Aplicar Filtros
        </button>
        <button 
          @click="handleReset"
          class="flex-1 py-3 bg-white border border-gray-200 hover:border-gray-300 rounded-lg text-sm font-semibold text-gray-600 hover:text-gray-800 transition-colors"
        >
          Limpiar
        </button>
      </div>
    </div>

  </aside>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['change', 'apply', 'reset'])

// Variables renombradas para mayor claridad
const searchQuery = ref('')
const courseStatus = ref('all')
const startDate = ref('')
const endDate = ref('')

const handleChange = () => {
  emit('change', { 
    search: searchQuery.value, 
    status: courseStatus.value, 
    startDate: startDate.value, 
    endDate: endDate.value 
  })
}

const setStatus = (status) => {
  courseStatus.value = status
  handleChange()
}

const handleApply = () => {
  emit('apply', { 
    search: searchQuery.value, 
    status: courseStatus.value, 
    startDate: startDate.value, 
    endDate: endDate.value 
  })
}

const handleReset = () => {
  searchQuery.value = ''
  courseStatus.value = 'all'
  startDate.value = ''
  endDate.value = ''
  emit('reset')
}

const statusButtonClass = (status) => {
  const isActive = courseStatus.value === status
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