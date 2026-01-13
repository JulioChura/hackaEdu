# 🚀 INICIO RÁPIDO - HackaEdu Backend

## ¡Implementación Completada! ✅

El backend de **HackaEdu** está **completamente implementado** y listo para ejecutar.

---

## 📦 Qué se Implementó

### ✅ Backend Completo (Django REST Framework)
- **3 Apps Principales:**
  - `auth/` → Autenticación, usuarios, roles
  - `lecturas/` → Contenido, sesiones, progresión
  - `ia/` → Integración con Claude API

- **13 Modelos de BD:**
  - Catálogos (Niveles CEFR, Criterios, Categorías, Modalidades)
  - Usuarios (Custom AbstractUser con roles)
  - Contenido (Lecturas, Preguntas)
  - Sesiones (Respuestas, Análisis)
  - IA (Prompts, Histórico, Contenido generado)

- **7 ViewSets con Endpoints:**
  - AuthViewSet (registro, login)
  - UsuarioViewSet (perfil, progresión, ascenso)
  - LecturaViewSet (listar, crear, iniciar sesión)
  - SesionViewSet (responder preguntas, calcular puntajes)
  - RankingViewSet (top usuarios, por nivel)
  - EstadisticasViewSet (análisis de progreso)
  - IA Integration (generar contenido)

- **Servicios de Negocio:**
  - AnalisysService → Análisis de progreso y recomendaciones
  - IntegracionIAService → Integración con Claude API
  - ProgresionNivel → Lógica de ascenso automático

- **Admin Django Completo:**
  - Panel administrativo para gestionar todo
  - Usuarios, lecturas, sesiones, logros

- **Documentación y DevOps:**
  - Docker y docker-compose configurados
  - Scripts de setup (Windows + Unix)
  - README con instrucciones completas
  - Documentación de arquitectura

---

## 🚀 Cómo Ejecutar

### Opción 1: Docker (MÁS FÁCIL) 🐳

```bash
# Desde la raíz del proyecto
cd backend

# Iniciar servicios (PostgreSQL + Django + pgAdmin)
docker-compose up -d

# Esperar 30 segundos a que arrange todo
sleep 30

# Verificar que todo está corriendo
docker-compose ps

# Ver logs
docker-compose logs -f web

# Acceso:
# - API: http://localhost:8000/api/v1/
# - Admin: http://localhost:8000/admin/
# - PgAdmin: http://localhost:5050/
```

**Credenciales por defecto:**
- Admin: `admin` / `admin123`
- PgAdmin: `admin@example.com` / `admin`

### Opción 2: Local Sin Docker

#### Windows
```cmd
cd backend\hackaEdu
setup.bat
python manage.py runserver
```

#### Unix (Mac/Linux)
```bash
cd backend/hackaEdu
bash setup.sh
python manage.py runserver
```

---

## 📊 Primer Test de API

### 1. Registro de Usuario
```bash
curl -X POST http://localhost:8000/api/v1/auth/registro/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456!",
    "password2": "Test123456!",
    "first_name": "Test",
    "nivel_cefr": 1
  }'
```

Respuesta:
```json
{
  "token": "abc123def456...",
  "usuario": {
    "id": 2,
    "username": "testuser",
    "email": "test@example.com",
    "rol": "ESTUDIANTE",
    "nivel_cefr": "A1"
  }
}
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456!"
  }'
```

### 3. Obtener Mi Perfil
```bash
curl -X GET http://localhost:8000/api/v1/auth/usuarios/me/ \
  -H "Authorization: Token abc123def456..."
```

### 4. Listar Lecturas
```bash
curl -X GET http://localhost:8000/api/v1/lecturas/lecturas/ \
  -H "Authorization: Token abc123def456..."
```

