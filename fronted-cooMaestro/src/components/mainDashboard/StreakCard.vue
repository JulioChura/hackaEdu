<template>
  <section>
    <div class="bg-white dark:bg-zinc-900 p-4 md:p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4 md:mb-6">
        <div class="flex items-center gap-2 md:gap-3">
          <div class="w-8 h-8 md:w-10 md:h-10 rounded-full bg-orange-100 dark:bg-orange-500/20 flex items-center justify-center text-orange-500">
            <span class="material-symbols-outlined fill-icon text-lg md:text-xl">local_fire_department</span>
          </div>
          <h3 class="font-bold text-sm md:text-base">Learning Streak</h3>
        </div>
        <div class="bg-orange-100 dark:bg-orange-500/20 text-orange-600 dark:text-orange-400 px-2 md:px-3 py-1 rounded-full text-xs md:text-sm font-bold whitespace-nowrap">
          {{ currentStreak }} Days 🔥
        </div>
      </div>

      <!-- Week Calendar -->
      <div class="flex justify-between items-center px-1 md:px-2">
        <div 
          v-for="day in weekDays" 
          :key="day.name"
          class="flex flex-col items-center gap-1 md:gap-2"
          :class="{ 'opacity-40': !day.isCompleted }"
        >
          <!-- Day Circle -->
          <div 
            v-if="day.isCompleted"
            class="w-7 h-7 md:w-10 md:h-10 rounded-full bg-primary text-white flex items-center justify-center"
          >
            <span class="material-symbols-outlined text-xs md:text-sm">check</span>
          </div>
          <div 
            v-else
            class="w-7 h-7 md:w-10 md:h-10 rounded-full border-2 border-dashed border-gray-400 flex items-center justify-center"
          ></div>
          
          <!-- Day Label -->
          <span class="text-[9px] md:text-[10px] text-medium-gray font-bold uppercase">
            {{ day.label }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentStreak: {
    type: Number,
    default: 0
  },
  completedDaysThisWeek: {
    type: Array,
    default: () => [true, true, true, true, true, false, false] // Lun-Dom
  }
});

const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const weekDays = computed(() => {
  return dayLabels.map((label, index) => ({
    name: label.toLowerCase(),
    label: label,
    isCompleted: props.completedDaysThisWeek[index] || false
  }));
});
</script>
