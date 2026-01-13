# 📚 Arquitectura HackaEdu - Sistema de Aprendizaje de Inglés

## 🎯 Visión General

**HackaEdu** es una plataforma educativa para mejorar comprensión lectora en inglés usando marcos CEFR (A1-C2), con integración de IA para generación de contenido y recomendaciones personalizadas.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Vue.js + Vite)                     │
│  - Dashboard Estudiante   - Dashboard Profesor   - Admin Panel   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP/REST + WebSocket
┌──────────────────────▼──────────────────────────────────────────┐
│                   Backend API (Django REST)                      │
│  Port: 8000                                                       │
│  ├─ /auth         → Autenticación (registro, login)             │
│  ├─ /lecturas     → Lecturas, sesiones, respuestas              │
│  ├─ /ia           → Generación de contenido                     │
│  └─ /admin        → Panel administrativo                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │ SQLAlchemy + Django ORM
┌──────────────────────▼──────────────────────────────────────────┐
│                  Database (PostgreSQL)                            │
│  - Catálogos         - Usuarios    - Sesiones   - Logros         │
│  - Progresión        - Análisis    - Historial IA               │
└─────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│              External Services                                   │
│  ├─ Anthropic Claude API → Generación de contenido              │
│  ├─ AWS S3 / GCS        → Almacenamiento de archivos            │
│  └─ Email Service       → Notificaciones                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitectura de Capas

### 1. **Presentation Layer** (Frontend)
```
vue.js + Vite
├── /src
│   ├── views/
│   │   ├── Home.vue              → Página de inicio
│   │   ├── auth/                 → Login, Registro
│   │   ├── student/              → Dashboard estudiante
│   │   └── teacher/              → Dashboard profesor
│   ├── components/               → Componentes reutilizables
│   ├── router/                   → Rutas
│   └── core/                     → Configuración
└── API Calls via Axios/Fetch
```

### 2. **API Layer** (Django REST Framework)
```
Endpoints REST
├── Stateless
├── Token Authentication
├── Rate Limiting
└── CORS Enabled
```

### 3. **Business Logic Layer** (Services)
```
Services
├── AnalisysService              → Análisis de progreso
├── IntegracionIAService         → Claude API integration
├── ProgresionService            → Lógica de ascenso
└── RecommendationService        → Recomendaciones
```

### 4. **Data Access Layer** (Models + ORM)
```
Django ORM
├── 13 Modelos
├── Relationships definidas
├── Validaciones
└── Business Logic en métodos
```

### 5. **Database Layer** (PostgreSQL)
```
PostgreSQL 15+
├── 13 Tablas
├── Índices
├── Foreign Keys
└── Constraints
```

---

## 📊 Modelos de Datos (13 Tablas)

### Catálogos (Lookups)
```
NivelCEFR (6 registros)
├── id: 1-6
├── codigo: A1, A2, B1, B2, C1, C2
├── nombre: Beginner, Elementary, etc.
├── cantidad_preguntas: 7, 8, 10, 13, 15, 15
├── lecturas_para_ascender: 5, 8, 10, 12, 15, mastery
├── promedio_requerido: 80%, 75%, 75%, 70%, 70%, 70%
└── distribucion_criterios: JSON con pesos de skills

CriterioHabilidad (8 registros)
├── VOCAB_BASICO (peso: 2)
├── VOCAB_IDIOMS (peso: 2)
├── GRAMMAR_PRESENT (peso: 1)
├── GRAMMAR_PAST (peso: 1)
├── GRAMMAR_CONDITIONAL (peso: 1)
├── READING_COMPREHENSION (peso: 2)
├── INFERENCE (peso: 1)
└── READING_SPEED (peso: 1)

Categoria (4+ registros)
├── Naturaleza
├── Tecnología
├── Cultura
└── Deporte

Modalidad (4 registros)
├── IA_GENERAR: Contenido generado por Claude
├── MANUAL: Cargado por admin
├── API_NEWS: De API de noticias
└── PERSONALIZADA: Creado por profesor
```

