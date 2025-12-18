<template>
  <article class="group flex flex-col bg-surface rounded-2xl border border-[#e5e7eb] overflow-hidden hover:shadow-xl hover:shadow-blue-900/5 hover:border-primary/30 transition-all duration-300">
    <div class="h-36 w-full relative overflow-hidden bg-slate-100">
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10"></div>
      <div class="absolute top-4 left-4 z-20">
        <span class="inline-flex items-center rounded-md bg-white/90 px-2 py-1 text-xs font-bold text-primary ring-1 ring-inset ring-blue-700/10 backdrop-blur-sm">{{ code }}</span>
      </div>
      <div class="bg-center bg-cover w-full h-full transform group-hover:scale-105 transition-transform duration-700" :style="bgStyle"></div>
    </div>

    <div class="flex flex-col p-5 gap-4 flex-1">
      <div>
        <div class="flex justify-between items-start mb-1">
          <h3 class="text-lg font-bold text-[#111318] group-hover:text-primary transition-colors">{{ title }}</h3>
          <span v-if="isActive" class="flex size-2 rounded-full bg-green-500 mt-2" title="Clase Activa"></span>
        </div>
        <p class="text-sm text-[#616f89]">{{ group }} • {{ semester }}</p>
      </div>

      <div class="py-3 border-y border-[#f0f2f4] border-dashed">
        <div class="flex items-center gap-2">
          <div class="p-1.5 bg-background-light rounded-full text-[#616f89]">
            <span class="material-symbols-outlined text-[18px]">group</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs text-[#616f89] font-medium leading-none">Total</span>
            <span class="text-sm font-bold text-[#111318] leading-tight">{{ students }} Estudiantes</span>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4 bg-[#f9fafb] border-t border-[#f0f2f4] flex justify-between items-center group-hover:bg-blue-50/30 transition-colors">
      <div class="flex -space-x-2 overflow-hidden">
        <template v-for="(a,i) in avatars" :key="i">
          <img v-if="a" :src="a" alt="avatar" class="inline-block size-6 rounded-full ring-2 ring-white"/>
        </template>
      </div>
      <button @click="$emit('view', id)" class="text-sm font-bold text-primary hover:text-primary-dark flex items-center gap-1 transition-colors">
        Ver Clase <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
      </button>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  id: { type: [String, Number], default: null },
  code: { type: String, default: 'MAT-000' },
  title: { type: String, default: 'Curso' },
  group: { type: String, default: '' },
  semester: { type: String, default: '' },
  students: { type: Number, default: 0 },
  image: { type: String, default: '' },
  isActive: { type: Boolean, default: false },
  avatars: { type: Array, default: () => [] }
})

const bgStyle = props.image ? `background-image: url('${props.image}')` : ''
</script>

<style scoped>
/* keep defaults, sizes utility used in project */
</style>
