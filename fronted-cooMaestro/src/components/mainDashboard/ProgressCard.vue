<template>
  <section>
    <h2 class="text-xl md:text-2xl font-bold mb-3 md:mb-4">{{ greetingMessage }} 👋</h2>
    <div class="bg-white dark:bg-zinc-900 p-4 md:p-6 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800">
      <div class="flex flex-col md:flex-row gap-4 md:gap-6 items-center">
        <!-- Level Badge -->
        <div class="w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-primary flex flex-col items-center justify-center text-white shrink-0">
          <span class="text-2xl md:text-3xl font-bold">{{ currentLevel }}</span>
          <span class="text-[9px] md:text-[10px] font-medium tracking-widest uppercase">Level</span>
        </div>

        <!-- Progress Info -->
        <div class="flex-1 w-full">
          <div class="flex justify-between items-end mb-2">
            <div class="min-w-0 flex-1">
              <h3 class="text-base md:text-lg font-bold truncate">{{ levelTitle }}</h3>
              <p class="text-xs md:text-sm text-medium-gray truncate">
                {{ currentPoints }}/{{ nextLevelPoints }} pts to {{ nextLevel }}
              </p>
            </div>
            <span class="text-xs md:text-sm font-bold text-primary ml-2 shrink-0">{{ progressPercentage }}%</span>
          </div>

          <!-- Progress Bar -->
          <div class="h-2 md:h-3 bg-gray-100 dark:bg-zinc-800 rounded-full overflow-hidden">
            <div 
              class="h-full bg-primary rounded-full transition-all duration-500" 
              :style="{ width: progressPercentage + '%' }"
            ></div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-3 md:mt-4 flex flex-col sm:flex-row gap-2 md:gap-4">
            <button 
              @click="handleContinuePath"
              class="flex-1 bg-primary text-white text-xs md:text-sm font-semibold py-2 md:py-2.5 rounded-lg hover:bg-primary/90 transition-colors"
            >
              Continue Path
            </button>
            <button 
              @click="handleViewRoadmap"
              class="flex-1 sm:flex-none px-4 border border-gray-200 dark:border-zinc-700 text-xs md:text-sm font-semibold py-2 md:py-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-zinc-800 transition-colors"
            >
              View Roadmap
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  studentName: {
    type: String,
    default: 'Student'
  },
  currentLevel: {
    type: String,
    default: 'A1'
  },
  levelTitle: {
    type: String,
    default: 'Beginner'
  },
  currentPoints: {
    type: Number,
    default: 0
  },
  nextLevelPoints: {
    type: Number,
    default: 100
  },
  nextLevel: {
    type: String,
    default: 'A2 Elementary'
  }
});

const emit = defineEmits(['continue-path', 'view-roadmap']);

const greetingMessage = computed(() => {
  const hour = new Date().getHours();
  let greeting = 'Good evening';
  
  if (hour < 12) {
    greeting = 'Good morning';
  } else if (hour < 18) {
    greeting = 'Good afternoon';
  }
  
  return `${greeting}, ${props.studentName}!`;
});

const progressPercentage = computed(() => {
  if (props.nextLevelPoints === 0) return 0;
  return Math.round((props.currentPoints / props.nextLevelPoints) * 100);
});

const handleContinuePath = () => {
  emit('continue-path');
};

const handleViewRoadmap = () => {
  emit('view-roadmap');
};
</script>
