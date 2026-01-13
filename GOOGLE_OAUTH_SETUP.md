# 🔐 GOOGLE OAUTH - CONFIGURACIÓN COMPLETA

## ✅ CHECKLIST DE CONFIGURACIÓN

### 1. Google Cloud Console
- [ ] Proyecto creado en Google Cloud Console
- [ ] Google+ API habilitada
- [ ] OAuth Client ID creado (Web application)
- [ ] JavaScript origins configurados:
  - `http://localhost:8000`
  - `http://127.0.0.1:8000`
- [ ] Redirect URIs configurados:
  - `http://localhost:8000/accounts/google/login/callback/`
  - `http://127.0.0.1:8000/accounts/google/login/callback/`
- [ ] Client ID y Client Secret copiados

### 2. Django Admin
- [ ] Superuser creado: `python manage.py createsuperuser`
- [ ] Servidor iniciado: `python manage.py runserver`
- [ ] Ir a http://localhost:8000/admin/
- [ ] Sites configurado:
  - Domain: `localhost:8000`
  - Display name: `hackaEdu Local`
- [ ] Social Application creada:
  - Provider: Google
  - Name: Google OAuth
  - Client ID: (de Google Cloud)
  - Secret key: (de Google Cloud)
  - Site seleccionado: `localhost:8000`

### 3. Vue.js Router
Agrega estas rutas en `router/index.js`:

```javascript
import LoginWithGoogle from '../views/LoginWithGoogle.vue'
import GoogleCallback from '../views/GoogleCallback.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginWithGoogle
  },
  {
    path: '/auth/google/callback',
    name: 'google-callback',
    component: GoogleCallback
  },
  // ... tus otras rutas
]
```

---

## 🚀 CÓMO FUNCIONA

### Flujo Completo:

```
1. Usuario click "Continuar con Google"
   ↓
2. Vue redirige a: http://localhost:8000/api/auth/google/login/
   ↓
3. Django redirige a: https://accounts.google.com (login de Google)
   ↓
4. Usuario se autentica en Google
   ↓
5. Google redirige a: http://localhost:8000/accounts/google/login/callback/
   ↓
6. Django (AllAuth) procesa:
   - Valida el código de Google
   - Crea/actualiza usuario en tu DB
   - Crea/actualiza SocialAccount
   - Guarda token de Google en SocialToken
   - Crea sesión de Django
   ↓
7. Django redirige a: http://localhost:5173/auth/google/callback
   ↓
8. Vue (GoogleCallback.vue):
   - Llama GET /api/auth/convert-token/ (con cookies de sesión)
   - Django genera JWT tokens
   - Vue guarda tokens en localStorage
   ↓
9. Vue redirige a /dashboard
   ✅ Usuario autenticado con JWT
```

---

## 🧪 PRUEBA PASO A PASO

### 1. Iniciar Backend
```bash
cd backend/hackaEdu
python manage.py runserver
```

### 2. Iniciar Frontend
```bash
cd fronted-cooMaestro
npm run dev
```

### 3. Probar Login con Google
1. Ir a: http://localhost:5173/login
2. Click en "Continuar con Google"
3. Serás redirigido a Google
4. Autoriza la aplicación
5. Deberías volver a Vue en /dashboard

### 4. Verificar en Admin
1. Ir a: http://localhost:8000/admin/
2. Ver "Social accounts" → Deberías ver tu cuenta de Google
3. Ver "Social application tokens" → Deberías ver el token de Google

---

## 🔍 DEBUGGING

### Si no funciona:

1. **Error: "redirect_uri_mismatch"**
   - Verifica que las URIs en Google Cloud coincidan EXACTAMENTE:
     ```
     http://localhost:8000/accounts/google/login/callback/
     ```
   - NO uses https en desarrollo
   - NO olvides el slash final `/`

2. **Error: "Social application not found"**
   - Ve a Django Admin
   - Verifica que la Social Application tenga el Site correcto seleccionado
   - El dominio del Site debe ser `localhost:8000` (sin http://)

3. **Error: "CSRF token missing"**
   - Asegúrate de que CORS esté configurado:
   ```python
   CORS_ALLOW_CREDENTIALS = True
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:5173",
   ]
   ```

4. **Error al obtener JWT tokens**
   - Verifica que `withCredentials: true` esté en el axios call
   - Verifica que el usuario esté autenticado en la sesión

---

## 📊 DATOS GUARDADOS

Después de un login exitoso con Google, verás:

### En CustomUser:
```sql
id: 1
email: "juan@gmail.com"
nombre: "Juan"
apellido: "Pérez"
is_active: True
```

### En SocialAccount:
```sql
id: 1
user_id: 1
provider: "google"
uid: "105842347892345"
extra_data: {
  "email": "juan@gmail.com",
  "picture": "https://lh3.googleusercontent.com/...",
  "name": "Juan Pérez",
  ...
}
```

### En SocialToken:
```sql
id: 1
account_id: 1
token: "ya29.a0AfH6SMB..."
expires_at: "2026-01-12 20:00:00"
```

### En localStorage (Frontend):
```javascript
access_token: "eyJ0eXAiOiJKV1QiLCJhbGc..."
refresh_token: "eyJ0eXAiOiJKV1QiLCJhbGc..."
user: {
  "id": 1,
  "email": "juan@gmail.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "google_data": {
    "google_id": "105842347892345",
    "picture": "https://lh3.googleusercontent.com/...",
    "email": "juan@gmail.com"
  }
}
```

---

## 🔐 SEGURIDAD

### Tokens:
- **Access token JWT**: 60 minutos
- **Refresh token JWT**: 1 día
- **Google access token**: Variable (guardado en DB, manejado por AllAuth)

### NO expongas:
- ❌ Client Secret de Google
- ❌ SECRET_KEY de Django
- ❌ Tokens de Google en API responses

### SÍ expones:
- ✅ JWT tokens (son efímeros y firmados)
- ✅ Datos públicos del perfil de Google
- ✅ Email, nombre, foto de perfil

---

## 📱 ENDPOINTS DISPONIBLES

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/auth/google/login/` | GET | Iniciar login con Google |
| `/api/auth/convert-token/` | GET | Convertir sesión a JWT |
| `/api/auth/token/` | POST | Login email/password |
| `/api/auth/register/` | POST | Registro tradicional |
| `/api/auth/users/profile/` | GET | Obtener perfil |

---

## ✅ LISTO!

Si completaste todos los pasos, tu aplicación ahora tiene:
- ✅ Login con email/password
- ✅ Login con Google OAuth
- ✅ JWT tokens para ambos métodos
- ✅ Perfil con datos de Google
- ✅ Token de Google guardado (para usar APIs de Google)

**Siguiente paso:** Probar login con Google desde http://localhost:5173/login