### 5. Generar Lectura con IA
```bash
curl -X POST http://localhost:8000/api/v1/ia/generar/generar_lectura/ \
  -H "Authorization: Token abc123def456..." \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Animales salvajes",
    "nivel": "A1",
    "interes": "Naturaleza",
    "cantidad_palabras": 300
  }'
```

---

## 📁 Estructura de Archivos Clave

```
backend/
├── hackaEdu/              # Proyecto Django
│   ├── auth/              # App autenticación
│   │   ├── models.py      # Usuario custom
│   │   ├── views.py       # ViewSets de auth
│   │   ├── serializers.py # Serializers
│   │   ├── urls.py        # URLs
│   │   └── admin.py       # Admin panel
│   │
│   ├── lecturas/          # App principal
│   │   ├── models.py      # 13 modelos
│   │   ├── views.py       # 7 ViewSets
│   │   ├── serializers.py # 13 serializers
│   │   ├── services.py    # Lógica de negocio
│   │   ├── urls.py        # URLs
│   │   ├── admin.py       # Admin panel
│   │   └── management/commands/
│   │       └── seed_data.py  # Datos iniciales
│   │
│   ├── ia/                # App IA
│   │   ├── models.py      # IAPromptTemplate, etc
│   │   ├── views.py       # ViewSets IA
│   │   ├── serializers.py # Serializers
│   │   ├── services.py    # IntegracionIAService
│   │   ├── urls.py        # URLs
│   │   └── admin.py       # Admin panel
│   │
│   ├── hackaEdu/          # Configuración
│   │   ├── settings.py    # ✅ CONFIGURADO
│   │   ├── urls.py        # ✅ CONFIGURADO
│   │   ├── wsgi.py        # WSGI
│   │   └── asgi.py        # ASGI
│   │
│   ├── requirements.txt   # ✅ ACTUALIZADO
│   ├── manage.py          # CLI de Django
│   ├── Dockerfile         # ✅ CREADO
│   ├── README_BACKEND.md  # ✅ Documentación
│   └── test_api.py        # ✅ Testing script
│
├── docker-compose.yml     # ✅ CREADO
├── .env.example           # ✅ TEMPLATE
├── ARQUITECTURA.md        # ✅ Documentación completa
└── CHECKLIST.md           # ✅ Plan de implementación
```

---

## ⚙️ Variables de Entorno

Crear archivo `.env` en `backend/`:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Para PostgreSQL (con Docker):
# DATABASE_URL=postgresql://hackaEdu_user:hackaEdu_pass@db:5432/hackaEdu

# Anthropic Claude (opcional)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# IA
MODO_IA=SIMPLE
# Cambiar a IA_AVANZADA para usar Claude
```

---

## 🗄️ Base de Datos

### Migraciones
```bash
python manage.py makemigrations  # Crear migraciones
python manage.py migrate          # Aplicar migraciones
```

### Datos Iniciales
```bash
python manage.py seed_data
```

Esto crea:
- ✅ 6 niveles CEFR (A1-C2)
- ✅ 8 criterios de habilidad
- ✅ 4 categorías
- ✅ 4 modalidades
- ✅ 8 logros
- ✅ Usuario admin: `admin` / `admin123`
- ✅ 2 lecturas de ejemplo

### Ver Base de Datos
```bash
# SQLite (desarrollo)
sqlite3 db.sqlite3

# PostgreSQL (con Docker)
docker exec -it hackaEdu-db psql -U hackaEdu_user -d hackaEdu

# PgAdmin Web
http://localhost:5050/
```

---

## 🧪 Testing

### Test API Automático
```bash
python test_api.py
```

Esto testea:
1. ✅ Registro de usuario
2. ✅ Login
3. ✅ Perfil
4. ✅ Progresión
5. ✅ Listado de lecturas
6. ✅ Estadísticas

### Tests Unitarios
```bash
python manage.py test auth.tests
python manage.py test lecturas.tests
```

---

## 📚 API Endpoints Completos

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/registro/` | Registrar nuevo usuario |
| POST | `/api/v1/auth/login/` | Iniciar sesión |

