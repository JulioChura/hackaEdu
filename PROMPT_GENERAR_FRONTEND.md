# PROMPT PARA GENERAR FRONTEND - HackaEdu

## CONTEXTO GENERAL
Genera un frontend completo en Vue.js 3 + Composition API + Tailwind CSS para HackaEdu, una plataforma de lectura comprensiva con niveles CEFR (A1-C2). El usuario puede ser ESTUDIANTE o ADMIN. La autenticación usa JWT (access/refresh tokens) y soporta login con Google OAuth. Backend en Django REST API en http://localhost:8000.

---

## ARQUITECTURA TÉCNICA

**Stack:**
- Vue 3 (Composition API)
- Vue Router (rutas protegidas)
- Pinia (state management)
- Tailwind CSS (estilos)
- Axios (HTTP)

**Stores Pinia:**
1. `authStore`: user, tokens (access/refresh), login(), logout(), refreshToken()
2. `lecturaStore`: lecturas[], fetchLecturas(), createLectura()
3. `sesionStore`: sesiones[], currentSesion, startSesion(), submitRespuesta()
4. `nivelStore`: niveles[], progresion, fetchProgresion()
5. `logroStore`: logros[], misLogros[], fetchLogros()

**Layout Components:**
- `AppLayout.vue`: Sidebar + TopBar + RouterView (estudiante)
- `AdminLayout.vue`: Sidebar + TopBar + RouterView (admin)
- `AuthLayout.vue`: Sin sidebar/topbar (login, registro)

---

## GESTIÓN DE IMÁGENES/PORTADAS

**Sistema de Imágenes:**
1. **Portadas Genéricas por Categoría**: Descargar/crear 1 imagen genérica por cada categoría
   - Ciencia → imagen azul con átomo/microscopio
   - Literatura → imagen púrpura con libro/pluma
   - Historia → imagen marrón con pergamino/reloj
   - Tecnología → imagen gris con circuito/código
   - Arte → imagen naranja con paleta/pincel
   - Negocios → imagen verde con gráfico/dinero
   - Viajes → imagen roja con mapa/brújula
   - Salud → imagen verde oscuro con corazón/píldora
   - Deportes → imagen roja con pelota/trofeo
   - Política → imagen azul oscuro con bandera/micrófono
   - (Crear más según necesidad)

2. **Almacenamiento de Imágenes**:
   - Carpeta `src/assets/images/categorias/` con imágenes nombradas por categoría:
     - `ciencia.jpg`, `literatura.jpg`, `historia.jpg`, etc.
   - Carpeta `src/assets/images/logros/` con iconos de logros
   - Carpeta `src/assets/images/niveles/` con iconos CEFR (A1, A2, B1, B2, C1, C2)

3. **Mapeo de Imágenes en Datos**:
   - Cada objeto `Lectura` tiene campo `categoria` (string)
   - En el frontend, crear función helper: `getImagenPorCategoria(categoria)` que devuelva ruta
   - La imagen se asigna automáticamente según la categoría
   - Si en futuro se agrega scraping, usar `lectura.imagen_url` (si existe), sino usar genérica de categoría

4. **Renderizado de Imágenes en Cards**:
   - Todos los cards de lectura muestran imagen con altura fija (200px) y ancho 100%
   - Usar `object-fit: cover` para mantener aspect ratio
   - Imagen debe ser clickeable (redirige a `/lecturas/{id}`)
   - Tamaños de imagen: 400x300px (comprimidas para web)

5. **Responsive Images**:
   - Mobile: imagen height 150px
   - Tablet: imagen height 180px
   - Desktop: imagen height 200px
   - Usar srcset para diferentes resolutions (1x, 2x)
   - Lazy loading con `loading="lazy"` en tags `<img>`

**Ejemplo de Uso:**
```vue
<template>
  <div class="lectura-card">
    <img 
      :src="getImagenPorCategoria(lectura.categoria)" 
      :alt="lectura.titulo"
      class="w-full h-48 object-cover rounded-lg"
      loading="lazy"
    />
    <h3>{{ lectura.titulo }}</h3>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  lectura: Object
})

const categoriaImageMap = {
  'Ciencia': '/images/categorias/ciencia.jpg',
  'Literatura': '/images/categorias/literatura.jpg',
  'Historia': '/images/categorias/historia.jpg',
  'Tecnología': '/images/categorias/tecnologia.jpg',
  'Arte': '/images/categorias/arte.jpg',
  'Negocios': '/images/categorias/negocios.jpg',
  'Viajes': '/images/categorias/viajes.jpg',
  'Salud': '/images/categorias/salud.jpg',
  'Deportes': '/images/categorias/deportes.jpg',
  'Política': '/images/categorias/politica.jpg'
}

const getImagenPorCategoria = (categoria) => {
  return categoriaImageMap[categoria] || '/images/categorias/default.jpg'
}
</script>
```

**Para Futuro (Scraping):**
- Campo `lectura.imagen_url` (nullable)
- Actualizar helper: `if (lectura.imagen_url) return lectura.imagen_url; else return genérica`
- Si scraping falla, fallback automático a imagen genérica

---

## FRAMES DETALLADOS (TODAS LAS PANTALLAS)

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 1. FRAME: LOGIN (`/login`)
**Layout:** `AuthLayout` (sin sidebar/topbar)

**Elementos:**
- Card centrado en pantalla con logo HackaEdu arriba
- Input email (type="email", placeholder="correo@ejemplo.com")
- Input password (type="password", placeholder="••••••••")
- Botón "Iniciar Sesión" (submit)
- Divisor horizontal con texto "O"
- Botón "Continuar con Google" (con icono de Google, href="/api/auth/google/login/")
- Link "¿No tienes cuenta? Regístrate" → `/register`
- Mensaje de error si login falla (alert rojo)

