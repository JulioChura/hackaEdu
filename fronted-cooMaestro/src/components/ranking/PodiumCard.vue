<script setup>
const props = defineProps({
  rank: {
    type: Number,
    required: true
  },
  user: {
    type: Object,
    required: true
  }
})

const getBorderClass = () => {
  if (props.rank === 1) return 'gold-border'
  if (props.rank === 2) return 'silver-border'
  if (props.rank === 3) return 'bronze-border'
  return ''
}

const getMedalColor = () => {
  if (props.rank === 1) return '#FFD700'
  if (props.rank === 2) return '#C0C0C0'
  if (props.rank === 3) return '#CD7F32'
  return ''
}

const getAvatarSize = () => {
  return props.rank === 1 ? 'size-28' : 'size-20'
}

const getCardPadding = () => {
  return props.rank === 1 ? 'p-6 sm:p-8' : 'p-4 sm:p-6'
}

const getOrder = () => {
  if (props.rank === 1) return 'order-1 md:order-2'
  if (props.rank === 2) return 'order-2 md:order-1'
  return 'order-3'
}

const getLevelColor = (level) => {
  const colors = {
    'A1': 'bg-green-100 text-green-700',
    'A2': 'bg-lime-100 text-lime-700',
    'B1': 'bg-blue-100 text-blue-700',
    'B2': 'bg-indigo-100 text-indigo-700',
    'C1': 'bg-purple-100 text-purple-700',
    'C2': 'bg-violet-100 text-violet-700'
  }
  return colors[level] || 'bg-gray-100 text-gray-700'
}
</script>

<template>
  <div 
    :class="[
      'bg-white dark:bg-white/5 rounded-2xl text-center podium-shadow flex flex-col items-center',
      getBorderClass(),
      getCardPadding(),
      getOrder(),
      rank === 1 ? 'scale-100 md:scale-105 relative z-10 border-x border-b border-primary/5' : ''
    ]"
  >
    <!-- Crown for first place -->
    <span 
      v-if="rank === 1" 
      class="material-symbols-outlined text-[#FFD700] text-3xl sm:text-4xl mb-2 fill-icon"
    >
      workspace_premium
    </span>

    <!-- Avatar -->
    <div class="relative mb-3 sm:mb-4">
      <div 
        :class="[
          'rounded-full overflow-hidden p-1',
          getAvatarSize(),
          `border-4`
        ]"
        :style="{ borderColor: getMedalColor() }"
      >
        <img 
          :src="user.avatar" 
          :alt="`${user.name} avatar`"
          class="rounded-full w-full h-full object-cover bg-slate-100"
        />
      </div>
      <div 
        :class="[
          'absolute -bottom-2 left-1/2 -translate-x-1/2 text-white rounded-full font-black',
          rank === 1 ? 'px-4 py-1 text-sm ring-4 ring-white dark:ring-background-dark bg-[#FFD700] text-black' : 'px-3 py-0.5 text-xs'
        ]"
        :style="{ backgroundColor: rank === 1 ? '#FFD700' : getMedalColor() }"
      >
        #{{ rank }}
      </div>
    </div>

    <!-- Name -->
    <h3 :class="rank === 1 ? 'font-black text-lg sm:text-xl mb-1' : 'font-bold text-base sm:text-lg mb-1'">
      {{ user.name }}
    </h3>

    <!-- Level Badge -->
    <div class="flex items-center gap-2 mb-3 sm:mb-4">
      <span 
        :class="[
          'px-2 sm:px-3 py-0.5 sm:py-1 rounded font-black uppercase tracking-wider',
          getLevelColor(user.level),
          rank === 1 ? 'text-xs' : 'text-[10px] sm:text-xs'
        ]"
      >
        {{ user.level }} Level
      </span>
    </div>

    <!-- Points -->
    <p :class="rank === 1 ? 'text-primary font-black text-2xl sm:text-3xl' : 'text-primary font-extrabold text-xl sm:text-2xl'">
      {{ user.points.toLocaleString() }}
    </p>
    <p class="text-[10px] uppercase font-bold text-slate-400 tracking-widest">
      {{ rank === 1 ? 'Master Points' : 'Total Points' }}
    </p>
  </div>
</template>

<style scoped>
.podium-shadow {
  box-shadow: 0 20px 25px -5px rgba(79, 65, 230, 0.1), 0 10px 10px -5px rgba(79, 65, 230, 0.04);
}

.gold-border { 
  border-top: 4px solid #FFD700; 
}

.silver-border { 
  border-top: 4px solid #C0C0C0; 
}

.bronze-border { 
  border-top: 4px solid #CD7F32; 
}

.fill-icon {
  font-variation-settings: 'FILL' 1;
}
</style>