### Usuarios y Autenticación
```
Usuario (extends AbstractUser)
├── username: Único
├── email: Único
├── password: Hasheado
├── first_name, last_name
├── rol: ESTUDIANTE | ADMIN
├── nivel_cefr: FK a NivelCEFR
├── puntos_totales: INT
├── lecturas_completadas: INT
├── esta_activo: BOOLEAN
└── RelatedManager: Token (autenticación)

Token (Django Built-in)
├── key: Token único
└── user: FK a Usuario
```

### Progresión
```
ProgresionNivel (One-to-One con Usuario)
├── usuario: FK
├── nivel_actual: FK a NivelCEFR
├── lecturas_completadas_en_nivel: INT
├── promedio_nivel: FLOAT
├── puntos_en_nivel: INT
├── intentos_ascenso: INT
├── esta_preparado_ascenso: BOOLEAN
├── fecha_ultimo_ascenso: DATETIME
├── fecha_actualizacion: DATETIME

Métodos:
├── verificar_ascenso()  → Verifica si cumple criterios
├── aceptar_ascenso()    → Promueve usuario
└── reset_nivel_stats()  → Reinicia stats para nuevo nivel
```

### Contenido
```
Lectura
├── titulo: VARCHAR
├── contenido: TEXT
├── nivel: FK a NivelCEFR
├── categoria: FK a Categoria
├── modalidad: FK a Modalidad
├── autor_ia_usado: VARCHAR (si fue generado)
├── cantidad_palabras: INT
├── duracion_minutos_promedio: INT
├── archivo_url: VARCHAR (PDF/TXT)
├── interes_tags: JSON (["Naturaleza", "Animales"])
├── fecha_creacion: DATETIME
└── fecha_actualizacion: DATETIME

Pregunta (5 tipos)
├── lectura: FK
├── numero: INT (1-15)
├── texto: TEXT
├── tipo: MULTIPLE_CHOICE | COMPLETAR | VERDADERO_FALSO | RESPUESTA_CORTA | ENSAYO
├── criterio: FK a CriterioHabilidad
├── dificultad: FACIL | MEDIA | DIFICIL
├── opciones_json: JSON (para MC)
├── respuesta_correcta: VARCHAR
├── respuesta_correcta_json: JSON
└── explicacion: TEXT
```

### Sesiones y Respuestas
```
Sesion
├── usuario: FK a Usuario
├── lectura: FK a Lectura
├── nivel: FK a NivelCEFR (nivel en que se tomó)
├── estado: INICIADA | EN_PROGRESO | COMPLETADA | ABANDONADA
├── fecha_inicio: DATETIME
├── fecha_fin: DATETIME
├── duracion_minutos: INT
├── puntaje_total: FLOAT (0-100)
├── puntajes_por_criterio: JSON
  {
    "VOCAB_BASICO": 85,
    "READING_COMPREHENSION": 90,
    ...
  }
├── tiempo_total_segundos: INT
└── notas: TEXT

Respuesta
├── sesion: FK a Sesion
├── pregunta: FK a Pregunta
├── respuesta_usuario: VARCHAR
├── es_correcta: BOOLEAN
├── puntos_obtenidos: FLOAT
├── tiempo_respuesta_segundos: INT
└── fecha_respuesta: DATETIME
```

### Análisis
```
DesempenoCriterio
├── usuario: FK a Usuario
├── criterio: FK a CriterioHabilidad
├── porcentaje_promedio: FLOAT (0-100)
├── respuestas_correctas: INT
├── respuestas_totales: INT
├── ultima_actualizacion: DATETIME
└── tendencia: MEJORANDO | ESTABLE | EMPEORANDO

Logro
├── nombre: VARCHAR
├── tipo: BADGE | MILESTONE | ACHIEVEMENT
├── descripcion: TEXT
├── icono_url: VARCHAR
├── criterio_desbloques: JSON
└── fecha_creacion: DATETIME

LogroUsuario
├── usuario: FK a Usuario
├── logro: FK a Logro
├── fecha_obtenido: DATETIME
└── notificacion_enviada: BOOLEAN
```