**Funcionalidad:**
- POST /api/auth/token/ con {email, password}
- Guardar access/refresh en localStorage
- Guardar user en authStore
- Redirigir a `/dashboard` si rol=ESTUDIANTE, `/admin/dashboard` si rol=ADMIN

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 2. FRAME: GOOGLE CALLBACK (`/auth/google/callback`)
**Layout:** `AuthLayout`

**Elementos:**
- Spinner de carga centrado
- Texto "Autenticando con Google..."

**Funcionalidad:**
- onMounted: POST /api/auth/convert-token/ (credentials: include)
- Guardar tokens en localStorage
- Redirigir a `/dashboard` o `/admin/dashboard` según rol

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 3. FRAME: REGISTRO (`/register`)
**Layout:** `AuthLayout`

**Elementos:**
- Card centrado
- Input nombre (placeholder="Juan")
- Input apellido (placeholder="Pérez")
- Input email (unique, type="email")
- Input password (min 8 caracteres)
- Input confirmar password
- Checkbox "Acepto términos y condiciones"
- Botón "Registrarse"
- Link "¿Ya tienes cuenta? Inicia sesión" → `/login`

**Funcionalidad:**
- POST /api/auth/register/ con {email, password, nombre, apellido}
- Retorna tokens automáticamente
- Guardar tokens y redirigir a `/dashboard`

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 4. FRAME: DASHBOARD ESTUDIANTE (`/dashboard`)
**Layout:** `AppLayout` (sidebar izquierda + topbar arriba)

**TOPBAR (fijo arriba, todas las pantallas estudiante):**
- Logo "HackaEdu" (izquierda)
- Barra de búsqueda (centro, placeholder="Buscar lecturas...")
- Icono de notificaciones (derecha)
- Avatar del usuario con dropdown:
  - Nombre completo
  - Email
  - "Mi Perfil" → `/profile`
  - "Configuración" → `/settings`
  - "Cerrar Sesión" (logout)

**SIDEBAR (fijo izquierda, todas las pantallas estudiante):**
- Item "Dashboard" (icono casa) → `/dashboard`
- Item "Mis Lecturas" (icono libro) → `/lecturas`
- Item "Nueva Lectura" (icono +) → `/lecturas/nueva`
- Item "Mis Sesiones" (icono clipboard) → `/sesiones`
- Item "Mi Progreso" (icono gráfico) → `/progreso`
- Item "Logros" (icono trofeo) → `/logros`
- Separador
- Indicador de nivel actual (badge): "Nivel: B1"
- Barra de progreso del nivel (% hasta próximo nivel)
- Puntos totales (icono estrella): "1,245 pts"

**CONTENIDO (área principal derecha del sidebar):**
- Sección "Resumen Rápido" (cards horizontales):
  - Card "Lecturas Completadas": número + icono
  - Card "Promedio de Puntaje": % + icono
  - Card "Nivel Actual": código CEFR + descripción
  - Card "Logros Desbloqueados": número + icono

- Sección "Continuar Leyendo" (si hay sesiones en progreso):
  - Card de lectura con:
    - Título
    - Nivel (badge)
    - Progreso (barra %)
    - Botón "Continuar" → `/sesiones/{id}`

- Sección "Lecturas Recomendadas" (basadas en nivel actual):
  - Grid de cards de lectura (3 columnas):
    - Cada card: título, categoría (badge), nivel (badge), duración estimada, botón "Iniciar"

- Sección "Últimos Logros" (últimos 3):
  - Lista horizontal de cards de logro:
    - Icono del logro
    - Nombre
    - Fecha de obtención

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 5. FRAME: MIS LECTURAS (`/lecturas`)
**Layout:** `AppLayout` (mismo topbar + sidebar)

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Mis Lecturas"
- Barra de filtros (fila horizontal):
  - Dropdown "Filtrar por Nivel" (Todos, A1, A2, B1, B2, C1, C2)
  - Dropdown "Filtrar por Categoría" (Todas, Ciencia, Literatura, Historia, etc.)
  - Dropdown "Filtrar por Estado" (Todas, Completadas, En Progreso, Pendientes)
  - Input búsqueda (placeholder="Buscar por título...")

- Grid de cards de lectura (3 columnas, responsive):
  - Cada card:
    - Thumbnail (si tiene imagen) o icono de categoría
    - Título
    - Nivel (badge coloreado)
    - Categoría (badge)
    - Modalidad (badge: IA, Manual, API)
    - Duración estimada (icono reloj + minutos)
    - Cantidad de palabras
    - Estado (badge): "Completada" (verde) / "En Progreso" (amarillo) / "Pendiente" (gris)
    - Botón "Ver Detalles" → `/lecturas/{id}`
    - Si completada: icono check verde

- Paginación al final (si hay >12 lecturas)

