<template>
  <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors group">
    <div v-if="avatar" class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" :style="{ backgroundImage: `url(${avatar})` }"></div>
    <div v-else class="flex items-center justify-center rounded-full size-10 bg-purple-100 text-purple-600 font-bold text-sm">{{ initials }}</div>
    <div class="flex-1 min-w-0">
      <p class="text-sm font-bold text-[#111318] dark:text-white truncate">{{ name }}</p>
      <p class="text-xs text-[#616f89] dark:text-gray-400">Nivel: {{ level }}</p>
    </div>
    <div class="flex flex-col items-end">
      <span class="text-xs font-bold" :class="percentClass">{{ percent }}%</span>
      <span class="text-[10px] text-[#616f89]">Progreso</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  name: { type: String, required: true },
  level: { type: String, default: 'Intermedio' },
  percent: { type: [Number, String], default: 0 },
  avatar: { type: String, default: '' },
})

const initials = props.name.split(' ').map(s => s[0]).slice(0,2).join('')
const percentClass = props.percent >= 90 ? 'text-green-600' : props.percent >= 60 ? 'text-blue-800' : 'text-orange-500'
</script>

<style scoped></style>