### IA Integration
```
IAPromptTemplate
├── nombre: VARCHAR único
├── tipo: GENERAR_LECTURA | GENERAR_PREGUNTAS | etc.
├── modelo: CLAUDE_3_HAIKU | CLAUDE_3_SONNET
├── template_texto: TEXT (con {placeholders})
├── parametros_json: JSON (temperatura, max_tokens)
├── activo: BOOLEAN
└── fecha_creacion: DATETIME

GeneratedContent
├── prompt_template: FK a IAPromptTemplate
├── usuario: FK a Usuario
├── contenido_original: TEXT (input)
├── contenido_generado: TEXT (output)
├── tipo_contenido: LECTURA | PREGUNTAS | RECOMENDACIONES
├── modelo_ia: VARCHAR
├── tokens_usados: INT
├── costo_usd: DECIMAL
├── es_utilizado: BOOLEAN
├── feedback_usuario: TEXT
└── fecha_generacion: DATETIME

IAHistory (Auditoría)
├── usuario: FK a Usuario
├── tipo_llamada: VARCHAR
├── modelo: VARCHAR
├── prompt: TEXT
├── respuesta_ia: TEXT
├── tokens_usados: INT
├── costo_usd: DECIMAL
├── tiempo_respuesta_ms: INT
├── exitosa: BOOLEAN
├── error_mensaje: TEXT
└── fecha_llamada: DATETIME
```

---

## 🔄 Flujos Principales

### 1. Registro y Login

```
┌─────────────────────────────────────────────────────┐
│  Usuario accede a /registro en frontend             │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  POST /api/v1/auth/registro/                        │
│  {username, email, password, nivel_cefr}           │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │ UsuarioRegistroSerializer│
        │   - Valida campos        │
        │   - Hashea password      │
        └────────────┬─────────────┘
                     │
        ┌────────────▼────────────────────────────┐
        │ Usuario.objects.create_user()           │
        │ ✅ Crea en tabla Usuario               │
        └────────────┬────────────────────────────┘
                     │
        ┌────────────▼────────────────────────────┐
        │ Token.objects.create(user=usuario)      │
        │ ✅ Crea token de autenticación         │
        └────────────┬────────────────────────────┘
                     │
        ┌────────────▼────────────────────────────┐
        │ ProgresionNivel.objects.create(usuario)│
        │ ✅ Inicializa progresión en A1         │
        └────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Retorna: {token, usuario}                          │
│  Frontend guarda token en localStorage              │
└─────────────────────────────────────────────────────┘
```

### 2. Lectura de Contenido

```
┌──────────────────────────────────────┐
│  GET /api/v1/lecturas/lecturas/      │
│  Mostrar lecturas del nivel de user   │
└────────────┬─────────────────────────┘
             │
┌────────────▼──────────────────────────────────┐
│  LecturaViewSet.list()                       │
│  - Filtra por nivel_cefr del usuario         │
│  - Usa LecturaListSerializer                 │
└────────────┬──────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────┐
│  Usuario elige lectura y hace click           │
│  POST /api/v1/lecturas/lecturas/{id}/         │
│       iniciar_sesion/                         │
└────────────┬───────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Sesion.objects.create()                       │
│  - Crea registro de sesión                     │
│  - Estado: INICIADA                           │
│  - Obtiene preguntas asociadas a la lectura   │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Retorna: {sesion, preguntas, lectura}         │
│  Frontend muestra lectura + preguntas          │
└─────────────────────────────────────────────────┘
```

### 3. Responder Preguntas

