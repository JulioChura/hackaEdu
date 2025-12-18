<template>
  <div class="p-6 lg:p-10">
    <div class="mx-auto w-full max-w-[1400px] flex flex-col gap-8">
      <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
        <div class="flex flex-col gap-2 max-w-2xl">
          <h1 class="text-[#111318] text-3xl lg:text-4xl font-black leading-tight tracking-tight">Mis Cursos</h1>
          <p class="text-[#616f89] text-base font-normal leading-normal">Gestiona tus aulas activas y accede a las herramientas de evaluación.</p>
        </div>
        <div class="shrink-0">
          <button @click="showAddModal = true" class=" flex w-full md:w-auto cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-6 bg-blue-800 hover:bg-primary-hover transition-colors text-white gap-2 text-base font-bold shadow-lg">
            <span class="material-symbols-outlined">add</span>
            <span class="truncate">Crear Nueva Clase</span>
          </button>
        </div>
      </div>

      <div class="flex flex-col gap-6">

        <!-- Filters always visible on top (responsive) -->
        <div class="w-full">
          <FiltersPanel @change="onFilterChange" @apply="onFilterApply" @reset="onFilterReset" />
        </div>

        <div class="flex-1">

          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <CourseCard v-for="c in filtered" :key="c.id" v-bind="c" @view="viewCourse" />
            <div @click="showAddModal = true" class="flex flex-col justify-center items-center bg-[#f6f6f8] rounded-2xl border-2 border-dashed border-[#d1d5db] p-8 gap-4 hover:border-primary/50 hover:bg-blue-50/30 transition-all cursor-pointer group h-full min-h-[320px]">
              <div class="size-16 rounded-full bg-white flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-3xl text-[#616f89] group-hover:text-primary">add</span>
              </div>
              <div class="text-center">
                <h3 class="text-lg font-bold text-[#111318] group-hover:text-primary mb-1">Añadir Nuevo Curso</h3>
                <p class="text-sm text-[#616f89]">Configura una nueva aula virtual</p>
              </div>
            </div>
            </div>
          </div>
        </div>
      </div>
      
      <TeacherCoursesAddModal v-if="showAddModal" @close="showAddModal = false" @save="handleAddCourse" />

    </div>

</template>

<script setup>
import { ref, computed } from 'vue'
import CourseCard from '../../../shared/components/CourseCard.vue'
import FiltersPanel from '../../../shared/components/FiltersPanel.vue'
import TeacherCoursesAddModal from './components/TeacherCoursesAddModal.vue'

const courses = ref([
  { id: 1, code: 'MAT-101', title: 'Álgebra Lineal', group: 'Grupo 3B', semester: '2024-1', students: 34, image: '', isActive: true, avatars: [] },
  { id: 2, code: 'MAT-202', title: 'Cálculo Diferencial', group: 'Grupo 2A', semester: '2024-1', students: 28, image: '', isActive: true, avatars: [] },
  { id: 3, code: 'FIS-105', title: 'Física Mecánica', group: 'Grupo 1C', semester: '2024-1', students: 42, image: '', isActive: false, avatars: [] }
])

const showAddModal = ref(false)

function handleAddCourse(newCourse) {
  // ensure unique id
  newCourse.id = (courses.value.length ? Math.max(...courses.value.map(c => c.id)) : 0) + 1
  courses.value.push(newCourse)
}

const query = ref('')
const filters = ref({ q: '', status: 'all', from: '', to: '' })

function onFilterChange(payload) { filters.value = { ...filters.value, ...payload } }
function onFilterApply(payload) { filters.value = { ...filters.value, ...payload } }
function onFilterReset() { filters.value = { q: '', status: 'all', from: '', to: '' } }

function onSearch() { filters.value.q = query.value }

const filtered = computed(() => {
  let list = courses.value.slice()
  if (filters.value.q) {
    const q = filters.value.q.toLowerCase()
    list = list.filter(c => `${c.title} ${c.code} ${c.group} ${c.semester}`.toLowerCase().includes(q))
  }
  if (filters.value.status === 'active') list = list.filter(c => c.isActive)
  if (filters.value.status === 'archived') list = list.filter(c => !c.isActive)
  return list
})

function viewCourse(id) { console.log('view course', id) }
</script>

