<template>
  <aside class="w-64 bg-white dark:bg-zinc-900 border-r border-gray-200 dark:border-zinc-800 flex flex-col fixed h-full z-20">
    <!-- Logo Header -->
    <div class="p-6 flex items-center gap-3">
      <div class="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white">
        <span class="material-symbols-outlined text-2xl">school</span>
      </div>
      <div class="flex flex-col">
        <h1 class="text-lg font-bold leading-tight">HackaEdu</h1>
        <p class="text-xs text-medium-gray font-medium uppercase tracking-wider">
          {{ userRole }} Portal
        </p>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 px-4 mt-4 space-y-1 overflow-y-auto">
      <a 
        v-for="menuItem in menuItems" 
        :key="menuItem.routeName"
        :href="menuItem.routePath"
        @click.prevent="handleNavigate(menuItem.routeName)"
        class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all"
        :class="isActiveRoute(menuItem.routeName) 
          ? 'bg-primary/10 text-primary font-semibold' 
          : 'text-medium-gray hover:bg-gray-100 dark:hover:bg-zinc-800 hover:text-charcoal dark:hover:text-white'"
      >
        <span 
          class="material-symbols-outlined"
          :class="{ 'fill-icon': isActiveRoute(menuItem.routeName) }"
        >
          {{ menuItem.icon }}
        </span>
        <span>{{ menuItem.label }}</span>
      </a>
    </nav>

    <!-- Bottom Section -->
    <div class="p-4 mt-auto border-t border-gray-100 dark:border-zinc-800">
      <!-- Pro Plan Upgrade Card -->
      <div 
        v-if="!userIsPro"
        class="bg-primary/5 dark:bg-primary/10 p-4 rounded-xl mb-4"
      >
        <p class="text-xs font-bold text-primary mb-2">PRO PLAN</p>
        <p class="text-xs text-charcoal dark:text-gray-300 mb-3">
          Unlock advanced analytics and AI mentoring.
        </p>
        <button 
          @click="handleUpgradeToPro"
          class="w-full bg-primary text-white text-xs font-bold py-2 rounded-lg hover:bg-primary/90 transition-colors"
        >
          Upgrade Now
        </button>
      </div>

      <!-- User Profile -->
      <div class="flex items-center gap-3 px-2">
        <div 
          class="w-10 h-10 rounded-full bg-cover bg-center ring-2 ring-primary/20 shrink-0"
          :style="{ backgroundImage: `url(${userData.avatarUrl})` }"
          :alt="`${userData.fullName} avatar`"
        >
          <div 
            v-if="!userData.avatarUrl" 
            class="w-full h-full bg-gray-300 dark:bg-zinc-700 rounded-full flex items-center justify-center"
          >
            <span class="material-symbols-outlined text-white text-sm">person</span>
          </div>
        </div>

        <div class="flex-1 min-w-0">
          <p class="text-sm font-bold truncate">{{ userData.fullName }}</p>
          <p class="text-xs text-medium-gray truncate">{{ userData.userLevelTitle }}</p>
        </div>

        <button 
          @click="handleOpenSettings"
          class="shrink-0"
          aria-label="Settings"
        >
          <span class="material-symbols-outlined text-gray-400 text-lg hover:text-primary transition-colors">
            settings
          </span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
const props = defineProps({
  activeRoute: {
    type: String,
    default: 'dashboard'
  },
  userData: {
    type: Object,
    default: () => ({
      userId: null,
      fullName: 'User',
      userLevelTitle: 'Learner',
      avatarUrl: ''
    })
  },
  userRole: {
    type: String,
    default: 'Student',
    validator: (value) => ['Student', 'Teacher', 'Admin'].includes(value)
  },
  userIsPro: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['navigate', 'upgrade-to-pro', 'open-settings']);

const menuItems = [
  {
    routeName: 'dashboard',
    routePath: '/dashboard',
    label: 'Dashboard',
    icon: 'dashboard'
  },
  {
    routeName: 'my-courses',
    routePath: '/my-courses',
    label: 'My Courses',
    icon: 'book_5'
  },
  {
    routeName: 'progress',
    routePath: '/progress',
    label: 'Progress',
    icon: 'analytics'
  },
  {
    routeName: 'achievements',
    routePath: '/achievements',
    label: 'Achievements',
    icon: 'workspace_premium'
  },
  {
    routeName: 'ranking',
    routePath: '/ranking',
    label: 'Ranking',
    icon: 'leaderboard'
  }
];

const isActiveRoute = (routeName) => {
  return props.activeRoute === routeName;
};

const handleNavigate = (routeName) => {
  emit('navigate', routeName);
  // En el futuro: router.push({ name: routeName });
};

const handleUpgradeToPro = () => {
  emit('upgrade-to-pro');
};

const handleOpenSettings = () => {
  emit('open-settings');
};
</script>
