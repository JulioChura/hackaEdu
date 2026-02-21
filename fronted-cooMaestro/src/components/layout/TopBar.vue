<template>
  <header class="h-16 md:h-20 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md sticky top-0 z-10 px-4 md:px-8 flex items-center justify-between border-b border-gray-200 dark:border-zinc-800">
    <!-- Mobile Menu Button -->
    <button 
      @click="$emit('toggle-sidebar')"
      class="lg:hidden w-10 h-10 flex items-center justify-center rounded-xl bg-gray-100 dark:bg-zinc-800 hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors mr-3"
      aria-label="Toggle menu"
    >
      <span class="material-symbols-outlined text-charcoal dark:text-gray-300">menu</span>
    </button>

    <!-- Search Bar -->
    <div class="flex-1 max-w-xl">
      <div class="relative group">
        <span class="material-symbols-outlined absolute left-3 md:left-4 top-1/2 -translate-y-1/2 text-medium-gray group-focus-within:text-primary transition-colors text-lg md:text-xl">search</span>
        <input 
          v-model="searchQuery"
          class="w-full bg-background-light dark:bg-zinc-800 border-none rounded-xl pl-10 md:pl-12 pr-3 md:pr-4 py-2 md:py-2.5 text-xs md:text-sm focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-medium-gray" 
          placeholder="Search courses..." 
          type="text"
          @input="handleSearch"
        />
      </div>
    </div>

    <div class="flex items-center gap-3 md:gap-6 ml-3 md:ml-8">
      <!-- Notifications -->
      <div class="relative">
        <button 
          @click="handleNotificationsClick"
          class="w-9 h-9 md:w-10 md:h-10 flex items-center justify-center rounded-xl bg-gray-100 dark:bg-zinc-800 hover:bg-gray-200 dark:hover:bg-zinc-700 transition-colors"
          aria-label="Notifications"
        >
          <span class="material-symbols-outlined text-charcoal dark:text-gray-300 text-lg md:text-xl">notifications</span>
        </button>
        <span 
          v-if="unreadNotificationsCount > 0"
          class="absolute -top-1 -right-1 w-4 h-4 md:w-5 md:h-5 bg-primary text-white text-[9px] md:text-[10px] font-bold flex items-center justify-center rounded-full border-2 border-white dark:border-zinc-900"
        >
          {{ unreadNotificationsCount > 9 ? '9+' : unreadNotificationsCount }}
        </span>
      </div>

      <div class="h-6 md:h-8 w-[1px] bg-gray-200 dark:bg-zinc-800 hidden sm:block"></div>

      <!-- User Profile Mini -->
      <div class="flex items-center gap-2 md:gap-3">
        <div class="text-right hidden md:block">
          <p class="text-xs font-bold leading-none">{{ userData.fullName }}</p>
          <p class="text-[10px] text-medium-gray mt-1">{{ userData.userLevelTitle }}</p>
        </div>
        <div 
          class="w-9 h-9 md:w-10 md:h-10 rounded-full bg-cover bg-center border-2 border-primary/10 cursor-pointer"
          :style="{ backgroundImage: `url(${userData.avatarUrl})` }"
          @click="handleOpenSettings"
        >
          <div 
            v-if="!userData.avatarUrl" 
            class="w-full h-full bg-gray-300 dark:bg-zinc-700 rounded-full flex items-center justify-center"
          >
            <span class="material-symbols-outlined text-white text-sm">person</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  userData: {
    type: Object,
    required: true
  },
  unreadNotificationsCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['toggle-sidebar', 'search', 'open-notifications', 'open-settings']);

const searchQuery = ref('');

const handleSearch = () => {
  emit('search', searchQuery.value);
};

const handleNotificationsClick = () => {
  emit('open-notifications');
};

const handleOpenSettings = () => {
  emit('open-settings');
};
</script>
