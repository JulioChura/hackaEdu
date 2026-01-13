# Integración de Django-AllAuth - Guía de Implementación

## ✅ Cambios Realizados

### 1. **Dependencies (requirements.txt)**
- ✅ Agregado `django-allauth==0.62.0` (última versión estable)
- ✅ Agregado `django-cors-headers` para CORS
- ✅ Agregado `djangorestframework-simplejwt` para JWT tokens
- ✅ Removidas dependencias innecesarias (Flask, blinker, etc.)

### 2. **Configuración Django (settings.py)**
- ✅ Limpiado y reorganizado completamente
- ✅ Agregado soporte para arquitectura cliente-servidor
- ✅ Configurado CORS para Vue.js (localhost:5173)
- ✅ SimpleJWT configurado con tokens de corta duración (60min) y refresh token (1 día)
- ✅ Autenticación vía email (no username)
- ✅ Removidas configuraciones deprecadas
- ✅ Google OAuth configurado (falta agregar credenciales)

### 3. **Endpoints REST de Autenticación**
Creados en `auth_custom/`:

#### **Serializers (serializers.py)**
- `UserSerializer`: Para obtener/actualizar datos públicos del usuario
- `UserDetailSerializer`: Con campos adicionales (fecha registro, estado)
- `RegisterSerializer`: Para registro de nuevos usuarios
- `ChangePasswordSerializer`: Para cambiar contraseña

#### **Views (views.py)**
- `CustomTokenObtainPairView`: Obtener access/refresh tokens
- `RegisterView`: Registro de usuarios con tokens automáticos
- `UserViewSet`: CRUD de usuarios con acciones personalizadas:
  - `/api/auth/users/profile/` - Obtener perfil del usuario autenticado
  - `/api/auth/users/update_profile/` - Actualizar perfil
  - `/api/auth/users/change_password/` - Cambiar contraseña
  - `/api/auth/users/logout/` - Logout (para UI)

#### **URLs (urls.py)**
```
POST   /api/auth/register/              # Registrar usuario
POST   /api/auth/token/                 # Obtener tokens (login)
POST   /api/auth/token/refresh/         # Refrescar token
GET    /api/auth/users/profile/         # Obtener perfil
PUT    /api/auth/users/update_profile/  # Actualizar perfil
POST   /api/auth/users/change_password/ # Cambiar contraseña
POST   /api/auth/users/logout/          # Logout
```

### 4. **Main URLs (hackaEdu/urls.py)**
- ✅ Incluidos auth_custom URLs bajo `/api/auth/`
- ✅ Token refresh disponible en `/api/auth/token/refresh/`
- ✅ Allauth URLs en `/accounts/` (para admin si necesita)

## 🚀 Endpoints Disponibles

### Registrar Usuario
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "password": "MiPassword123",
  "password_confirm": "MiPassword123",
  "telefono": "+34912345678"  # Opcional
}

Response:
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login (Obtener Tokens)
```bash
POST /api/auth/token/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "MiPassword123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Obtener Perfil (Autenticado)
```bash
GET /api/auth/users/profile/
Authorization: Bearer {access_token}

Response:
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "telefono": "+34912345678",
  "avatar": null,
  "fecha_nacimiento": null,
  "date_joined": "2026-01-12T10:30:00Z",
  "is_active": true,
  "email_verificado": false
}
```

### Refrescar Token
```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Cambiar Contraseña
```bash
POST /api/auth/users/change_password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "MiPassword123",
  "new_password": "NuevaPassword456",
  "new_password_confirm": "NuevaPassword456"
}
```

## 🔐 Configuración de Seguridad

### CORS
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Vue.js dev server
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # Alternative port
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True  # Permite cookies
```

### Autenticación
- **Método principal**: JWT tokens (para API)
- **Email verificado**: No (configurado para APIs)
- **Login via**: Email (no username)
- **Rate limiting**: 5 intentos fallidos en 5 min

### JWT
```python
ACCESS_TOKEN_LIFETIME = 60 minutos
REFRESH_TOKEN_LIFETIME = 1 día
ROTATE_REFRESH_TOKENS = True  # Genera nuevo refresh en cada uso
```

## 📝 Configuración en el Frontend (Vue.js)

### 1. Guardar Tokens en localStorage
```javascript
// En login/register
localStorage.setItem('access_token', response.data.access);
localStorage.setItem('refresh_token', response.data.refresh);
```

### 2. Agregar Token a Requests
```javascript
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Interceptor para agregar token
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refrescar token si expira
instance.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      try {
        const resp = await axios.post('http://localhost:8000/api/auth/token/refresh/', {
          refresh: refreshToken
        });
        localStorage.setItem('access_token', resp.data.access);
        // Reintentar request original
        return instance(error.config);
      } catch (err) {
        // Redirigir a login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default instance;
```

## 🔧 Google OAuth (Opcional)

### Para habilitar Google OAuth:
1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea credenciales OAuth 2.0
3. Agrega en Django Admin:
   - Admin > Sites > sites > Editar dominio actual
   - Admin > Social Applications > Add
     - Provider: Google
     - Name: Google OAuth
     - Client ID: (de Google Cloud)
     - Secret: (de Google Cloud)
     - Sites: Selecciona el sitio actual

## ✨ Cambios Clave en Arquitectura

### Antes ❌
- Autenticación basada en sesiones
- Token endpoints genéricos
- Sin endpoints REST específicos
- Configuración duplicada

### Ahora ✅
- Autenticación basada en JWT tokens
- Endpoints REST RESTful específicos
- Separación clara entre cliente y servidor
- Configuración limpia y mantenible
- Django-allauth integrado y listo para social auth

## 📦 Próximos Pasos (Opcionales)

1. **Email Verification**: Cambiar `ACCOUNT_EMAIL_VERIFICATION` de `'none'` a `'optional'` o `'mandatory'`
2. **Google OAuth**: Obtener credenciales y configurar en admin
3. **Caché**: Agregar Redis para tokens revocados
4. **Logs**: Configurar logging para debug
5. **Tests**: Crear tests para los endpoints

## 🐛 Testing de Endpoints

```bash
# Crear superuser
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# En otra terminal, probar endpoints
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","nombre":"Test","apellido":"User","password":"Test1234","password_confirm":"Test1234"}'
```
