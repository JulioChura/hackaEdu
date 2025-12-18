<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import TeacherSideBar from '../../shared/components/TeacherSideBar.vue'

const sidebarOpen = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => { sidebarOpen.value = false })
</script>

<template>
    <div class="min-h-screen flex bg-background-light">
                <!-- Sidebar (fixed on desktop, overlay on mobile) -->
                <TeacherSideBar :open="sidebarOpen" @close="sidebarOpen = false" />

        <main class="flex-1 overflow-auto md:pl-72">
            <!-- Mobile topbar with menu -->
            <div class="md:hidden flex items-center justify-between p-3 bg-surface border-b">
                <button @click="sidebarOpen = true" class="p-2 rounded-md">
                    <span class="material-symbols-outlined">menu</span>
                </button>
                <div class="text-sm font-bold">Portal Docente</div>
                <div class="w-8" />
            </div>

            <router-view />
        </main>
    </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .18s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>