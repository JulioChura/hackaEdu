<template>
  <section class="border-y border-slate-100 bg-background-subtle py-10 sm:py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6 sm:gap-8">
        <!-- Title -->
        <div class="text-center md:text-left md:w-1/4">
          <h4 class="text-charcoal font-bold text-base sm:text-lg">Supported Proficiency Levels</h4>
          <p class="text-slate-text text-xs sm:text-sm mt-1">From absolute beginner to mastery.</p>
        </div>
        
        <!-- CEFR Badges Carousel -->
        <div class="flex-1 w-full relative">
          <!-- Previous Button -->
          <button
            v-show="showControls && canScrollLeft"
            @click="scrollLeft"
            class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-primary border-2 border-slate-200 hover:border-primary rounded-full w-8 h-8 sm:w-10 sm:h-10 flex items-center justify-center shadow-md transition-all group"
            aria-label="Previous levels"
          >
            <span class="material-symbols-outlined text-slate-600 group-hover:text-white text-lg sm:text-xl">
              chevron_left
            </span>
          </button>
          
          <!-- Badges Container -->
          <div 
            ref="scrollContainer"
            class="overflow-x-auto pb-4 md:pb-0 scroll-smooth"
            style="scrollbar-width: none; -ms-overflow-style: none;"
            @scroll="checkScroll"
          >
            <div class="flex items-center justify-center md:justify-end gap-2 sm:gap-3 min-w-[500px] sm:min-w-[600px] px-4">
              <BadgeCefrHome level="A1" label="Beginner" />
              <div class="h-[1px] w-6 sm:w-8 bg-slate-200"></div>
              
              <BadgeCefrHome level="A2" label="Elementary" />
              <div class="h-[1px] w-6 sm:w-8 bg-slate-200"></div>
              
              <BadgeCefrHome level="B1" label="Interm." />
              <div class="h-[1px] w-6 sm:w-8 bg-slate-200"></div>
              
              <BadgeCefrHome level="B2" label="Upper Int." :is-active="true" />
              <div class="h-[1px] w-6 sm:w-8 bg-slate-200"></div>
              
              <BadgeCefrHome level="C1" label="Advanced" />
              <div class="h-[1px] w-6 sm:w-8 bg-slate-200"></div>
              
              <BadgeCefrHome level="C2" label="Mastery" />
            </div>
          </div>
          
          <!-- Next Button -->
          <button
            v-show="showControls && canScrollRight"
            @click="scrollRight"
            class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-primary border-2 border-slate-200 hover:border-primary rounded-full w-8 h-8 sm:w-10 sm:h-10 flex items-center justify-center shadow-md transition-all group"
            aria-label="Next levels"
          >
            <span class="material-symbols-outlined text-slate-600 group-hover:text-white text-lg sm:text-xl">
              chevron_right
            </span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import BadgeCefrHome from './BadgeCefrHome.vue'

const scrollContainer = ref(null)
const showControls = ref(false)
const canScrollLeft = ref(false)
const canScrollRight = ref(false)

const checkScroll = () => {
  if (!scrollContainer.value) return
  
  const { scrollLeft, scrollWidth, clientWidth } = scrollContainer.value
  
  canScrollLeft.value = scrollLeft > 0
  canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 5
}

const checkOverflow = () => {
  if (!scrollContainer.value) return
  
  const { scrollWidth, clientWidth } = scrollContainer.value
  showControls.value = scrollWidth > clientWidth
  checkScroll()
}

const scrollLeft = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -200, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 200, behavior: 'smooth' })
  }
}

onMounted(() => {
  checkOverflow()
  window.addEventListener('resize', checkOverflow)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkOverflow)
})
</script>

<style scoped>
/* Ocultar scrollbar */
div::-webkit-scrollbar {
  display: none;
}
</style>
