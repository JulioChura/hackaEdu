<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth.store'

const authStore = useAuthStore()

// Restore session on every hard-reload or tab open.
// The axios interceptor transparently refreshes the access token if it
// has expired, so the user never gets kicked out unexpectedly.
onMounted(() => {
  authStore.initSession()
})
</script>

<template>
  <router-view />
</template>

<style scoped>
/* App-level styles are provided by Tailwind */
</style>
