<template>
  <div class="bg-white dark:bg-zinc-900 p-3 md:p-4 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800 flex items-center gap-3 md:gap-4 group">
    <!-- Course Thumbnail -->
    <div 
      class="w-16 h-16 md:w-20 md:h-20 rounded-lg bg-cover bg-center shrink-0"
      :style="{ backgroundImage: `url(${courseThumbnail})` }"
      :alt="courseTitle"
    >
      <!-- Fallback if no image -->
      <div 
        v-if="!courseThumbnail" 
        class="w-full h-full bg-gradient-to-br from-primary/20 to-primary/40 rounded-lg flex items-center justify-center"
      >
        <span class="material-symbols-outlined text-primary text-2xl md:text-3xl">auto_stories</span>
      </div>
    </div>

    <!-- Course Info -->
    <div class="flex-1 min-w-0">
      <p class="text-[9px] md:text-[10px] font-bold text-primary uppercase tracking-wider mb-1">
        {{ courseCategory }}
      </p>
      <h4 class="font-bold text-sm md:text-base mb-1.5 md:mb-2 truncate">
        {{ courseTitle }}
      </h4>
      
      <!-- Progress Bar -->
      <div class="flex items-center gap-2 md:gap-3">
        <div class="flex-1 h-1.5 bg-gray-100 dark:bg-zinc-800 rounded-full overflow-hidden">
          <div 
            :class="['h-full rounded-full transition-all duration-300', getBarColor()]"
            :style="{ width: courseProgress + '%' }"
          ></div>
        </div>
        <span class="text-[10px] md:text-xs text-medium-gray font-bold">
          {{ courseProgress }}%
          <span v-if="courseStatus === 'completed'" class="block text-[8px] uppercase tracking-wide">score</span>
        </span>
      </div>
    </div>

    <!-- Play Button -->
    <button 
      @click="handlePlayCourse"
      class="w-9 h-9 md:w-10 md:h-10 bg-primary/10 group-hover:bg-primary text-primary group-hover:text-white rounded-xl flex items-center justify-center transition-all shrink-0"
      :aria-label="`Continue ${courseTitle}`"
    >
      <span class="material-symbols-outlined fill-icon text-xl md:text-2xl">play_arrow</span>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  courseId: {
    type: [String, Number],
    required: true
  },
  courseTitle: {
    type: String,
    required: true,
    default: 'Untitled Course'
  },
  courseCategory: {
    type: String,
    default: 'General'
  },
  courseThumbnail: {
    type: String,
    default: ''
  },
  courseProgress: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  courseStatus: {
    type: String,
    default: 'not-started'
  }
});

const getBarColor = () => {
  if (props.courseStatus === 'completed') {
    if (props.courseProgress >= 80) return 'bg-emerald-500'
    if (props.courseProgress >= 50) return 'bg-amber-400'
    return 'bg-red-400'
  }
  return 'bg-primary'
}

const emit = defineEmits(['play-course']);

const handlePlayCourse = () => {
  emit('play-course', {
    courseId: props.courseId,
    courseTitle: props.courseTitle
  });
};
</script>