### Usuarios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/auth/usuarios/me/` | Mi perfil |
| GET | `/api/v1/auth/usuarios/me/progresion/` | Mi progresión |
| GET | `/api/v1/auth/usuarios/me/historial/` | Mi historial |
| POST | `/api/v1/auth/usuarios/me/aceptar_ascenso/` | Aceptar ascenso |

### Lecturas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/lecturas/lecturas/` | Listar lecturas |
| GET | `/api/v1/lecturas/lecturas/{id}/` | Detalle lectura |
| POST | `/api/v1/lecturas/lecturas/{id}/iniciar_sesion/` | Iniciar sesión |

### Sesiones
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/lecturas/sesiones/` | Mis sesiones |
| GET | `/api/v1/lecturas/sesiones/{id}/` | Detalle sesión |
| POST | `/api/v1/lecturas/sesiones/{id}/responder/` | Responder pregunta |

### Rankings
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/lecturas/rankings/top_usuarios/` | Top 10 usuarios |
| GET | `/api/v1/lecturas/rankings/por_nivel/` | Por nivel |

### Estadísticas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/lecturas/estadisticas/general/` | Estadísticas generales |
| GET | `/api/v1/lecturas/estadisticas/mi_estadistica/` | Mis estadísticas |

### IA
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/ia/generar/generar_lectura/` | Generar lectura |
| POST | `/api/v1/ia/generar/generar_preguntas/` | Generar preguntas |
| POST | `/api/v1/ia/generar/generar_recomendaciones/` | Generar recomendaciones |
| GET | `/api/v1/ia/historial/` | Historial IA |
| GET | `/api/v1/ia/historial/resumen/` | Resumen de uso |

---

## 🔧 Troubleshooting

### Error: "No such table"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "AUTH_USER_MODEL"
Verificar que en `settings.py` esté:
```python
AUTH_USER_MODEL = 'auth.Usuario'
```

### Error: Puerto 8000 en uso
```bash
python manage.py runserver 8001  # Usar puerto diferente
```

### Docker: Servicios no inician
```bash
docker-compose down -v      # Limpiar volúmenes
docker-compose up -d --build # Reconstruir
```

---

## 📊 Próximos Pasos

1. **✅ BACKEND COMPLETADO** - Ya está todo listo!
2. **⏳ FRONTEND** - Crear interfaz Vue.js
3. **⏳ TESTING** - Suite de tests automáticos
4. **⏳ DEPLOYMENT** - Producción (AWS/Azure/GCP)

---

## 📖 Documentación Completa

- 📘 [ARQUITECTURA.md](ARQUITECTURA.md) - Arquitectura detallada
- 📙 [backend/hackaEdu/README_BACKEND.md](backend/hackaEdu/README_BACKEND.md) - Guía backend
- 📕 [CHECKLIST.md](CHECKLIST.md) - Plan de implementación

---

## 💡 Tips Útiles

### Crear superuser adicional
```bash
python manage.py createsuperuser
```

### Ver logs en tiempo real
```bash
docker-compose logs -f web
```

### Ejecutar command personalizado
```bash
python manage.py seed_data --clear  # Limpiar y recargar
```

### Acceso directo a BD
```bash
python manage.py dbshell
```

---

## 🎉 ¡LISTO PARA EMPEZAR!

**El backend está completamente funcional y documentado.**

### Pasos para iniciar:

1. **Docker (Recomendado):**
   ```bash
   docker-compose up -d
   ```

2. **O Local:**
   ```bash
   cd backend/hackaEdu
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_data
   python manage.py runserver
   ```

3. **Acceder a:**
   - 🌐 API: http://localhost:8000/api/v1/
   - 🔐 Admin: http://localhost:8000/admin/
   - 🧪 Test: `python test_api.py`

---

**¡A programar! 🚀**
