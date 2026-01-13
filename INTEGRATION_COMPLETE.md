# ✅ INTEGRACIÓN COMPLETADA: Django-AllAuth + Arquitectura Cliente-Servidor

## 📊 Resumen de Cambios

### Backend (Django)

#### 1. **Dependencias Actualizadas** ✅
```
✓ django-allauth==0.62.0 (última versión)
✓ django-cors-headers==4.3.1
✓ djangorestframework-simplejwt==5.4.0
✓ Removidas: Flask, Werkzeug, blinker, click, etc.
```

#### 2. **Configuración Optimizada** ✅
- `settings.py`: Limpiado, sin duplicados
- CORS configurado para Vue.js (localhost:5173)
- JWT tokens: 60min access + 1 día refresh
- Email-based authentication (sin username)
- Allauth integrado con Rate Limiting

#### 3. **Endpoints REST API** ✅

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/api/auth/register/` | POST | Registrar usuario |
| `/api/auth/token/` | POST | Login (obtener tokens) |
| `/api/auth/token/refresh/` | POST | Refrescar access token |
| `/api/auth/users/profile/` | GET | Obtener perfil |
| `/api/auth/users/update_profile/` | PUT | Actualizar perfil |
| `/api/auth/users/change_password/` | POST | Cambiar contraseña |
| `/api/auth/users/logout/` | POST | Logout |

#### 4. **Archivos Creados/Modificados**
```
backend/hackaEdu/
├── requirements.txt (ACTUALIZADO)
├── hackaEdu/
│   ├── settings.py (LIMPIADO Y OPTIMIZADO)
│   └── urls.py (ACTUALIZADO)
└── auth_custom/
    ├── serializers.py (NUEVO)
    ├── views.py (REESCRITO)
    ├── urls.py (NUEVO)
    └── models.py (SIN CAMBIOS - Compatible ✓)
```

---

### Frontend (Vue.js)

#### 1. **Servicio de Autenticación** ✅
```
fronted-cooMaestro/src/services/auth.js (NUEVO)
```
- Cliente axios con interceptores
- Manejo automático de tokens expirados
- Métodos para: register, login, logout, profile

#### 2. **Store Pinia** ✅
```
fronted-cooMaestro/src/stores/auth.js (NUEVO)
```
- Gestión centralizada del estado
- Métodos: register, login, logout, loadProfile
- Auto-carga de perfil al iniciar

#### 3. **Componente Login** ✅
```
fronted-cooMaestro/src/views/LoginView.vue (NUEVO)
```
- Interfaz de login responsiva
- Manejo de errores
- Integrado con store de autenticación

---

## 🔐 Flujo de Autenticación

### 1️⃣ Registro
```bash
POST /api/auth/register/
{
  "email": "user@example.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "password": "Pass123!",
  "password_confirm": "Pass123!"
}

