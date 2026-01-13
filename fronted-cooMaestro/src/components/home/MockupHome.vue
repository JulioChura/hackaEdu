<template>
  <div class="relative bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden transform transition hover:scale-[1.01] duration-500 group">
    <!-- Browser Header -->
    <div class="h-8 sm:h-10 bg-slate-50 border-b border-slate-200 flex items-center px-3 sm:px-4 gap-2">
      <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-400"></div>
      <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-yellow-400"></div>
      <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-green-400"></div>
      <div class="ml-2 sm:ml-4 flex-1 h-5 sm:h-6 bg-white border border-slate-200 rounded-md flex items-center px-2 sm:px-3 text-[9px] sm:text-[10px] text-slate-400 font-mono">
        hackaedu.com/learn/session-b2
      </div>
    </div>

    <!-- Content Area -->
    <div class="p-4 sm:p-6 md:p-8 grid md:grid-cols-3 gap-4 sm:gap-6 bg-white min-h-[300px] sm:min-h-[400px]">
      <!-- Sidebar -->
      <div class="md:col-span-1 border-r border-slate-100 pr-3 sm:pr-4 flex flex-col gap-3 sm:gap-4">
        <div class="h-2 w-16 sm:w-20 bg-slate-200 rounded animate-pulse"></div>
        <div class="space-y-2 sm:space-y-3 mt-3 sm:mt-4">
          <div class="h-8 sm:h-10 w-full bg-primary/10 rounded-lg border-l-4 border-primary p-2">
            <div class="h-1.5 sm:h-2 w-12 sm:w-16 bg-primary/40 rounded mb-1"></div>
            <div class="h-1 sm:h-1.5 w-8 sm:w-10 bg-primary/20 rounded"></div>
          </div>
          <div class="h-8 sm:h-10 w-full bg-slate-50 rounded-lg p-2"></div>
          <div class="h-8 sm:h-10 w-full bg-slate-50 rounded-lg p-2"></div>
        </div>
        <div class="mt-auto bg-slate-900 text-white p-2 sm:p-3 rounded-lg text-xs">
          <p class="font-bold mb-1">Daily Streak</p>
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-orange-400 text-sm">local_fire_department</span>
            <span>12 Days</span>
          </div>
        </div>
      </div>

      <!-- Main Text -->
      <div class="md:col-span-2">
        <h3 class="text-base sm:text-xl font-bold mb-3 sm:mb-4 text-charcoal">The Future of Urban Planning</h3>
        <div class="space-y-2 sm:space-y-3 text-slate-600 leading-relaxed text-xs sm:text-sm">
          <p>
            Urban planning is a 
            <span class="bg-yellow-100 text-charcoal px-1 rounded cursor-pointer hover:bg-yellow-200 transition-colors border-b-2 border-yellow-300">
              technical
            </span> 
            and political process concerned with the use of land and design of the urban environment.
          </p>
          <p>
            It involves the preparation of plans for and the regulation and management of towns, cities, and metropolitan regions.
          </p>
          <div class="flex gap-2 mt-3 sm:mt-4">
            <span class="px-2 py-1 bg-slate-100 rounded text-xs text-slate-500 font-medium">#Architecture</span>
            <span class="px-2 py-1 bg-slate-100 rounded text-xs text-slate-500 font-medium">#Society</span>
          </div>
        </div>

        <!-- Floating Tooltip -->
        <div class="hidden lg:block absolute top-[40%] right-[10%] bg-charcoal text-white p-3 rounded-lg shadow-xl text-xs w-48 z-10 transform translate-y-4 opacity-0 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300">
          <div class="font-bold mb-1 flex justify-between items-center">
            technical <span class="text-[10px] text-slate-400">adj.</span>
          </div>
          <p class="text-slate-300 mb-2">Relating to a particular subject, art, or craft, or its techniques.</p>
          <button class="w-full py-1 bg-primary text-white font-bold rounded text-[10px]">Add to Flashcards</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Mockup del dashboard
</script>
