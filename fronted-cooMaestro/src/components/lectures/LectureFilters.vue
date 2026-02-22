<script setup>
const props = defineProps({
  activeTab: {
    type: String,
    default: 'all'
  },
  selectedLevel: {
    type: String,
    default: 'all'
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['tab-change', 'level-change', 'search'])

const tabs = [
  { id: 'all', label: 'All' },
  { id: 'not-started', label: 'Not Started' },
  { id: 'completed', label: 'Completed' }
]

const levels = [
  { value: 'all', label: 'Level: All' },
  { value: 'A1', label: 'A1 - Beginner' },
  { value: 'A2', label: 'A2 - Elementary' },
  { value: 'B1', label: 'B1 - Intermediate' },
  { value: 'B2', label: 'B2 - Upper Intermediate' },
  { value: 'C1', label: 'C1 - Advanced' },
  { value: 'C2', label: 'C2 - Proficiency' }
]
</script>

<template>
  <div class="bg-white dark:bg-slate-800 p-3 sm:p-4 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700/50 space-y-3">
    <div class="flex flex-col sm:flex-row gap-3">
      <!-- Tab Buttons -->
      <div class="flex bg-slate-50 dark:bg-slate-900/50 p-1 rounded-xl flex-grow sm:flex-grow-0">
        <button 
          v-for="tab in tabs"
          :key="tab.id"
          @click="emit('tab-change', tab.id)"
          :class="[
            'px-4 sm:px-5 py-2 text-sm font-semibold rounded-lg transition-colors',
            activeTab === tab.id
              ? 'bg-primary text-white shadow-sm'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Level Select -->
      <div class="relative group flex-grow sm:flex-grow-0">
        <select 
          :value="selectedLevel"
          @change="emit('level-change', $event.target.value)"
          class="w-full appearance-none pl-4 pr-10 py-2.5 bg-slate-50 dark:bg-slate-900/50 border-none rounded-xl text-sm font-semibold focus:ring-2 focus:ring-primary/20 transition-all"
        >
          <option v-for="level in levels" :key="level.value" :value="level.value">
            {{ level.label }}
          </option>
        </select>
        <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400 text-lg">
          expand_more
        </span>
      </div>
    </div>

    <!-- Search Input -->
    <div class="relative">
      <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xl">search</span>
      <input 
        :value="searchQuery"
        @input="emit('search', $event.target.value)"
        type="text"
        class="w-full pl-12 pr-4 py-3 bg-slate-50 dark:bg-slate-900/50 border-none rounded-xl text-sm placeholder:text-slate-400 focus:ring-2 focus:ring-primary/20 transition-all"
        placeholder="Search readings..."
      />
    </div>
  </div>
</template>
