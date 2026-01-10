<template>
  <div class="bg-gradient-to-br from-white to-gray-50 rounded-xl p-5 shadow-lg hover:shadow-2xl transition-shadow">
    <div class="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center mb-4">
        <div class="flex items-start gap-3">
        <div class="p-3 rounded-lg text-blue-800" :class="iconBg">
          <span class="material-symbols-outlined">{{ icon }}</span>
        </div>
        <div>
          <h4 class="font-bold text-[#111318] dark:text-white text-lg">{{ title }}</h4>
          <p class="text-sm text-[#616f89] dark:text-gray-400">{{ subtitle }}</p>
        </div>
      </div>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="statusBg">{{ status }}</span>
    </div>

    <div class="flex items-center justify-between gap-4 mt-2">
      <div class="flex flex-col w-full max-w-[200px] gap-1">
        <div class="flex justify-between text-xs text-[#616f89] dark:text-gray-400">
          <span>Completado</span>
          <span>{{ completed }}/{{ total }}</span>
        </div>
        <div class="w-full bg-gray-50 rounded-full h-2">
          <div class="h-2 rounded-full" :class="progressBg" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
      <button class="text-sm font-bold text-blue-800 hover:underline">Ver Detalles</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  subtitle: String,
  icon: { type: String, default: 'menu_book' },
  status: { type: String, default: 'En Progreso' },
  statusBg: { type: String, default: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' },
  iconBg: { type: String, default: 'bg-blue-50 dark:bg-blue-900/30' },
  completed: { type: [Number, String], default: 0 },
  total: { type: [Number, String], default: 0 },
  progress: { type: Number, default: 0 },
})

const progressBg = props.progress >= 75 ? 'bg-blue-800' : 'bg-orange-500'
</script>

<style scoped></style>
