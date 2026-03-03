# 🎨 Frontend - Documentación Técnica

HackaEdu Frontend es una **Single Page Application (SPA)** moderna construida con **Vue 3 + Vite + Tailwind CSS**.

---

## 📋 Contenido

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Stack Tecnológico](#stack-tecnológico)
- [Componentes y Vistas](#componentes-y-vistas)
- [Servicios API](#servicios-api)
- [Estado Global (Pinia)](#estado-global-pinia)
- [Enrutamiento](#enrutamiento)
- [Guía de Desarrollo](#guía-de-desarrollo)
- [Build y Deploy](#build-y-deploy)

---

## 📁 Estructura del Proyecto

```
fronted-cooMaestro/
├── package.json              # Dependencias + scripts npm
├── vite.config.js           # Configuración Vite (bundler)
├── tailwind.config.js       # Configuración Tailwind CSS
├── postcss.config.js        # PostCSS para Tailwind
│
├── public/                  # Assets estáticos
│   └── google-oauth-test.html
│
└── src/
    ├── App.vue              # Componente raíz
    ├── main.js              # Entry point
    ├── style.css            # Estilos globales
    │
    ├── assets/              # Imágenes, iconos
    ├── lib/                 # Utilidades compartidas
    │
    ├── router/              # Vue Router
    │   └── index.js         # Definición de rutas
    │
    ├── stores/              # Estado global (Pinia)
    │   ├── auth.js          # Auth y usuario
    │   ├── dashboard.js     # Dashboard
    │   └── settings.js      # Configuración app
    │
    ├── services/            # Llamadas API REST
    │   ├── auth.service.js          # GET/POST /auth/*
    │   ├── dashboard.service.js     # GET /usuarios/dashboard/*
    │   ├── lectures.service.js      # GET/POST /lecturas/*
    │   ├── llm.service.js           # POST /lecturas/generar/*
    │   ├── evaluacion.service.js    # POST/PUT /sesiones/*
    │   ├── achievements.service.js  # GET /logros/*
    │   ├── ranking.service.js       # GET /ranking/*
    │   ├── categories.service.js    # GET /categorias/*
    │   └── modalidades.service.js   # GET /modalidades/*
    │
    ├── components/          # Componentes reutilizables
    │   ├── Navbar.vue
    │   ├── Sidebar.vue
    │   ├── LoadingSpinner.vue
    │   ├── Card.vue
    │   ├── Button.vue
    │   └── ...
    │
    └── views/              # Páginas principales
        ├── HomePage.vue
        ├── LoginPage.vue
        ├── RegisterPage.vue
        ├── Dashboard.vue
        ├── LecturePage.vue
        ├── AllLecturesPage.vue
        ├── AchievementsPage.vue
        ├── RankingPage.vue
        ├── LogoutPage.vue
        └── NotFoundPage.vue
```

---

## 🛠️ Stack Tecnológico

| Herramienta | Versión | Propósito |
|-------------|---------|----------|
| **Vue** | 3.5.24 | Framework SPA reactivo |
| **Vite** | 7.2.4 | Bundler ultra rápido (HMR ~100ms) |
| **Vue Router** | 5.0.3 | Enrutamiento client-side |
| **Pinia** | 3.0.4 | State management (Vuex moderno) |
| **Axios** | 1.13.5 | Cliente HTTP |
| **Tailwind CSS** | 3.4.19 | Utility-first CSS framework |
| **Marked** | 17.0.3 | Parser Markdown (para contenido) |

### ¿Por qué estas tecnologías?

**Vue 3 Composition API**
- Mejor organización que Options API
- Reactividad moderna con `ref()` y `reactive()`
- Mejor para equipo junior

**Vite**
- ⚡ HMR: cambios en código reflejan al instante (~100ms)
- 📦 Build optimizado (tree-shaking, code splitting)
- 🚀 Fast refresh sin full reload

**Pinia**
- 🧹 Alternativa moderna a Vuex
- 📝 Sintaxis clara y TypeScript-friendly (aunque usamos JS)
- 🔧 DevTools integradas

**Tailwind CSS**
- 🎨 Utility-first: `<div class="flex bg-blue-500">` = menos CSS
- 📦 Solo CSS usado en producción (tree-purged)
- 🎯 Consistent design system incluido

---

## 🚀 Guía de Desarrollo

### Setup Local

```bash
# 1. Navegar a frontend
cd fronted-cooMaestro

# 2. Instalar dependencias
npm install

# 3. Crear .env.local
cat > .env.local << EOF
VITE_API_URL=http://localhost:8000
VITE_API_VERSION=v1
VITE_APP_TITLE=HackaEdu
EOF

# 4. Iniciar servidor dev
npm run dev
# Abre http://localhost:5173
```

### Build para Producción

```bash
# Generar dist/ optimizado
npm run build

# Vista previa de build
npm run preview
```

---

## 📖 Recursos

- [Vue 3 Docs](https://vuejs.org/)
- [Vite Docs](https://vitejs.dev/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios](https://axios-http.com/)

---

**Última actualización**: Marzo 2026