```
┌──────────────────────────────────────┐
│  Usuario responde pregunta            │
│  POST /api/v1/lecturas/sesiones/{id}/│
│      responder/                       │
│  {pregunta_id, respuesta_usuario}     │
└────────────┬─────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  SesionViewSet.responder()                     │
│  1. Validar respuesta vs correcta              │
│  2. Calcular puntos                            │
│  3. Actualizar criterio habilidad              │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Respuesta.objects.create()                    │
│  - Registra respuesta usuario                  │
│  - Calcula es_correcta                         │
│  - Almacena puntos_obtenidos                   │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  DesempenoCriterio.update()                    │
│  - Actualiza porcentaje_promedio del criterio  │
│  - Recalcula tendencia (MEJORANDO|ESTABLE|etc)│
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Si todas respondidas:                         │
│  1. Sesion.calcular_puntajes_por_criterio()   │
│  2. Actualizar Sesion.estado = COMPLETADA      │
│  3. Usuario.puntos_totales += puntaje          │
│  4. Usuario.lecturas_completadas += 1          │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  AnalisysService.actualizar_progresion()       │
│  - Verifica ProgresionNivel.verificar_ascenso()│
│  - Si preparado_ascenso = True:                │
│    - Notifica al usuario                       │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Retorna: {sesion_actualizada, stats}          │
│  Frontend muestra resultados y opciones        │
└─────────────────────────────────────────────────┘
```

### 4. Ascenso de Nivel (Option 2: Automático)

```
┌──────────────────────────────────────┐
│  Sistema detecta cumplimiento de      │
│  criterios de ascenso para usuario    │
└────────────┬─────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  ProgresionNivel.verificar_ascenso()            │
│  Valida:                                        │
│  1. lecturas_completadas >= requeridas (5,8,10)│
│  2. promedio_nivel >= % mínimo (80,75,70)      │
│  3. promedio en todos los criterios            │
└────────────┬────────────────────────────────────┘
             │
        ┌────NO────┐
        │          │
        │      Retorna False
        │      Usuario sigue en nivel
        │
        │
        SÍ
        │
┌───────▼──────────────────────────────────────┐
│  ProgresionNivel.esta_preparado_ascenso=True │
│  Envía notificación a usuario                 │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Usuario ve notificación en frontend            │
│  "🎉 ¡Ya estás listo para ascender!"           │
│  Botón: Aceptar Ascenso                        │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  POST /api/v1/auth/usuarios/aceptar_ascenso/   │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  ProgresionNivel.aceptar_ascenso()              │
│  Transacción:                                   │
│  1. nivel_actual = siguiente_nivel              │
│  2. lecturas_completadas_en_nivel = 0           │
│  3. promedio_nivel = 0                          │
│  4. puntos_en_nivel = 0                         │
│  5. LogroUsuario.create(logro=ascenso)          │
│  6. Usuario.nivel_cefr = nuevo_nivel            │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  Retorna: {exito, nuevo_nivel, mensaje}         │
│  Frontend redirige a dashboard actualizado      │
└─────────────────────────────────────────────────┘
```

### 5. Generación de Contenido con IA

```
┌────────────────────────────────────────────┐
│  Usuario quiere lectura personalizada       │
│  POST /api/v1/ia/generar/generar_lectura/  │
│  {tema: "Animales", nivel: "A1"}            │
└─────────────┬──────────────────────────────┘
              │
┌─────────────▼──────────────────────────────┐
│  IntegracionIAService.generar_lectura()    │
│  1. Obtener IAPromptTemplate                │
│  2. Construir prompt con variables          │
│  3. Llamar a Anthropic Claude API           │
└─────────────┬──────────────────────────────┘
              │
┌─────────────▼──────────────────────────────┐
│  client.messages.create()                  │
│  Envía prompt a Claude                     │
│  Espera respuesta                          │
└─────────────┬──────────────────────────────┘
              │
    ┌─────────▼─────────┐
    │ ¿Éxito?           │
    │ SÍ        │ NO    │
    │          │        │
    │       Error!
    │       Registra en IAHistory
    │       Retorna error
    │
    SÍ
    │
┌───▼─────────────────────────────────────┐
│  Procesar respuesta de Claude            │
│  - Extraer contenido generado            │
│  - Contar tokens (input + output)        │
│  - Calcular costo (USD)                  │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  GeneratedContent.objects.create()      │
│  - Registra contenido generado          │
│  - Almacena tokens y costo              │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  IAHistory.objects.create()             │
│  - Auditoría de llamada a IA            │
│  - Registra tokens, tiempo, costo       │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  Retorna: {                             │
│    contenido: "The amazing...",         │
│    tokens_usados: 342,                  │
│    costo_usd: 0.004,                    │
│    tiempo_ms: 1850                      │
│  }                                      │
└─────────────────────────────────────────┘
```

