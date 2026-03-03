# HackaEdu — Plataforma Inteligente de Lectura en Inglés con IA

<p align="center">

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-REST_API-AA4400?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)

![Vue.js](https://img.shields.io/badge/Vue-3.5-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-State_Management-FFD859?style=for-the-badge)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

![LangChain](https://img.shields.io/badge/LangChain-LLM_Orchestration-1F51C2?style=for-the-badge)

![JWT](https://img.shields.io/badge/JWT-Stateless_Auth-000000?style=for-the-badge)

</p>

---

## 📌 Descripción

HackaEdu es una plataforma web educativa que genera automáticamente lecturas personalizadas en inglés con evaluaciones adaptativas usando IA.

Combina:

- Generación estructurada de contenido con LLM
- Evaluación multidimensional basada en criterios
- Sistema de progresión CEFR (A1–C2)
- Gamificación y ranking competitivo
- Arquitectura backend desacoplada y escalable

El proyecto fue desarrollado como un **MVP intensivo con enfoque en arquitectura sólida e integración robusta de LLM**.

---

# 🎯 Problema

Las plataformas tradicionales de aprendizaje de inglés presentan limitaciones claras:

- Contenido genérico no adaptado al nivel real del estudiante  
- Evaluaciones superficiales (solo score final)  
- Falta de análisis por habilidad específica  
- Baja personalización y engagement  
- Costos altos para generar contenido educativo escalable  

---

# 💡 Solución

HackaEdu aborda estos desafíos mediante:

## 1️⃣ Generación estructurada con IA

- Motor LLM con validación estricta usando Pydantic  
- Lecturas generadas por nivel CEFR  
- Preguntas asociadas a criterios específicos de evaluación  
- Persistencia transaccional en base de datos  

## 2️⃣ Evaluación multidimensional

Cada sesión evalúa:

- Comprensión general  
- Detalles específicos  
- Vocabulario en contexto  
- Inferencia  
- Gramática  
- Análisis crítico  

Se almacena puntuación por criterio y se calcula dominio progresivo.

## 3️⃣ Sistema de progresión inteligente

- 6 niveles CEFR (A1 → C2)  
- Puntos en nivel (progreso interno)  
- Puntos acumulativos (ranking global)  
- Ascenso basado en dominio real de habilidades  

## 4️⃣ Gamificación

- Logros y badges  
- Rachas diarias  
- Leaderboard segmentado  
- Dashboard con métricas claras  

---

# 🏗 Arquitectura Técnica

## Backend

- Django 5.2  
- Django REST Framework  
- JWT stateless authentication  
- PostgreSQL (producción)  
- SQLite (desarrollo)  
- Integración LLM con LangChain + Ollama  

### Arquitectura general

```
Frontend (Vue 3 SPA)
        ↓
REST API (DRF + JWT)
        ↓
Apps Django desacopladas
        ↓
PostgreSQL
```

Se priorizó:

- Modelado relacional sólido  
- Separación de responsabilidades  
- Selectors para lógica compleja  
- Transacciones atómicas en generación IA  

---

## Frontend

- Vue 3 (Composition API)  
- Vite  
- Pinia (estado global)  
- Vue Router  
- TailwindCSS  

Enfoque:

- SPA reactiva  
- Mobile-first  
- Separación por servicios API  
- Arquitectura modular y escalable  

---

# 🧠 Pipeline LLM

```
Input usuario (nivel, categoría)
    ↓
Prompt estructurado (Few-shot)
    ↓
ChatOllama (qwen2.5:3b local)
    ↓
Validación Pydantic v2
    ↓
Persistencia atómica en DB
```

### Decisiones clave

- LLM local → evita costos API  
- Validación estructurada → evita inconsistencias  
- Retry controlado ante fallos de JSON  
- Servicio LLM desacoplado del resto del sistema  

---

# ⚙️ Funcionalidades Principales

- Registro y login (email + Google OAuth)  
- Generación automática de lecturas por nivel  
- Test interactivo con límite de tiempo  
- Análisis por criterio  
- Recomendaciones IA  
- Dashboard con progreso visual  
- Sistema de logros  
- Ranking global  
- Ascenso automático de nivel  

---

# 🚧 Retos Técnicos Resueltos

## Validación de salida LLM

Problema: respuestas no estructuradas.  
Solución: Pydantic + validadores + retry controlado.

## Escalabilidad de criterios

Problema: modelo simple no soportaba múltiples habilidades.  
Solución: sistema dinámico por nivel + almacenamiento JSON estructurado.

## Rendimiento dashboard

Problema: consultas con múltiples relaciones.  
Solución: `select_related`, `prefetch_related`, selectors optimizados.

## Autenticación multi-provider

Email + Google OAuth integrados sobre CustomUser sin romper modelo relacional.

---

# 📸 Capturas de Pantalla

## Login
![Login](./docs/login.webp)

## Dashboard
![Dashboard](./docs/dashboard.webp)

## Generación de Lectura con IA
![Generación](./docs/formularioDeGeneracion.webp)

## Test Interactivo
![Test](./docs/testLecture.webp)

## Resultados y Análisis
![Resultados](./docs/testCalificado.webp)

## Ranking Global
![Ranking](./docs/ranking.webp)

---

# 🛠 Instalación y Setup

## Requisitos

- Python 3.10+  
- Node 18+  
- PostgreSQL 15  
- Ollama con modelo `qwen2.5:3b`  

---

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Variables de entorno (.env)

```env
DEBUG=True
SECRET_KEY=your-secret
DATABASE_URL=postgresql://user:password@localhost:5432/hackaEdu
LLM_MODEL_NAME=qwen2.5:3b
```

### Migraciones

```bash
python manage.py migrate
```

### Inicialización

```bash
python manage.py shell < scripts/init/initialize_data.py
```

### Ejecutar servidor

```bash
python manage.py runserver
```

Backend disponible en: http://localhost:8000

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en: http://localhost:5173

---



# 🧠 Aprendizajes Clave

- Modelado relacional sólido reduce deuda técnica futura  
- Validación estructurada es esencial en sistemas LLM  
- Separar progreso interno de ranking público evita manipulación  
- JWT stateless facilita escalabilidad  
- Documentar decisiones técnicas mejora mantenibilidad  

---

# 👨‍💻 Enfoque Profesional

Este proyecto demuestra:

- Arquitectura backend escalable con Django  
- Integración moderna de LLM con validación robusta  
- Modelado de dominio complejo (educación + progresión)  
- Diseño de sistemas gamificados  
- Integración frontend/backend desacoplada  
- Enfoque en mantenibilidad y claridad estructural  

---

## 📬 Contacto

- Email: [tu-email]
- LinkedIn: [tu-linkedin]