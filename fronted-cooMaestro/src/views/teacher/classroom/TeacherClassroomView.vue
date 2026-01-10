<template>
	<main class="flex-1 flex justify-center py-8 px-4 md:px-8 lg:px-12">
		<div class="w-full max-w-[1200px] flex flex-col gap-6">

			<!-- Breadcrumbs -->
			<div class="flex flex-wrap gap-2 items-center text-sm">
				<a class="text-[#616f89] dark:text-gray-400 font-medium hover:text-blue-800" href="#">Inicio</a>
				<span class="material-symbols-outlined text-[16px] text-[#616f89] dark:text-gray-500">chevron_right</span>
				<a class="text-[#616f89] dark:text-gray-400 font-medium hover:text-blue-800" href="#">Mis Salones</a>
				<span class="material-symbols-outlined text-[16px] text-[#616f89] dark:text-gray-500">chevron_right</span>
				<span class="text-blue-800 font-medium">Literatura 5º Grado</span>
			</div>

			<!-- Header component -->
			<Header title="Literatura 5º Grado" accessCode="LIT-5-2024">
				<template #actions>
					<button class="flex items-center justify-center gap-2 h-12 px-6 bg-blue-800 hover:bg-blue-900 text-white text-base font-bold rounded-lg shadow-md hover:shadow-lg transition-all transform active:scale-95">
						<span class="material-symbols-outlined">add_circle</span>
						<span>Crear Nueva Actividad</span>
					</button>
				</template>
			</Header>

			<!-- Stats Overview -->
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
				<StatCard>
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-blue-800 bg-blue-50 p-2 rounded-lg">insights</span>
						<p class="text-[#616f89] text-sm font-medium">Comprensión Lectora Promedio</p>
					</div>
					<div class="flex items-end gap-3 mt-1">
						<p class="text-3xl font-bold leading-tight">82%</p>
						<span class="flex items-center text-[#07883b] text-sm font-bold mb-1">
							<span class="material-symbols-outlined text-sm">trending_up</span>
							+5%
						</span>
					</div>
					<p class="text-xs text-[#616f89]">Mejora respecto al mes anterior</p>
				</StatCard>

				<StatCard>
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-orange-500 bg-orange-50 p-2 rounded-lg">assignment_turned_in</span>
						<p class="text-[#616f89] text-sm font-medium">Tareas Entregadas</p>
					</div>
					<div class="flex items-end gap-3 mt-1">
						<p class="text-3xl font-bold leading-tight">24/30</p>
						<span class="text-[#616f89] dark:text-gray-500 text-sm font-medium mb-1">Estudiantes</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-1">
						<div class="bg-orange-500 h-1.5 rounded-full" style="width: 80%"></div>
					</div>
				</StatCard>

				<StatCard>
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-purple-500 bg-purple-50 dark:bg-purple-900/30 p-2 rounded-lg">psychology</span>
						<p class="text-[#616f89] dark:text-gray-400 text-sm font-medium">Nivel de Lectura (IA)</p>
					</div>
					<div class="flex items-end gap-3 mt-1">
						<p class="text-3xl font-bold leading-tight">Intermedio</p>
					</div>
					<p class="text-xs text-[#616f89]">Basado en análisis de las últimas 3 lecturas</p>
				</StatCard>
			</div>

			<!-- Main Split Layout -->
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<ActivitiesContainer>
					<!-- Activities header & controls + activity cards copied here -->
					<div class="flex items-center justify-between">
						<h3 class="text-lg font-bold text-[#111318]">Actividades</h3>
						<div class="flex bg-gray-50 rounded-lg p-1">
							<button class="px-3 py-1 text-xs font-bold bg-white text-[#111318] rounded shadow-sm">Activas</button>
							<button class="px-3 py-1 text-xs font-medium text-[#616f89] hover:text-[#111318]">Pendientes</button>
							<button class="px-3 py-1 text-xs font-medium text-[#616f89] hover:text-[#111318]">Finalizadas</button>
						</div>
					</div>

					<!-- Activity cards: use ActivityCard component -->
					<ActivityCard
						title="Lectura: Don Quijote Cap. 1"
						subtitle="Asignada: 10 Oct • Vence: Mañana"
						icon="menu_book"
						status="En Progreso"
						:completed="18"
						:total="30"
						:progress="60"
					/>

					<ActivityCard
						title="Quiz de Vocabulario: Realismo Mágico"
						subtitle="Programada: 15 Oct"
						icon="quiz"
						status="Pendiente"
						:completed="0"
						:total="20"
						:progress="0"
						iconBg="bg-purple-50"
						statusBg="bg-gray-50 text-gray-800"
					/>

					<!-- other activity cards can be added similarly -->
				</ActivitiesContainer>

				<StudentsContainer>
					<div class="flex items-center justify-between">
						<h3 class="text-lg font-bold text-[#111318]">Estudiantes (30)</h3>
						<button class="text-blue-800 text-sm font-bold hover:underline">Gestionar</button>
					</div>
					  <div class="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-lg overflow-hidden flex flex-col h-full max-h-[600px]">
						<!-- Search -->
						<div class="p-3 border-b border-[#e5e7eb] dark:border-gray-800">
							<div class="relative">
								<span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
									<span class="material-symbols-outlined text-[#616f89] text-[20px]">search</span>
								</span>
								<input class="block w-full pl-10 pr-3 py-2 border border-transparent rounded-lg leading-5 bg-gray-50 text-[#111318] placeholder-[#616f89] focus:outline-none focus:bg-white focus:ring-1 focus:ring-blue-800 focus:border-blue-800 sm:text-sm transition-colors" placeholder="Buscar estudiante..." type="text"/>
							</div>
						</div>

						<!-- List -->
						<div class="overflow-y-auto flex-1 p-2 space-y-1">
							<!-- Student items: use StudentItem component -->
							<StudentItem name="Ana García" level="Avanzado" :percent="95" avatar="https://lh3.googleusercontent.com/aida-public/AB6AXuBPn7Epj5AUPtwF6zdlhI8VLonsxt7icRhV58CCvTDZbFxUaMRNPJtt5KEvOcGM1W3a8OG1_lSdBI8lizydR40hCfIxDUupHvIxgYZ_GSKHTsZqmKxvFA1sgXWy0D_Hd2GEJYdLLZ10ZgGpD5aMZXZnZkaX-M8BPM2cXvvRRYFK474Y8A5jh9E8RGMM5y4NZtrdV0U9CQsssa2TX60fUv5EUXLgrqqVqCefG46q23imh2dsYRhXUKeeGsmmXzBtObiKymj7nhfyNjY" />
							<StudentItem name="Carlos Méndez" level="Intermedio" :percent="82" avatar="" />
							<StudentItem name="Lucía Martínez" level="Principiante" :percent="45" />
							<StudentItem name="David Torres" level="Intermedio" :percent="78" />
							<StudentItem name="Sofia Ortiz" level="Avanzado" :percent="92" />
						</div>

						<div class="p-2 border-t border-[#e5e7eb] dark:border-gray-800 bg-[#f9fafb] dark:bg-gray-800/50 text-center">
							<button class="text-xs text-[#616f89] hover:text-blue-800 font-medium">Ver todos los estudiantes</button>
						</div>
					</div>
				</StudentsContainer>
			</div>
		</div>
	</main>
</template>

<script setup>
import Header from './components/Header.vue'
import StatCard from './components/StatCard.vue'
import ActivitiesContainer from './components/ActivitiesContainer.vue'
import StudentsContainer from './components/StudentsContainer.vue'
import ActivityCard from './components/ActivityCard.vue'
import StudentItem from './components/StudentItem.vue'
</script>

<style scoped>
/* page-scoped styles (if any) */
</style>