---

## 🔐 Autenticación y Permisos

```
Token-based Authentication
├── Cliente envía token en header:
│   Authorization: Token abc123def456...
│
├── Middleware verifica token
├── Obtiene usuario asociado
└── Establece request.user

Permisos (permission_classes)
├── AllowAny           → /auth/registro/, /auth/login/
├── IsAuthenticated    → Todas las demás
└── Custom Permissions → (para futuro)

Roles de Usuario
├── ESTUDIANTE
│   ├── Ver solo sus propias sesiones
│   ├── Ver solo su perfil
│   └── Ver lecturas de su nivel
│
└── ADMIN
    ├── Ver/editar todos los usuarios
    ├── Crear/editar lecturas
    ├── Ver estadísticas globales
    └── Acceso a admin panel
```

---

## 📈 Escalabilidad

### Optimizaciones Actuales
- ✅ Query optimization con select_related, prefetch_related
- ✅ Pagination de resultados
- ✅ Caching de tokens
- ✅ Índices de base de datos

### Mejoras Futuras
- [ ] Redis para caching
- [ ] Elastic Search para búsqueda
- [ ] Message Queue (Celery) para tareas async
- [ ] CDN para static files
- [ ] Rate limiting avanzado
- [ ] Microservicios (IA en servicio separado)

---

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Docker
```bash
docker-compose up -d
```

### Production (Gunicorn + Nginx)
```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 hackaEdu.wsgi:application
```

---

## 📊 Métricas Importantes

### Por Usuario
- Nivel CEFR actual
- Puntos totales
- Lecturas completadas
- Promedio por criterio
- Logros desbloqueados
- Progreso hacia siguiente nivel

### Por Nivel
- Promedio de puntos
- Distribución de criterios
- Cantidad de preguntas (7-15)
- Lecturas necesarias para ascender (5-15)
- Promedio requerido (70-80%)

### Por Sistema
- Total usuarios
- Sesiones completadas
- Contenido generado con IA
- Costo total de IA
- Criterio más débil a nivel sistema

---

## 🔄 Diagrama de Estados de Sesión

```
         ┌─────────┐
         │ INICIADA│
         └────┬────┘
              │ Usuario comienza a responder
              │
         ┌────▼─────────┐
         │EN_PROGRESO    │
         └────┬──────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    │    Completa    Abandona
    │         │         │
┌───▼──┐  ┌───▼──┐     │
│COMP. │  │ABANDONADA │
│TADA  │  │        │
└──────┘  └────────┘
    │
    │ Cálculos + Actualizaciones
    │
    ▼
Registra sesión, actualiza stats,
verifica ascenso
```

---

## 📝 Conclusión

HackaEdu es una plataforma educativa moderna y escalable que combina:
- ✅ Estructura de datos robusta (CEFR + 8 skills)
- ✅ Progresión automática e inteligente
- ✅ Integración con Claude AI para contenido generado
- ✅ API RESTful completa
- ✅ Admin panel Django completo
- ✅ Recomendaciones personalizadas
- ✅ Análisis detallado de progreso

**Total: 13 tablas, 7 ViewSets, 13 Serializers, Servicios de negocio, Integración IA.**
