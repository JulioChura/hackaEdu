<script setup>
const props = defineProps({
  users: {
    type: Array,
    default: () => []
  },
  currentUserId: {
    type: Number,
    default: null
  }
})

const getLevelColor = (level) => {
  const colors = {
    'A1': 'bg-green-50 text-green-600',
    'A2': 'bg-lime-50 text-lime-600',
    'B1': 'bg-blue-50 text-blue-600',
    'B2': 'bg-indigo-50 text-indigo-600',
    'C1': 'bg-purple-50 text-purple-600',
    'C2': 'bg-violet-50 text-violet-600'
  }
  return colors[level] || 'bg-gray-50 text-gray-600'
}

const isCurrentUser = (userId) => {
  return userId === props.currentUserId
}
</script>

<template>
  <div class="bg-white dark:bg-white/5 rounded-2xl overflow-hidden border border-slate-200 dark:border-white/10 shadow-sm">
    <!-- Desktop Table -->
    <div class="hidden md:block overflow-x-auto">
      <table class="w-full text-left">
        <thead class="bg-slate-50 dark:bg-white/5 border-b border-slate-200 dark:border-white/10">
          <tr>
            <th class="px-4 lg:px-6 py-3 lg:py-4 text-xs font-black uppercase tracking-widest text-slate-400">Rank</th>
            <th class="px-4 lg:px-6 py-3 lg:py-4 text-xs font-black uppercase tracking-widest text-slate-400">Student</th>
            <th class="px-4 lg:px-6 py-3 lg:py-4 text-xs font-black uppercase tracking-widest text-slate-400">CEFR Level</th>
            <th class="px-4 lg:px-6 py-3 lg:py-4 text-xs font-black uppercase tracking-widest text-slate-400 text-right">Points</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-white/5">
          <tr 
            v-for="user in users" 
            :key="user.id"
            :class="[
              'transition-colors group',
              isCurrentUser(user.id) 
                ? 'bg-primary/5 dark:bg-primary/20 border-l-4 border-primary' 
                : 'hover:bg-slate-50 dark:hover:bg-white/5'
            ]"
          >
            <td class="px-4 lg:px-6 py-3 lg:py-4 font-bold" :class="isCurrentUser(user.id) ? 'text-primary' : 'text-slate-500'">
              {{ user.rank }}
            </td>
            <td class="px-4 lg:px-6 py-3 lg:py-4">
              <div class="flex items-center gap-3">
                <div 
                  :class="[
                    'h-10 w-10 rounded-full overflow-hidden',
                    isCurrentUser(user.id) ? 'border-2 border-primary bg-primary/20' : 'bg-slate-100'
                  ]"
                >
                  <img 
                    :src="user.avatar" 
                    :alt="`${user.name} avatar`"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div v-if="isCurrentUser(user.id)">
                  <span class="font-black text-primary">You</span>
                  <span class="text-[10px] block text-primary/60 font-bold uppercase tracking-tighter">Current Progress</span>
                </div>
                <span v-else class="font-bold">{{ user.name }}</span>
              </div>
            </td>
            <td class="px-4 lg:px-6 py-3 lg:py-4">
              <span 
                :class="[
                  'px-3 py-1 rounded-lg text-xs font-black',
                  isCurrentUser(user.id) ? 'bg-primary text-white' : getLevelColor(user.level)
                ]"
              >
                {{ user.level }}
              </span>
            </td>
            <td class="px-4 lg:px-6 py-3 lg:py-4 text-right font-black text-primary">
              {{ user.points.toLocaleString() }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile Cards -->
    <div class="md:hidden divide-y divide-slate-100 dark:divide-white/5">
      <div 
        v-for="user in users" 
        :key="user.id"
        :class="[
          'p-4 transition-colors',
          isCurrentUser(user.id) 
            ? 'bg-primary/5 dark:bg-primary/20 border-l-4 border-primary' 
            : 'hover:bg-slate-50 dark:hover:bg-white/5'
        ]"
      >
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3 flex-1">
            <span 
              class="text-lg font-black min-w-[2rem] text-center"
              :class="isCurrentUser(user.id) ? 'text-primary' : 'text-slate-500'"
            >
              {{ user.rank }}
            </span>
            <div 
              :class="[
                'h-12 w-12 rounded-full overflow-hidden shrink-0',
                isCurrentUser(user.id) ? 'border-2 border-primary bg-primary/20' : 'bg-slate-100'
              ]"
            >
              <img 
                :src="user.avatar" 
                :alt="`${user.name} avatar`"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <div v-if="isCurrentUser(user.id)">
                <span class="font-black text-primary block truncate">You</span>
                <span class="text-[10px] text-primary/60 font-bold uppercase">Current Progress</span>
              </div>
              <span v-else class="font-bold block truncate">{{ user.name }}</span>
              <div class="flex items-center gap-2 mt-1">
                <span 
                  :class="[
                    'px-2 py-0.5 rounded text-[10px] font-black',
                    isCurrentUser(user.id) ? 'bg-primary text-white' : getLevelColor(user.level)
                  ]"
                >
                  {{ user.level }}
                </span>
              </div>
            </div>
          </div>
          <div class="text-right">
            <p class="font-black text-primary text-lg">{{ user.points.toLocaleString() }}</p>
            <p class="text-[9px] text-slate-400 font-bold uppercase">pts</p>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4 text-center border-t border-slate-100 dark:border-white/5 bg-slate-50/50 dark:bg-white/5">
      <button class="text-xs sm:text-sm font-bold text-primary hover:underline">
        View Full Leaderboard (500+ students)
      </button>
    </div>
  </div>
</template>