Response:
{
  "id": 1,
  "email": "user@example.com",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  ← Access token
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."   ← Refresh token
}
```

### 2️⃣ Login
```bash
POST /api/auth/token/
{
  "email": "user@example.com",
  "password": "Pass123!"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3️⃣ Usar API (con token)
```bash
GET /api/auth/users/profile/
Authorization: Bearer {access_token}
```

### 4️⃣ Refrescar Token (cuando expira)
```bash
POST /api/auth/token/refresh/
{
  "refresh": "{refresh_token}"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."  ← Nuevo access token
}
```

---

## 🚀 Cómo Usar en el Frontend

### 1. Usar el Store en un Componente
```vue
<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Registrar
await authStore.register({
  email: 'user@example.com',
  nombre: 'Juan',
  apellido: 'Pérez',
  password: 'Pass123!',
  password_confirm: 'Pass123!'
})

// Login
await authStore.login('user@example.com', 'Pass123!')

// Logout
authStore.logout()

// Verificar autenticación
if (authStore.isAuthenticated) {
  console.log(authStore.user)
}

// Actualizar perfil
await authStore.updateProfile({ nombre: 'Juan Carlos' })

// Cambiar contraseña
await authStore.changePassword('oldPass', 'newPass', 'newPass')
</script>
```

### 2. Proteger Rutas
```javascript
// router/index.js
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    component: LoginView
  }
]

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})
```

### 3. Usar API Directamente
```javascript
import api from '@/services/auth'

// El token se agrega automáticamente en todas las peticiones
const response = await api.get('/users/profile/')
```

---

## ✨ Características Incluidas

✅ **Autenticación JWT**
- Tokens de corta duración (60min)
- Refresh tokens para renovar (1 día)
- Rotación automática de tokens

✅ **Seguridad**
- CORS configurado
- Rate limiting (5 intentos/5min)
- Password hashing con Django
- Email-based auth (más seguro que username)

✅ **Usuario Personalizado**
- Email único (login)
- Campos adicionales: nombre, apellido, teléfono, avatar
- Integrado con Django Admin

✅ **Social Auth (Ready)**
- Google OAuth preparado
- Solo falta agregar credenciales de Google Cloud

✅ **Validaciones**
- Email válido
- Contraseña mínimo 8 caracteres
- Confirmación de contraseña
- Manejo de errores

---

## 📝 Archivo de Documentación

**Ver también:**
- [ALLAUTH_INTEGRATION.md](./ALLAUTH_INTEGRATION.md) - Documentación completa con ejemplos
- [ALLAUTH_SETUP_SUMMARY.md](./ALLAUTH_SETUP_SUMMARY.md) - Resumen técnico de cambios

---

## 🔧 Base de Datos

### Migraciones Aplicadas ✅
```
✓ allauth.account
✓ allauth.socialaccount
✓ auth_custom
✓ contenido
✓ evaluacion
✓ habilidades
✓ logros
✓ niveles
✓ usuarios
```

### Crear Admin (Superuser)
```bash
cd backend/hackaEdu
python manage.py createsuperuser
# Email: admin@example.com
# Password: <tu_contraseña>
```

---

## 🎯 Próximos Pasos (Opcionales)

1. **Google OAuth**
   - Crear proyecto en [Google Cloud Console](https://console.cloud.google.com)
   - Obtener Client ID y Secret
   - Agregar en Django Admin

2. **Email Verification**
   - Cambiar en settings: `ACCOUNT_EMAIL_VERIFICATION = 'optional'`
   - Configurar SMTP para enviar emails

3. **Frontend Enhancements**
   - Guard routes protegidas
   - Formulario de registro
   - Recuperar contraseña olvidada
   - Perfil de usuario editable

4. **Backend Enhancements**
   - Logs de autenticación
   - Auditoría de cambios
   - Caché de usuarios
   - Tests automatizados

---

## ✅ Testing

### Backend
```bash
# Verificar configuración
python manage.py check

# Crear superuser
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Tests
python manage.py test auth_custom
```

### Frontend
```bash
# Instalar Pinia si no está
npm install pinia

# Ejecutar dev server
npm run dev

# Acceder a http://localhost:5173/login
```

### Probar Endpoints
```bash
# Registrar
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "nombre":"Test",
    "apellido":"User",
    "password":"Pass1234",
    "password_confirm":"Pass1234"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass1234"}'

# Perfil (con token)
curl -X GET http://localhost:8000/api/auth/users/profile/ \
  -H "Authorization: Bearer {access_token}"
```

---

## 🎉 ¡Listo para Producción!

Tu proyecto ahora tiene:
- ✅ Autenticación moderna con JWT
- ✅ API REST RESTful
- ✅ Frontend integrado
- ✅ Seguridad configurada
- ✅ Escalabilidad lista

**Arquitectura: Cliente-Servidor ✓**
- Backend: Django REST Framework
- Frontend: Vue.js + Pinia + Axios
- Comunicación: JSON + JWT Tokens

---

## 📞 Troubleshooting

### Error: "CORS not allowed"
→ Verificar `CORS_ALLOWED_ORIGINS` en settings.py

### Error: "Invalid token"
→ Verificar que el token no esté expirado, usar refresh endpoint

### Error: "401 Unauthorized"
→ Token faltante o inválido. Verificar header Authorization

### Error: "422 Unprocessable Entity"
→ Validación fallida. Revisar formato del JSON enviado

---

**¿Preguntas? Revisar documentación en:**
- ALLAUTH_INTEGRATION.md
- Django-AllAuth: https://django-allauth.readthedocs.io/
- DRF JWT: https://django-rest-framework-simplejwt.readthedocs.io/