**Funcionalidad:**
- GET /api/lecturas/?nivel=B1&categoria=Ciencia&estado=completada
- Filtrado dinámico (watcher en filtros)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 6. FRAME: DETALLE DE LECTURA (`/lecturas/{id}`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Botón "← Volver" → `/lecturas`
- Card principal con lectura:
  - Sección izquierda (70%):
    - Título (h1)
    - Metadata (fila horizontal):
      - Nivel (badge grande)
      - Categoría (badge)
      - Modalidad (badge)
      - Autor/IA usado
      - Fecha de creación
    - Tags de interés (chips horizontales)
    - Contenido completo (texto formateado, scrollable)
  
  - Sección derecha (30%, sidebar card):
    - "Información"
    - Duración estimada: X minutos
    - Palabras: X
    - Preguntas: 15
    - Criterios evaluados (lista):
      - Comprensión Literal
      - Inferencial
      - Crítica
      - etc.
    - Si NO completada:
      - Botón "Iniciar Lectura" (grande, primario) → POST /api/sesiones/ {lectura_id, usuario_id}
    - Si completada:
      - Badge "✓ Completada"
      - Puntaje obtenido: X/100
      - Fecha de finalización
      - Botón "Ver Resultados" → `/sesiones/{sesion_id}/resultados`
      - Botón "Reintentar" (secundario)

**Funcionalidad:**
- GET /api/lecturas/{id}/
- GET /api/sesiones/?lectura={id}&usuario={user_id} (para ver si ya completó)
- POST /api/sesiones/ crea nueva sesión y redirige a `/sesiones/{sesion_id}`

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 7. FRAME: TOMAR LECTURA/SESIÓN (`/sesiones/{id}`)
**Layout:** `AppLayout` (IMPORTANTE: sidebar colapsado, topbar simplificado)

**TOPBAR SIMPLIFICADO:**
- Logo HackaEdu (izquierda)
- Título de la lectura (centro)
- Timer (derecha): "12:34" contando hacia arriba
- Botón "Salir" (X) → confirmar modal

**SIDEBAR:** OCULTO (o colapsado a iconos pequeños)

**CONTENIDO (pantalla completa):**
- Layout de 2 columnas (60% lectura, 40% pregunta):

**COLUMNA IZQUIERDA (lectura):**
- Card con contenido de la lectura (scrollable)
- Marcador de scroll (arriba → medio → abajo)

**COLUMNA DERECHA (preguntas):**
- Indicador de progreso: "Pregunta 3 de 15"
- Barra de progreso visual (20%)
- Card de pregunta actual:
  - Número: "Pregunta 3"
  - Tipo: badge (Multiple Choice, Verdadero/Falso, etc.)
  - Criterio: badge (Comprensión Literal)
  - Texto de la pregunta
  - Si tipo Multiple Choice:
    - Radio buttons con opciones A, B, C, D
  - Si tipo Completar:
    - Input text
  - Si tipo Verdadero/Falso:
    - Dos botones grandes: "Verdadero" / "Falso"
- Botones de navegación:
  - "← Anterior" (disabled si es pregunta 1)
  - "Siguiente →" (primario)
  - Si es última pregunta: "Finalizar Lectura" (verde, grande)

**MODAL DE FINALIZACIÓN:**
- "¿Estás seguro de finalizar?"
- "Has respondido X de 15 preguntas"
- Botón "Cancelar" / Botón "Finalizar" (primario)

**Funcionalidad:**
- GET /api/sesiones/{id}/ (cargar sesión + lectura + preguntas)
- POST /api/respuestas/ {sesion, pregunta, respuesta_usuario} (guardar cada respuesta)
- PATCH /api/sesiones/{id}/ {estado: 'COMPLETADA'} al finalizar
- Redirigir a `/sesiones/{id}/resultados` al completar

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 8. FRAME: RESULTADOS DE SESIÓN (`/sesiones/{id}/resultados`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Botón "← Volver a Mis Lecturas" → `/lecturas`
- Card principal "Resultados":
  - Header con:
    - Título de la lectura
    - Fecha y hora de finalización
    - Duración total (minutos)
  
  - Sección "Puntaje General":
    - Círculo grande con puntaje: "85/100" (coloreado según rango)
    - Mensaje: "¡Excelente trabajo!" / "Puedes mejorar"
  
  - Sección "Desglose por Criterio" (cards horizontales):
    - Card por cada criterio:
      - Nombre del criterio
      - Puntaje: X/100
      - Barra de progreso coloreada
      - Icono según desempeño (✓, ~, ✗)
  
  - Sección "Respuestas Detalladas" (accordion):
    - Item por cada pregunta (15 items):
      - Header: "Pregunta 1 - Comprensión Literal"
      - Indicador: ✓ Correcta / ✗ Incorrecta
      - Al expandir:
        - Texto de la pregunta
        - Tu respuesta: "A"
        - Respuesta correcta: "B"
        - Explicación (si disponible)
        - Tiempo de respuesta: X segundos
  
  - Sección "Acciones":
    - Botón "Compartir Resultados" (secundario)
    - Botón "Reintentar Lectura" (primario) → crea nueva sesión
    - Botón "Volver a Lecturas" (secundario)

**Funcionalidad:**
- GET /api/sesiones/{id}/ (incluye puntajes, respuestas, desempeño por criterio)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 9. FRAME: MIS SESIONES (`/sesiones`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Mis Sesiones"
- Filtros:
  - Dropdown "Estado" (Todas, Completadas, En Progreso)
  - Dropdown "Nivel" (Todos, A1, A2, ...)
  - Date picker "Desde" y "Hasta"

- Tabla de sesiones:
  - Columnas:
    - Lectura (título + icono)
    - Nivel (badge)
    - Estado (badge coloreado)
    - Fecha Inicio
    - Fecha Fin
    - Duración
    - Puntaje (0-100 o "En progreso")
    - Acciones:
      - Si completada: botón "Ver Resultados"
      - Si en progreso: botón "Continuar"
  
- Paginación

**Funcionalidad:**
- GET /api/sesiones/?usuario={user_id}&estado=COMPLETADA

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 10. FRAME: MI PROGRESO (`/progreso`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Mi Progreso"

- Sección "Nivel Actual":
  - Card grande con:
    - Badge de nivel actual: "B1 - Intermedio"
    - Descripción del nivel (del modelo NivelCEFR)
    - Barra de progreso: "15/25 lecturas completadas"
    - Promedio de puntaje en este nivel: "78.5/100"
    - Puntos acumulados en nivel: "450 pts"
    - Requisito para ascender: "Promedio ≥ 80 y 25 lecturas"
    - Estado: "¡Estás listo para ascender!" (si cumple) / "Te faltan X lecturas"

- Sección "Historial de Niveles":
  - Timeline vertical:
    - Item por cada nivel alcanzado:
      - Badge de nivel
      - Fecha de ascenso
      - Lecturas completadas en ese nivel
      - Promedio obtenido

- Sección "Desempeño por Criterio" (gráfico de radar):
  - Eje por cada criterio de habilidad
  - Puntaje promedio en cada criterio (0-100)
  - Coloreado según fortaleza/debilidad

- Sección "Estadísticas Generales":
  - Cards pequeños:
    - Total de lecturas: X
    - Promedio general: X/100
    - Tiempo total de lectura: X horas
    - Racha actual: X días consecutivos

**Funcionalidad:**
- GET /api/usuarios/{id}/progresion/
- GET /api/sesiones/?usuario={id} (para calcular estadísticas)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 11. FRAME: LOGROS (`/logros`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Logros"
- Tabs:
  - Tab "Mis Logros" (activo)
  - Tab "Todos los Logros"

**TAB "MIS LOGROS":**
- Grid de cards de logro (4 columnas):
  - Cada card:
    - Icono/imagen del logro (grande, coloreado)
    - Nombre del logro
    - Descripción
    - Fecha de obtención
    - Puntos otorgados
    - Badge "Desbloqueado" (verde)

**TAB "TODOS LOS LOGROS":**
- Grid similar pero incluye logros bloqueados:
  - Logros desbloqueados: coloreados
  - Logros bloqueados: en gris con icono de candado
    - Requisitos: "Completa 10 lecturas de nivel B1"
    - Progreso: "7/10" con barra

**Funcionalidad:**
- GET /api/logros/ (todos)
- GET /api/logros/?usuario={id} (mis logros)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 12. FRAME: MI PERFIL (`/profile`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Mi Perfil"
- Layout de 2 columnas:

**COLUMNA IZQUIERDA (30%):**
- Card "Información Personal":
  - Avatar (grande, editable con upload)
  - Nombre completo
  - Email
  - Rol (badge)
  - Miembro desde: fecha
  - Botón "Editar Perfil"

**COLUMNA DERECHA (70%):**
- Tabs:
  - Tab "Información General"
  - Tab "Estadísticas"
  - Tab "Actividad Reciente"

**TAB "INFORMACIÓN GENERAL":**
- Form editable:
  - Input Nombre
  - Input Apellido
  - Input Email (disabled)
  - Input Teléfono (opcional)
  - Date picker Fecha de Nacimiento (opcional)
  - Botón "Guardar Cambios"

**TAB "ESTADÍSTICAS":**
- Cards de resumen:
  - Lecturas completadas
  - Promedio general
  - Nivel actual
  - Puntos totales
  - Logros desbloqueados
  - Tiempo total de lectura

**TAB "ACTIVIDAD RECIENTE":**
- Lista de actividades:
  - Item: "Completaste la lectura 'X'" - fecha
  - Item: "Desbloqueaste el logro 'Y'" - fecha
  - Item: "Ascendiste a nivel B2" - fecha
  - (últimas 10 actividades)

**Funcionalidad:**
- GET /api/auth/users/profile/
- PUT /api/auth/users/update_profile/ {nombre, apellido, telefono, fecha_nacimiento, avatar}

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 13. FRAME: CONFIGURACIÓN (`/settings`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Configuración"
- Secciones colapsables (accordion):

**Sección "Cuenta":**
- Email actual (disabled)
- Link "Cambiar Contraseña" → modal
- Link "Vincular con Google" (si no vinculado) → OAuth flow
- Si vinculado: "Conectado con Google" + email de Google

**Modal "Cambiar Contraseña":**
- Input Contraseña Actual
- Input Nueva Contraseña
- Input Confirmar Nueva Contraseña
- Botón "Cambiar" / "Cancelar"

**Sección "Notificaciones":**
- Checkbox "Recibir notificaciones por email"
- Checkbox "Notificar nuevos logros"
- Checkbox "Notificar cuando esté listo para ascender de nivel"
- Botón "Guardar Preferencias"

**Sección "Privacidad":**
- Dropdown "¿Quién puede ver mi perfil?" (Todos, Solo yo, Amigos)
- Checkbox "Mostrar mi progreso en rankings"

**Sección "Eliminar Cuenta":**
- Texto de advertencia
- Botón "Eliminar mi Cuenta" (rojo) → modal de confirmación

**Funcionalidad:**
- POST /api/auth/users/change_password/
- PATCH /api/auth/users/update_profile/ (notificaciones, privacidad)
- DELETE /api/auth/users/{id}/ (eliminar cuenta)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 14. FRAME: NUEVA LECTURA (ESTUDIANTE) (`/lecturas/nueva`)
**Layout:** `AppLayout`

**TOPBAR:** (igual frame 4)
**SIDEBAR:** (igual frame 4)

**CONTENIDO:**
- Título "Crear Nueva Lectura"
- Form con steps (wizard de 3 pasos):

**STEP 1: "Contenido"**
- Radio buttons "Modalidad":
  - "Generar con IA" (seleccionado por defecto)
  - "Ingresar Manualmente"
  - "Importar desde URL" (API de noticias)
  - "Personalizada" (subir archivo)

- Si "Generar con IA":
  - Textarea "Tema o Prompt" (placeholder="Ej: Artículo sobre la fotosíntesis para nivel B1")
  - Dropdown "Modelo de IA" (GPT-4, Claude, etc.)
  
- Si "Ingresar Manualmente":
  - Input "Título"
  - Textarea "Contenido" (grande)

- Si "Importar desde URL":
  - Input "URL del artículo"
  - Botón "Extraer contenido"

- Si "Personalizada":
  - File upload (.pdf, .docx, .txt)

- Botón "Siguiente →"

**STEP 2: "Detalles"**
- Dropdown "Nivel CEFR" (A1, A2, B1, B2, C1, C2)
- Dropdown "Categoría" (Ciencia, Literatura, Historia, etc.)
- Input "Duración estimada (minutos)"
- Tags de interés (chips editables): "tecnología", "educación", etc.
- Checkbox "Generar preguntas automáticamente con IA"
- Botón "← Anterior" / "Siguiente →"

**STEP 3: "Preguntas"**
- Si marcó "Generar con IA":
  - Botón "Generar Preguntas" → loading → muestra 15 preguntas generadas
  - Lista editable de preguntas:
    - Cada pregunta tiene:
      - Input texto de pregunta
      - Dropdown tipo (Multiple, Completar, etc.)
      - Dropdown criterio (Literal, Inferencial, etc.)
      - Si Multiple: inputs para opciones A, B, C, D
      - Input respuesta correcta
      - Textarea explicación
      - Botón "Eliminar pregunta"
  - Botón "Agregar Pregunta" (hasta 15 máximo)

- Si no marcó IA:
  - Form vacío para crear preguntas manualmente (igual estructura)

- Botón "← Anterior" / "Crear Lectura" (primario, verde)

**Funcionalidad:**
- POST /api/lecturas/ {titulo, contenido, nivel, categoria, modalidad, ...}
- POST /api/preguntas/ (bulk create 15 preguntas)
- Si usa IA: POST /api/llm/generar-contenido/ o /api/llm/generar-preguntas/
- Redirigir a `/lecturas/{id}` al crear

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 15. FRAME: ADMIN DASHBOARD (`/admin/dashboard`)
**Layout:** `AdminLayout` (sidebar + topbar para admin)

**TOPBAR ADMIN:**
- Logo "HackaEdu Admin"
- Barra de búsqueda
- Icono notificaciones
- Avatar con dropdown:
  - Nombre
  - "Ver como Estudiante" → cambiar a layout estudiante
  - "Configuración"
  - "Cerrar Sesión"

**SIDEBAR ADMIN:**
- Item "Dashboard" → `/admin/dashboard`
- Item "Usuarios" → `/admin/usuarios`
- Item "Lecturas" → `/admin/lecturas`
- Item "Sesiones" → `/admin/sesiones`
- Item "Niveles CEFR" → `/admin/niveles`
- Item "Categorías" → `/admin/categorias`
- Item "Logros" → `/admin/logros`
- Item "Criterios" → `/admin/criterios`
- Separador
- Item "Reportes" → `/admin/reportes`
- Item "Configuración" → `/admin/settings`

**CONTENIDO:**
- Sección "Métricas Generales" (cards horizontales):
  - Card "Total Usuarios": número + gráfico de tendencia
  - Card "Lecturas Creadas": número
  - Card "Sesiones Completadas Hoy": número
  - Card "Promedio General": porcentaje

- Sección "Actividad Reciente" (tabla):
  - Columnas: Usuario, Acción, Fecha/Hora
  - Últimas 10 acciones

- Sección "Lecturas Más Populares" (top 5):
  - Lista con:
    - Título
    - Veces completada
    - Promedio de puntaje

- Sección "Usuarios Activos" (gráfico de línea):
  - Últimos 7 días
  - Usuarios activos por día

**Funcionalidad:**
- GET /api/admin/dashboard/ (métricas agregadas)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 16. FRAME: ADMIN USUARIOS (`/admin/usuarios`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Gestión de Usuarios"
- Filtros:
  - Input búsqueda (email, nombre)
  - Dropdown "Rol" (Todos, ESTUDIANTE, ADMIN)
  - Dropdown "Nivel" (Todos, A1, A2, ...)
  - Dropdown "Estado" (Todos, Activos, Inactivos)
- Botón "Exportar CSV" (esquina superior derecha)

- Tabla de usuarios:
  - Columnas:
    - Avatar (pequeño)
    - Nombre Completo
    - Email
    - Rol (badge)
    - Nivel Actual
    - Lecturas Completadas
    - Promedio
    - Fecha Registro
    - Estado (activo/inactivo, switch)
    - Acciones:
      - Botón "Ver Perfil" → `/admin/usuarios/{id}`
      - Botón "Editar" → modal
      - Botón "Eliminar" → confirmación

- Paginación

**Modal "Editar Usuario":**
- Input Nombre
- Input Apellido
- Input Email
- Dropdown Rol (ESTUDIANTE, ADMIN)
- Dropdown Nivel CEFR
- Switch "Usuario Activo"
- Botón "Guardar" / "Cancelar"

**Funcionalidad:**
- GET /api/usuarios/?search=juan&rol=ESTUDIANTE
- PATCH /api/usuarios/{id}/ (editar)
- DELETE /api/usuarios/{id}/ (eliminar)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 17. FRAME: ADMIN LECTURAS (`/admin/lecturas`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Gestión de Lecturas"
- Filtros:
  - Input búsqueda (título)
  - Dropdown "Nivel"
  - Dropdown "Categoría"
  - Dropdown "Modalidad"
- Botón "Nueva Lectura" (primario) → `/admin/lecturas/nueva`

- Tabla de lecturas:
  - Columnas:
    - ID
    - Título
    - Nivel (badge)
    - Categoría
    - Modalidad
    - Preguntas (15/15 o 10/15 si incompleta)
    - Veces Completada
    - Promedio Puntaje
    - Fecha Creación
    - Acciones:
      - Botón "Ver" → `/lecturas/{id}` (vista estudiante)
      - Botón "Editar" → `/admin/lecturas/{id}/editar`
      - Botón "Duplicar" → crea copia
      - Botón "Eliminar" → confirmación

- Paginación

**Funcionalidad:**
- GET /api/lecturas/?search=&nivel=B1
- POST /api/lecturas/ (crear)
- PATCH /api/lecturas/{id}/ (editar)
- DELETE /api/lecturas/{id}/ (eliminar)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 18. FRAME: ADMIN EDITAR LECTURA (`/admin/lecturas/{id}/editar`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Botón "← Volver a Lecturas"
- Título "Editar Lectura: {título}"
- Tabs:
  - Tab "Contenido" (activo)
  - Tab "Detalles"
  - Tab "Preguntas"

**TAB "CONTENIDO":**
- Textarea "Contenido" (valor actual, editable)
- Botón "Regenerar con IA" (si modalidad IA)
- Botón "Guardar Cambios"

**TAB "DETALLES":**
- Input "Título"
- Dropdown "Nivel CEFR"
- Dropdown "Categoría"
- Dropdown "Modalidad" (disabled)
- Input "Duración estimada"
- Textarea "Tags" (chips)
- Botón "Guardar Cambios"

**TAB "PREGUNTAS":**
- Lista de las 15 preguntas (accordion):
  - Cada item expandible:
    - Texto pregunta (editable)
    - Tipo (editable)
    - Criterio (editable)
    - Opciones (si Multiple, editables)
    - Respuesta correcta (editable)
    - Explicación (editable)
    - Botón "Eliminar Pregunta"
- Botón "Agregar Pregunta" (si <15)
- Botón "Regenerar Todas con IA"
- Botón "Guardar Cambios"

**Funcionalidad:**
- GET /api/lecturas/{id}/
- GET /api/preguntas/?lectura={id}
- PATCH /api/lecturas/{id}/ (actualizar)
- PATCH /api/preguntas/{id}/ (actualizar pregunta)
- POST /api/preguntas/ (crear nueva)
- DELETE /api/preguntas/{id}/ (eliminar)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 19. FRAME: ADMIN SESIONES (`/admin/sesiones`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Gestión de Sesiones"
- Filtros:
  - Input búsqueda (usuario, lectura)
  - Dropdown "Estado" (Todas, Completadas, En Progreso, Iniciadas)
  - Dropdown "Nivel"
  - Date picker "Desde" - "Hasta"
- Botón "Exportar CSV"

- Tabla de sesiones:
  - Columnas:
    - ID
    - Usuario (nombre + avatar pequeño)
    - Lectura (título)
    - Nivel
    - Estado (badge)
    - Fecha Inicio
    - Fecha Fin
    - Duración (minutos)
    - Puntaje (0-100)
    - Acciones:
      - Botón "Ver Detalles" → `/admin/sesiones/{id}/detalle`
      - Botón "Ver Respuestas" → modal
      - Botón "Eliminar" → confirmación

- Paginación

**Modal "Ver Respuestas":**
- Lista de 15 respuestas:
  - Pregunta texto
  - Respuesta usuario
  - Correcta/Incorrecta (icono)
  - Tiempo respuesta
- Botón "Cerrar"

**Funcionalidad:**
- GET /api/sesiones/?search=&estado=COMPLETADA&desde=2024-01-01
- GET /api/respuestas/?sesion={id}
- DELETE /api/sesiones/{id}/

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 20. FRAME: ADMIN NIVELES CEFR (`/admin/niveles`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Niveles CEFR"
- Botón "Nuevo Nivel" (raramente usado, solo 6 niveles)

- Tabla de niveles (6 filas fijas: A1, A2, B1, B2, C1, C2):
  - Columnas:
    - Código (A1, A2, etc.)
    - Nombre (Principiante, Elemental, etc.)
    - Lecturas Requeridas (para ascender)
    - Promedio Requerido (%)
    - Cantidad Preguntas por Lectura
    - Distribución (JSON, collapsed)
    - Acciones:
      - Botón "Editar" → modal

**Modal "Editar Nivel":**
- Input "Código" (disabled)
- Input "Nombre"
- Input "Descripción" (textarea)
- Input "Cantidad de Preguntas" (15 default)
- Input "Lecturas para Ascender" (número)
- Input "Promedio Requerido" (0-100)
- JSON editor "Distribución de Preguntas" (por criterio)
- Botón "Guardar" / "Cancelar"

**Funcionalidad:**
- GET /api/niveles/
- PATCH /api/niveles/{id}/

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 21. FRAME: ADMIN CATEGORÍAS (`/admin/categorias`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Categorías de Lectura"
- Botón "Nueva Categoría" (primario) → modal

- Grid de cards de categoría (4 columnas):
  - Cada card:
    - Icono (grande, editable)
    - Nombre
    - Descripción
    - Color (badge coloreado)
    - Lecturas Asociadas (número)
    - Acciones:
      - Botón "Editar" → modal
      - Botón "Eliminar" → confirmación

**Modal "Nueva/Editar Categoría":**
- Input "Nombre"
- Textarea "Descripción"
- File upload "Icono" (o selector de iconos)
- Color picker "Color"
- Botón "Guardar" / "Cancelar"

**Funcionalidad:**
- GET /api/categorias/
- POST /api/categorias/ (crear)
- PATCH /api/categorias/{id}/ (editar)
- DELETE /api/categorias/{id}/ (eliminar)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 22. FRAME: ADMIN LOGROS (`/admin/logros`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Gestión de Logros"
- Botón "Nuevo Logro" (primario) → modal

- Grid de cards de logro (3 columnas):
  - Cada card:
    - Icono del logro (grande)
    - Nombre
    - Descripción
    - Tipo (badge: LECTURA, NIVEL, RACHA, PUNTAJE, ESPECIAL)
    - Requisito (texto: "10 lecturas completadas")
    - Puntos otorgados
    - Usuarios que lo tienen (número)
    - Acciones:
      - Botón "Editar" → modal
      - Botón "Ver Usuarios" → modal con lista
      - Botón "Eliminar" → confirmación

**Modal "Nuevo/Editar Logro":**
- Input "Nombre"
- Textarea "Descripción"
- File upload "Icono"
- Dropdown "Tipo" (LECTURA, NIVEL, RACHA, PUNTAJE, ESPECIAL)
- Input "Requisito" (texto descriptivo)
- Input "Requisito Cantidad" (número, si aplica)
- Input "Puntos Otorgados"
- Checkbox "Logro Oculto" (no se muestra hasta desbloquearlo)
- Botón "Guardar" / "Cancelar"

**Funcionalidad:**
- GET /api/logros/
- POST /api/logros/ (crear)
- PATCH /api/logros/{id}/ (editar)
- DELETE /api/logros/{id}/ (eliminar)
- GET /api/logros/{id}/usuarios/ (usuarios que lo tienen)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 23. FRAME: ADMIN CRITERIOS (`/admin/criterios`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Criterios de Habilidad"
- Botón "Nuevo Criterio" → modal

- Tabla de criterios:
  - Columnas:
    - Código (LITERAL, INFERENCIAL, CRITICA, etc.)
    - Nombre
    - Descripción
    - Peso (%)
    - Fórmula de Cálculo (texto)
    - Acciones:
      - Botón "Editar" → modal
      - Botón "Eliminar" → confirmación

**Modal "Nuevo/Editar Criterio":**
- Input "Código" (UPPERCASE, unique)
- Input "Nombre"
- Textarea "Descripción"
- Input "Peso" (0-100, suma de todos debe ser 100)
- Textarea "Fórmula de Cálculo" (texto descriptivo)
- Botón "Guardar" / "Cancelar"

**Funcionalidad:**
- GET /api/criterios/
- POST /api/criterios/ (crear)
- PATCH /api/criterios/{id}/ (editar)
- DELETE /api/criterios/{id}/ (eliminar)

---

### ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### 24. FRAME: ADMIN REPORTES (`/admin/reportes`)
**Layout:** `AdminLayout`

**TOPBAR ADMIN:** (igual frame 15)
**SIDEBAR ADMIN:** (igual frame 15)

**CONTENIDO:**
- Título "Reportes y Analíticas"
- Tabs:
  - Tab "General"
  - Tab "Usuarios"
  - Tab "Lecturas"
  - Tab "Desempeño"

**TAB "GENERAL":**
- Date picker "Rango de Fechas"
- Cards de métricas:
  - Nuevos usuarios (período)
  - Sesiones completadas (período)
  - Promedio general (período)
  - Tiempo total de lectura (período)
- Gráficos:
  - Línea: Usuarios activos por día
  - Barra: Lecturas completadas por nivel
  - Pie: Distribución por categoría

**TAB "USUARIOS":**
- Tabla top 10 usuarios más activos:
  - Nombre, Lecturas completadas, Promedio, Puntos
- Gráfico: Distribución de usuarios por nivel CEFR
- Botón "Exportar Reporte CSV"

**TAB "LECTURAS":**
- Tabla top 10 lecturas más populares:
  - Título, Nivel, Veces completada, Promedio puntaje
- Gráfico: Distribución de lecturas por nivel
- Tabla: Lecturas menos populares (para revisar calidad)

**TAB "DESEMPEÑO":**
- Gráfico: Promedio por criterio de habilidad (radar)
- Tabla: Criterios con menor desempeño (para enfoque educativo)
- Tabla: Usuarios con desempeño bajo (para intervención)

**Funcionalidad:**
- GET /api/reportes/general/?desde=&hasta=
- GET /api/reportes/usuarios/
- GET /api/reportes/lecturas/
- GET /api/reportes/desempeno/

---

## RUTAS PROTEGIDAS Y ROLES

**Rutas Públicas (sin autenticación):**
- `/login`
- `/register`
- `/auth/google/callback`

**Rutas Estudiante (requiere rol ESTUDIANTE):**
- `/dashboard`
- `/lecturas`, `/lecturas/{id}`, `/lecturas/nueva`
- `/sesiones`, `/sesiones/{id}`, `/sesiones/{id}/resultados`
- `/progreso`
- `/logros`
- `/profile`
- `/settings`

**Rutas Admin (requiere rol ADMIN):**
- `/admin/dashboard`
- `/admin/usuarios`, `/admin/usuarios/{id}`
- `/admin/lecturas`, `/admin/lecturas/{id}/editar`
- `/admin/sesiones`
- `/admin/niveles`
- `/admin/categorias`
- `/admin/logros`
- `/admin/criterios`
- `/admin/reportes`

**Guards en router:**
```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const requiredRole = to.meta.role
  
  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (requiredRole && authStore.user.rol !== requiredRole) {
    next('/dashboard') // o /admin/dashboard según rol
  } else {
    next()
  }
})
```

---

## API ENDPOINTS (RESUMEN)

**Auth:**
- POST /api/auth/token/ {email, password} → {access, refresh}
- POST /api/auth/token/refresh/ {refresh} → {access}
- POST /api/auth/register/ {email, password, nombre, apellido} → {access, refresh, user}
- GET /api/auth/users/profile/ → {user data}
- PUT /api/auth/users/update_profile/ {nombre, apellido, ...}
- POST /api/auth/users/change_password/ {old_password, new_password}
- GET /api/auth/google/login/ → redirect to Google
- GET /api/auth/convert-token/ → {access, refresh, user, google_data}

**Lecturas:**
- GET /api/lecturas/ → [lecturas]
- GET /api/lecturas/{id}/ → {lectura + preguntas}
- POST /api/lecturas/ {titulo, contenido, ...} → {lectura}
- PATCH /api/lecturas/{id}/ {titulo, ...}
- DELETE /api/lecturas/{id}/

**Preguntas:**
- GET /api/preguntas/?lectura={id} → [preguntas]
- POST /api/preguntas/ {lectura, texto, tipo, ...}
- PATCH /api/preguntas/{id}/
- DELETE /api/preguntas/{id}/

**Sesiones:**
- GET /api/sesiones/ → [sesiones]
- GET /api/sesiones/{id}/ → {sesion + respuestas + puntajes}
- POST /api/sesiones/ {usuario, lectura} → {sesion}
- PATCH /api/sesiones/{id}/ {estado: 'COMPLETADA'}

**Respuestas:**
- POST /api/respuestas/ {sesion, pregunta, respuesta_usuario} → {respuesta + es_correcta + puntos}

**Usuarios:**
- GET /api/usuarios/ → [usuarios] (admin)
- GET /api/usuarios/{id}/progresion/ → {nivel_actual, lecturas_completadas, ...}
- PATCH /api/usuarios/{id}/ {nombre, nivel, ...}

**Niveles:**
- GET /api/niveles/ → [niveles CEFR]
- PATCH /api/niveles/{id}/

**Categorías:**
- GET /api/categorias/ → [categorias]
- POST /api/categorias/
- PATCH /api/categorias/{id}/

**Logros:**
- GET /api/logros/ → [todos logros]
- GET /api/logros/?usuario={id} → [logros del usuario]
- POST /api/logros/
- PATCH /api/logros/{id}/

**Criterios:**
- GET /api/criterios/ → [criterios habilidad]
- POST /api/criterios/
- PATCH /api/criterios/{id}/

**Reportes (admin):**
- GET /api/reportes/general/
- GET /api/reportes/usuarios/
- GET /api/reportes/lecturas/
- GET /api/reportes/desempeno/

---

## COMPONENTES REUTILIZABLES IMPORTANTES

1. **LecturaCard.vue**: Card de lectura (usado en listados)
   - Props: lectura (object)
   - Emits: @click
   - Muestra: título, nivel, categoría, duración, estado

2. **PreguntaForm.vue**: Form para crear/editar pregunta
   - Props: pregunta (object), readOnly (boolean)
   - Emits: @save, @cancel
   - Maneja todos los tipos de pregunta

3. **ProgressBar.vue**: Barra de progreso reutilizable
   - Props: progress (0-100), color, label

4. **LogroCard.vue**: Card de logro
   - Props: logro (object), isUnlocked (boolean)
   - Muestra: icono, nombre, descripción, fecha

5. **UserAvatar.vue**: Avatar con dropdown
   - Props: user (object)
   - Emits: @logout, @profile, @settings

6. **StatCard.vue**: Card de estadística
   - Props: title, value, icon, trend
   - Muestra métricas con icono y tendencia

7. **Modal.vue**: Modal genérico
   - Props: isOpen, title, size
   - Slots: default (contenido), footer (botones)

8. **Sidebar.vue**: Sidebar para layouts
   - Props: items (array), collapsed (boolean)
   - Emits: @navigate

9. **TopBar.vue**: Topbar para layouts
   - Props: title, showSearch
   - Slots: actions (botones personalizados)

---

## PALETA DE COLORES (Sugerida)

- **Primario**: #4F46E5 (Indigo) - Botones principales, enlaces
- **Secundario**: #10B981 (Verde) - Success, logros
- **Acento**: #F59E0B (Amber) - Alertas, badges importantes
- **Peligro**: #EF4444 (Rojo) - Errores, eliminar
- **Fondo**: #F9FAFB (Gris claro)
- **Texto**: #111827 (Gris oscuro)
- **Bordes**: #E5E7EB (Gris medio)

**Badges por nivel CEFR:**
- A1: #3B82F6 (Azul)
- A2: #10B981 (Verde)
- B1: #F59E0B (Amarillo)
- B2: #EF4444 (Naranja)
- C1: #8B5CF6 (Púrpura)
- C2: #EC4899 (Rosa)

---

## NOTAS ADICIONALES

1. **Responsive Design**: Todas las pantallas deben ser responsive (mobile, tablet, desktop)
2. **Loading States**: Mostrar spinners o skeletons mientras cargan datos
3. **Error Handling**: Toasts/alerts para errores de API
4. **Validación**: Validar forms antes de enviar (email, contraseñas, campos requeridos)
5. **Confirmaciones**: Modales de confirmación para acciones destructivas (eliminar, salir de sesión)
6. **Auto-save**: En forms largos (crear lectura), guardar drafts en localStorage
7. **Dark Mode**: (Opcional) Soportar tema oscuro
8. **i18n**: (Futuro) Preparar para internacionalización (español/inglés)

---

## ESTRUCTURA DE CARPETAS SUGERIDA

```
src/
├── assets/           # Imágenes, iconos
├── components/       # Componentes reutilizables
│   ├── common/       # Modals, Buttons, etc.
│   ├── lectura/      # LecturaCard, PreguntaForm
│   ├── admin/        # AdminTable, AdminCard
│   └── layout/       # Sidebar, TopBar, Footer
├── views/            # Páginas (frames)
│   ├── auth/         # Login, Register, Callback
│   ├── estudiante/   # Dashboard, Lecturas, Sesiones, etc.
│   └── admin/        # AdminDashboard, AdminUsuarios, etc.
├── layouts/          # AppLayout, AdminLayout, AuthLayout
├── router/           # Vue Router config
├── stores/           # Pinia stores
├── services/         # API service (axios)
│   ├── api.js        # Axios instance con interceptors
│   ├── authService.js
│   ├── lecturaService.js
│   └── ...
├── utils/            # Helpers, formatters
└── composables/      # Custom hooks (useAuth, usePagination)
```

---

## GENERACIÓN CON IA: INSTRUCCIONES FINALES

1. Genera cada frame como componente Vue 3 Composition API
2. Usa `<script setup>` syntax
3. Tailwind CSS para estilos (clases utility)
4. Axios para llamadas API (interceptors para JWT)
5. Pinia para state management
6. Vue Router con guards de autenticación
7. Validación con Vuelidate o VeeValidate
8. Toasts con vue-toastification
9. Iconos con Heroicons o Lucide Vue
10. NO olvides ningún frame mencionado arriba
11. Mantén consistencia en topbar/sidebar según layout
12. Implementa loading states y error handling en todos los fetch
13. Respeta los roles (ESTUDIANTE vs ADMIN) en guards
14. Usa la paleta de colores sugerida
15. Haz todas las pantallas responsive (mobile-first)

**¡LISTO PARA GENERAR!**
