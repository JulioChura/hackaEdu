<template>
    <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-lg">
        <div class="flex flex-col gap-2">
            <h1 class="text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em] text-[#111318]">{{ title }}
            </h1>
            <div class="flex items-center gap-3">
                <span class="text-[#616f89] dark:text-gray-400 text-sm font-medium">Código de acceso:</span>
                <div
                    class="flex items-center gap-2 bg-gray-50 px-3 py-1 rounded-full group cursor-pointer hover:border-blue-800 transition-colors">
                    <span class="text-[#111318] text-sm font-bold tracking-wide">{{ accessCode }}</span>
                    <span
                        class="material-symbols-outlined text-[16px] text-[#616f89] group-hover:text-blue-800">content_copy</span>
                </div>
            </div>
        </div>
    </div>

    <div>
        <slot name="actions" />
    </div>
</template>

<script setup>
defineProps({
    title: { type: String, default: '' },
    accessCode: { type: String, default: '' }
})
</script>

<style scoped>
/* small scoped adjustments can go here */
</style>
