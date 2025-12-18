<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="close" aria-hidden="true"></div>

    <div class="relative z-10 w-full max-w-[550px] flex flex-col bg-gray-50 rounded-2xl shadow-2xl border border-gray-200 overflow-hidden transform transition-all">
      
      <div class="flex items-center justify-between px-8 py-5 border-b border-gray-200 bg-white">
        <h3 class="text-blue-800 text-xl font-extrabold tracking-tight">Crear Nuevo Curso</h3>
        <button @click="close" class="text-gray-400 hover:text-blue-800 transition-colors p-1.5 rounded-lg hover:bg-gray-100">
          <span class="material-symbols-outlined text-2xl">close</span>
        </button>
      </div>

      <div class="p-8 flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <label class="text-gray-700 text-sm font-bold uppercase tracking-wider" for="course-name">Nombre del curso</label>
          <input 
            id="course-name" 
            v-model="form.name" 
            type="text" 
            placeholder="Ej. Matemáticas Avanzadas" 
            class="w-full rounded-xl border border-gray-300 bg-white h-12 px-4 text-gray-800 focus:border-blue-800 focus:ring-2 focus:ring-blue-800/20 outline-none transition-all shadow-sm" 
          />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-gray-700 text-sm font-bold uppercase tracking-wider">Código de acceso</label>
          <div class="flex flex-col sm:flex-row gap-2 items-stretch">
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="material-symbols-outlined text-blue-800/60" style="font-size:20px">lock</span>
              </div>
              <input 
                readonly 
                v-model="form.code" 
                class="w-full rounded-xl border border-gray-300 bg-gray-100 h-12 pl-10 pr-4 text-blue-900 font-mono tracking-widest font-bold cursor-not-allowed shadow-inner" 
              />
            </div>

            <div class="flex gap-2 shrink-0">
              <button @click.prevent="generateCode" class="flex items-center justify-center rounded-xl w-12 sm:w-auto sm:px-4 bg-white border border-gray-300 text-blue-800 hover:bg-blue-50 transition-colors shadow-sm" title="Regenerar">
                <span class="material-symbols-outlined">autorenew</span>
              </button>
              <button @click.prevent="copyCode" class="flex items-center justify-center rounded-xl w-12 sm:w-auto sm:px-4 bg-white border border-gray-300 text-blue-800 hover:bg-blue-50 transition-colors shadow-sm" title="Copiar">
                <span class="material-symbols-outlined">content_copy</span>
              </button>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 italic">Los estudiantes usarán este código para inscribirse automáticamente.</p>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row justify-end items-center gap-3 px-8 py-5 bg-white border-t border-gray-200">
        <button 
          @click="close" 
          class="w-full sm:w-auto rounded-xl h-12 px-6 text-gray-500 font-bold hover:bg-gray-100 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="save" 
          :disabled="!canSave" 
          class="w-full sm:w-auto rounded-xl h-12 px-10 bg-blue-800 hover:bg-blue-900 text-white shadow-md shadow-blue-800/30 font-bold transition-all transform active:scale-95 disabled:opacity-40 disabled:pointer-events-none"
        >
          Guardar Curso
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emits = defineEmits(['close', 'save'])

const form = ref({ name: '', code: generateDefaultCode() })

function generateDefaultCode() {
  return `${randomPart(3)}-${randomPart(3)}`
}

function randomPart(len) {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789' // Sin 'O', 'I', '1', '0' para evitar confusiones
  let s = ''
  for (let i = 0; i < len; i++) s += chars.charAt(Math.floor(Math.random() * chars.length))
  return s
}

function generateCode() { form.value.code = generateDefaultCode() }

async function copyCode() {
  try {
    await navigator.clipboard.writeText(form.value.code)
  } catch (e) {
    console.warn('Portapapeles no disponible', e)
  }
}

const canSave = computed(() => form.value.name.trim().length >= 3)

function save() {
  if (!canSave.value) return
  const newCourse = {
    id: Date.now(),
    code: form.value.code,
    title: form.value.name,
    group: '',
    semester: '',
    students: 0,
    image: '',
    isActive: true,
    avatars: []
  }
  emits('save', newCourse)
  emits('close')
}

function close() { emits('close') }
</script>