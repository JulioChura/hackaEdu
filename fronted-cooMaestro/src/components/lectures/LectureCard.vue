<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  lecture: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['play'])

const getLevelColor = (level) => {
  const colors = {
    'A1': 'bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400',
    'A2': 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400',
    'B1': 'bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400',
    'B2': 'bg-indigo-100 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400',
    'C1': 'bg-purple-100 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400',
    'C2': 'bg-violet-100 text-violet-600 dark:bg-violet-500/20 dark:text-violet-400'
  }
  return colors[level] || 'bg-slate-100 text-slate-600'
}

const getStatusColor = (status) => {
  const colors = {
    'completed': 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400',
    'in-progress': 'bg-orange-100 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400',
    'not-started': 'bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-400'
  }
  return colors[status] || 'bg-slate-100 text-slate-600'
}

const getProgressColor = (status, progress) => {
  if (status === 'completed') {
    if (progress >= 80) return 'bg-emerald-500'
    if (progress >= 50) return 'bg-amber-400'
    return 'bg-red-400'
  }
  if (status === 'in-progress') return 'bg-primary'
  return 'bg-slate-300'
}

const getButtonStyle = (status) => {
  if (status === 'completed') {
    return 'bg-emerald-500 text-white hover:bg-emerald-600'
  }
  return 'bg-indigo-50 dark:bg-indigo-900/30 text-primary hover:bg-primary hover:text-white'
}

const getButtonIcon = (status) => {
  return status === 'completed' ? 'check' : 'play_arrow'
}

const handlePlayLecture = () => {
  router.push({ name: 'LectureTake', params: { id: props.lecture.id } })
}
</script>

<template>
  <div class="group relative flex flex-col w-full bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700/50 hover:shadow-md transition-all duration-300 overflow-hidden">
    <!-- Thumbnail -->
    <div class="w-full h-48 sm:h-40 rounded-t-2xl overflow-hidden bg-slate-100 dark:bg-slate-700">
      <img 
        :src="lecture.thumbnail" 
        :alt="lecture.title"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
      />
    </div>

    <!-- Content -->
    <div class="flex flex-col flex-grow p-3 sm:p-4">
      <!-- Tags -->
      <div class="flex flex-wrap items-center gap-2 mb-2">
        <p class="text-[10px] font-bold tracking-wider text-primary uppercase">{{ lecture.category }}</p>
        <span 
          :class="[
            'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase',
            getStatusColor(lecture.status)
          ]"
        >
          {{ lecture.status === 'completed' ? 'Completed' : lecture.status === 'in-progress' ? 'In Progress' : 'Not Started' }}
        </span>
        <span 
          :class="[
            'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase',
            getLevelColor(lecture.level)
          ]"
        >
          {{ lecture.level }}
        </span>
      </div>

      <!-- Title -->
      <h3 class="text-sm sm:text-base font-bold font-display mb-3 line-clamp-2 flex-grow">
        {{ lecture.title }}
      </h3>

      <!-- Progress Bar -->
      <div class="flex items-center gap-3 mb-4">
        <div class="flex-grow h-2 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
          <div 
            :class="[
              'h-full rounded-full transition-all duration-700',
              getProgressColor(lecture.status, lecture.progress)
            ]"
            :style="{ width: `${lecture.progress}%` }"
          ></div>
        </div>
        <span class="text-xs font-semibold text-slate-400 tabular-nums min-w-[2.5rem] text-right">
          {{ lecture.progress }}%
          <span v-if="lecture.status === 'completed'" class="block text-[9px] uppercase tracking-wide">score</span>
        </span>
      </div>

      <!-- Play Button -->
      <button 
        @click="handlePlayLecture"
        :class="[
          'w-full px-3 py-2.5 rounded-lg font-bold text-sm transition-all shadow-sm',
          getButtonStyle(lecture.status)
        ]"
      >
        <span class="material-symbols-outlined inline-block mr-2 text-base align-middle">{{ getButtonIcon(lecture.status) }}</span>
        {{ lecture.status === 'completed' ? 'View Results' : 'Start Reading' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}
</style>
