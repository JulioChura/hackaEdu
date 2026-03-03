<script setup>
defineProps({
  level: {
    type: [Number, String],
    default: 'B1'
  },
  unlockedCount: {
    type: Number,
    default: 0
  },
  totalCount: {
    type: Number,
    default: 0
  }
})
</script>

<template>
  <div class="mb-6 sm:mb-8">
    <div class="space-y-2 sm:space-y-3">
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight">My Achievements</h1>
      <div class="flex flex-wrap items-center gap-2 sm:gap-3">
        <span class="px-2.5 sm:px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full uppercase">
          Level {{ level }}
        </span>
        <p class="text-gray-500 dark:text-gray-400 text-xs sm:text-sm font-medium">
          {{ unlockedCount }} of {{ totalCount }} milestones unlocked
        </p>
      </div>
    </div>
  </div>
</template>
