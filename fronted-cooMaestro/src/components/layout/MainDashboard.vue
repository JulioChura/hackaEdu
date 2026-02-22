<template>
  <div class="flex min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Sidebar -->
    <Sidebar
      :activeRoute="activeRoute"
      :userData="userData"
      :userRole="userRole"
      :userIsPro="userIsPro"
      :isMobileMenuOpen="isMobileMenuOpen"
      @navigate="handleNavigate"
      @upgrade-to-pro="handleUpgradeToPro"
      @open-settings="handleOpenSettings"
      @close-sidebar="closeMobileSidebar"
    />

    <!-- Main Content Area -->
    <main class="flex-1 lg:ml-64 min-h-screen w-full lg:w-auto">
      <!-- TopBar -->
      <TopBar
        :userData="userData"
        :unreadNotificationsCount="unreadNotificationsCount"
        @toggle-sidebar="toggleMobileSidebar"
        @search="handleSearch"
        @open-notifications="handleOpenNotifications"
        @open-settings="handleOpenSettings"
        @logout="handleLogout"
      />

      <!-- Page Content Slot -->
      <div class="p-4 sm:p-6 md:p-8">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Sidebar from './Sidebar.vue';
import TopBar from './TopBar.vue';

defineProps({
  activeRoute: {
    type: String,
    default: 'dashboard'
  },
  userData: {
    type: Object,
    required: true
  },
  userRole: {
    type: String,
    default: 'Student'
  },
  userIsPro: {
    type: Boolean,
    default: false
  },
  unreadNotificationsCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits([
  'navigate',
  'upgrade-to-pro',
  'open-settings',
  'search',
  'open-notifications',
  'logout'
]);

const isMobileMenuOpen = ref(false);

const toggleMobileSidebar = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileSidebar = () => {
  isMobileMenuOpen.value = false;
};

const handleNavigate = (routeName) => {
  emit('navigate', routeName);
};

const handleUpgradeToPro = () => {
  emit('upgrade-to-pro');
};

const handleOpenSettings = () => {
  emit('open-settings');
};

const handleSearch = (query) => {
  emit('search', query);
};

const handleOpenNotifications = () => {
  emit('open-notifications');
};

const handleLogout = () => {
  emit('logout');
};
</script>
