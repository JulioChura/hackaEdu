<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="close" aria-hidden="true"></div>

    <div class="relative z-10 w-full max-w-[550px] flex flex-col bg-gray-100 rounded-3xl shadow-2xl border border-gray-200 overflow-hidden transform transition-all">
      
      <div class="flex items-center justify-between px-8 py-6 border-b border-gray-200/60">
        <h3 class="text-gray-900 text-xl font-extrabold tracking-tight">Crear Nueva Aula</h3>
        <button @click="close" class="text-gray-500 hover:text-blue-800 transition-colors p-1.5 rounded-xl hover:bg-gray-200">
          <span class="material-symbols-outlined text-2xl">close</span>
        </button>
      </div>

      <div class="p-8 flex flex-col gap-8">
        <div class="flex flex-col gap-2">
          <label class="text-gray-700 text-xs font-black uppercase tracking-widest ml-1" for="course-name">
            Nombre de la Clase
          </label>
          <input 
            id="course-name" 
            v-model="form.name" 
            type="text" 
            placeholder="Ej. Física Cuántica I" 
            class="w-full rounded-2xl border border-gray-300 bg-white h-14 px-5 text-gray-800 focus:border-blue-800 focus:ring-4 focus:ring-blue-800/10 outline-none transition-all shadow-sm" 
          />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-gray-700 text-xs font-black uppercase tracking-widest ml-1">Código de Acceso</label>
          <div class="flex flex-col sm:flex-row gap-3 items-stretch">
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <span class="material-symbols-outlined text-blue-800" style="font-size:20px">key</span>
              </div>
              <input 
                readonly 
                v-model="form.code" 
                class="w-full rounded-2xl border border-gray-300 bg-gray-50 h-14 pl-12 pr-4 text-blue-900 font-mono text-lg tracking-[0.2em] font-bold cursor-not-allowed shadow-inner" 
              />
            </div>

            <div class="flex gap-2 shrink-0">
              <button @click.prevent="generateCode" class="flex items-center justify-center rounded-2xl w-14 bg-white border border-gray-300 text-blue-800 hover:bg-blue-50 transition-all shadow-sm active:scale-90" title="Regenerar">
                <span class="material-symbols-outlined">autorenew</span>
              </button>
              <button @click.prevent="copyCode" class="flex items-center justify-center rounded-2xl w-14 bg-white border border-gray-300 text-blue-800 hover:bg-blue-50 transition-all shadow-sm active:scale-90" title="Copiar">
                <span class="material-symbols-outlined">content_copy</span>
              </button>
            </div>
          </div>
          <p class="text-[11px] text-gray-500 font-medium ml-1">
            <span class="text-blue-800 font-bold">Nota:</span> Los alumnos usarán este código para unirse.
          </p>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row justify-end items-center gap-4 px-8 py-6 border-t border-gray-200/60">
        <button 
          @click="close" 
          class="w-full sm:w-auto rounded-2xl h-14 px-8 text-gray-500 font-bold hover:text-gray-800 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="save" 
          :disabled="!canSave" 
          class="w-full sm:w-auto rounded-2xl h-14 px-12 bg-blue-800 hover:bg-blue-900 text-white shadow-xl shadow-blue-800/20 font-bold transition-all transform active:scale-95 disabled:opacity-30 disabled:grayscale disabled:pointer-events-none"
        >
          Guardar Classroom
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
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let s = ''
  for (let i = 0; i < len; i++) s += chars.charAt(Math.floor(Math.random() * chars.length))
  return s
}

function generateCode() { form.value.code = generateDefaultCode() }

async function copyCode() {
  try {
    await navigator.clipboard.writeText(form.value.code)
  } catch (e) {
    console.warn('Error al copiar', e)
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