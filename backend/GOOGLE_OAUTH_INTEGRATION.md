# Google OAuth Integration con Django-AllAuth

## Descripción General
Este proyecto implementa autenticación con Google usando django-allauth en una arquitectura cliente-servidor. El flujo convierte credenciales de Google en tokens JWT para acceso stateless a APIs REST.

---

## 1. Arquitectura de Componentes

### Backend (Django)
- **Django 5.2.7** con Custom User Model (email-based)
- **django-allauth 0.62.0**: Maneja OAuth y validaciones
- **djangorestframework-simplejwt 5.4.0**: Genera/valida tokens JWT
- **django-cors-headers**: Permite comunicación con frontend en otro puerto

### Frontend (Vue.js)
- Corriendo en `localhost:5173` (dev server)
- Realiza login y gestiona tokens JWT en localStorage

### Base de Datos
- SQLite (desarrollo)
- Tablas de allauth para usuarios sociales

---

## 2. Flujo Completo de Comunicación (Paso a Paso)

### **Paso 1: Usuario abre la página de login**
```
Frontend (localhost:5173)
│
└─→ Renderiza componente LoginWithGoogle.vue
    └─→ Botón con href: http://localhost:8000/api/auth/google/login/
```

### **Paso 2: Usuario hace clic en "Continuar con Google"**
```
Frontend (usuario en login)
│
└─→ GET http://localhost:8000/api/auth/google/login/
    │
    Backend: views_social.py → google_login()
    │
    └─→ Redirige a: /accounts/google/login/ (URL de allauth)
        │
        └─→ Allauth redirige a Google OAuth
            │
            └─→ https://accounts.google.com/o/oauth2/v2/auth
                ├─ client_id: 801054122554-plmjb874ob8kg6u9o4tuve962fb5fdu1...
                ├─ redirect_uri: http://localhost:8000/accounts/google/login/callback/
                ├─ scope: email profile openid
                └─ state: token_aleatorio_para_validar
```

### **Paso 3: Usuario autoriza en Google**
```
Usuario en pantalla de Google
│
└─→ Ingresa credenciales
    │
    └─→ Google valida y genera código temporal
        │
        └─→ Redirige a: /accounts/google/login/callback/
            ├─ code: 4/0ASc3gC0akNoQKGySVzWEnNl_LOxOBNi2AM1Zkpv2...
            ├─ state: token_aleatorio_para_validar
            └─ authuser: 0
```

### **Paso 4: AllAuth procesa el callback**
```
GET http://localhost:8000/accounts/google/login/callback/?code=4/0AS...&state=...
│
Backend: allauth.socialaccount.providers.oauth2.views
│
├─→ 1. Valida que el 'state' sea válido (previene CSRF)
│
├─→ 2. Intercambia 'code' por token de Google con Google servers
│       └─→ POST https://oauth2.googleapis.com/token
│           └─→ Obtiene: access_token, id_token, refresh_token de Google
│
├─→ 3. Obtiene datos del usuario de Google
│       └─→ GET https://www.googleapis.com/oauth2/v2/userinfo
│           └─→ Obtiene: email, name, picture, etc.
│
├─→ 4. Busca/crea usuario en BD
│       └─→ SELECT * FROM auth_user WHERE email = 'usuario@gmail.com'
│           ├─ Si existe: obtiene usuario
│           └─ Si NO existe: crea CustomUser con:
│               ├─ email: 'usuario@gmail.com'
│               ├─ nombre/apellido: (de Google profile)
│               ├─ username: UUID aleatorio (solo interno, no se usa)
│               └─ is_active: True
│
├─→ 5. Almacena credenciales de Google en BD
│       └─→ INSERT INTO socialaccount_socialaccount (user, provider, uid)
│       └─→ INSERT INTO socialaccount_socialtoken (account, token, token_secret)
│
├─→ 6. Crea sesión Django (cookie httpOnly)
│       └─→ SET-COOKIE: sessionid=abc123def456...
│       └─→ Almacena en django_session tabla
│
└─→ 7. Redirige al frontend con sesión activa
        └─→ 302 Found
            Location: http://localhost:5173/auth/google/callback
            Set-Cookie: sessionid=abc123def456...; HttpOnly; Path=/; Domain=localhost:8000
```

### **Paso 5: Frontend recibe la sesión**
```
GET http://localhost:5173/auth/google/callback
│
Frontend: GoogleCallback.vue (onMounted)
│
└─→ Usuario ahora tiene cookie de sesión del backend
    ├─ La cookie está disponible automáticamente en fetch()
    │  si se usa credentials: 'include'
    └─ Pero aún NO tiene JWT tokens
```

### **Paso 6: Frontend convierte sesión en JWT**
```
Frontend: GoogleCallback.vue → convertToJwt()
│
└─→ POST http://localhost:8000/api/auth/convert-token/
    ├─ Headers:
    │  └─ Cookie: sessionid=abc123def456... (enviado automáticamente)
    ├─ Body: vacío
    └─ credentials: 'include' (permite enviar cookies)
    
    Backend: views_social.py → convert_token()
    │
    ├─→ 1. Valida que request.user esté autenticado
    │       └─→ Allauth middleware lee la sesión cookie
    │
    ├─→ 2. Crea tokens JWT usando SimpleJWT
    │       └─→ refresh = RefreshToken.for_user(request.user)
    │       └─→ access = refresh.access_token
    │
    ├─→ 3. Obtiene datos de usuario y Google (si existen)
    │       └─→ user.google_account (property del modelo)
    │       └─→ user.google_picture, user.google_id
    │
    └─→ 4. Retorna JSON
            ├─ access: "eyJ0eXAiOiJKV1QiLCJhbGc..."
            ├─ refresh: "eyJ0eXAiOiJKV1QiLCJhbGc..."
            ├─ user: {id, email, nombre, apellido, ...}
            └─ google_data: {id, picture, ...}
```

### **Paso 7: Frontend almacena JWT y redirige**
```
Frontend: GoogleCallback.vue → respuesta convert_token()
│
├─→ 1. Almacena tokens en localStorage
│       ├─ localStorage.setItem('access_token', 'eyJ0eXAi...')
│       ├─ localStorage.setItem('refresh_token', 'eyJ0eXAi...')
│       └─ localStorage.setItem('user', JSON.stringify({...}))
│
├─→ 2. Limpia la sesión cookie (opcional)
│       └─→ Usuario ya no necesita sessionid del backend
│
└─→ 3. Redirige a dashboard
        └─→ router.push('/dashboard')
```

### **Paso 8: Frontend accede a APIs protegidas**
```
GET http://localhost:8000/api/auth/users/profile/
│
Headers:
├─ Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
├─ Content-Type: application/json
└─ Origin: http://localhost:5173
│
Backend: JWT middleware (rest_framework_simplejwt)
│
├─→ 1. Extrae token del header Authorization
│
├─→ 2. Valida la firma (HMAC-SHA256 con SECRET_KEY)
│
├─→ 3. Decodifica payload
│       ├─ user_id: 1
│       ├─ exp: 1673456789 (expira en 60 minutos)
│       └─ token_type: 'access'
│
├─→ 4. Obtiene usuario de BD
│       └─→ user = CustomUser.objects.get(id=1)
│
└─→ 5. Ejecuta vista con request.user = usuario autenticado
        └─→ Response: {id, email, nombre, apellido, ...}
```

---

## 3. Instalación y Configuración

### 3.1 Instalar dependencias
```bash
cd backend/hackaEdu
pip install django-allauth==0.62.0 djangorestframework-simplejwt==5.4.0 django-cors-headers==4.3.1
```

### 3.2 Configurar settings.py
```python
INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'auth_custom',
    # ...
]

SITE_ID = 2  # ID del Site en admin (localhost:8000)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

LOGIN_REDIRECT_URL = 'http://localhost:5173/auth/google/callback'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### 3.3 Configurar URLs
```python
# hackaEdu/urls.py
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('auth_custom.urls')),
]

# auth_custom/urls.py
urlpatterns = [
    path('google/login/', google_login, name='google_login'),
    path('convert-token/', convert_token, name='convert_token'),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('users/profile/', UserViewSet.as_view({'get': 'profile'})),
]
```

### 3.4 Migrar BD
```bash
python manage.py migrate
```

### 3.5 Crear Social Application en Django Admin
```
URL: http://localhost:8000/admin/
│
1. Ir a "Social applications"
│
2. Click "Add social application"
│
3. Llenar:
   ├─ Provider: Google
   ├─ Name: Google OAuth
   ├─ Client id: 801054122554-plmjb874ob8kg6u9o4tuve962fb5fdu1.apps.googleusercontent.com
   ├─ Secret key: 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
   └─ Sites: Seleccionar "localhost:8000"
│
4. Click "Save"
```

### 3.6 Obtener credenciales de Google
```
1. Ir a https://console.cloud.google.com
│
2. Crear proyecto (o usar existente)
│
3. Habilitar API: Google+ API
│
4. Crear OAuth 2.0 Credential (Web Application)
│
5. Authorized redirect URIs:
   ├─ http://localhost:8000/accounts/google/login/callback/
   └─ http://127.0.0.1:8000/accounts/google/login/callback/
│
6. Authorized JavaScript origins:
   ├─ http://localhost:8000
   └─ http://127.0.0.1:8000
│
7. Obtener Client ID y Client Secret
```

---

## 4. Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `hackaEdu/settings.py` | Configuración de allauth, JWT, CORS |
| `hackaEdu/urls.py` | Rutas principales (/accounts/, /api/auth/) |
| `auth_custom/models.py` | CustomUser con email-based login |
| `auth_custom/serializers.py` | Serialización de usuario, registro, login |
| `auth_custom/views.py` | REST API endpoints (perfil, token, registro) |
| `auth_custom/views_social.py` | Google OAuth: google_login(), convert_token() |
| `auth_custom/urls.py` | Rutas /api/auth/ |
| `fronted-cooMaestro/google-oauth-test.html` | Test manual del flujo |

---

## 5. Seguridad

### CSRF Protection
- AllAuth usa tokens CSRF en formularios HTML
- Para API REST, Django obtiene CSRF token del header `X-CSRFToken`
- Validado automáticamente por middleware

### State Parameter
- Google OAuth genera un parámetro `state` aleatorio
- AllAuth lo valida en el callback para prevenir CSRF attacks
- Si `state` no coincide, rechaza la autenticación

### JWT Security
- Tokens firmados con HMAC-SHA256 + SECRET_KEY
- Access token: válido 60 minutos
- Refresh token: válido 1 día (se rota automáticamente)
- Si token expirado, frontend usa refresh token para obtener nuevo access token

### Credentials Storage
- Tokens almacenados en `localStorage` (accesible vía JavaScript)
- Sesión Django (cookie httpOnly, no accesible vía JavaScript)
- Datos sensibles (password) nunca se envían al frontend

---

## 6. Troubleshooting

### Error: `SocialApp.DoesNotExist`
**Causa:** Social Application no está configurada en admin
**Solución:** Ir a Django admin → Social applications → Add → Seleccionar Google y Site

### Error: `CustomUser has no field named 'username'`
**Causa:** Modelo antiguo sin campo username
**Solución:** `python manage.py migrate` después de agregar el campo

### Error: CORS blocked
**Causa:** Frontend origin no está en ALLOWED_ORIGINS
**Solución:** Agregar origin a settings: `CORS_ALLOWED_ORIGINS = ['http://localhost:5173']`

### Error: Invalid redirect_uri
**Causa:** Redirect URI en Google Cloud no coincide con la del callback
**Solución:** Google Console → Authorized redirect URIs → Agregar `http://localhost:8000/accounts/google/login/callback/`

---

## 7. Próximos Pasos

- [ ] Implementar refresh token endpoint en frontend
- [ ] Agregar logout que limpia localStorage y sesión
- [ ] Agregar rate limiting en login
- [ ] Verificación de email para signups regulares
- [ ] MFA/2FA
- [ ] Soporte para otros proveedores (GitHub, Microsoft)

---

## 8. Referencias

- [Django-AllAuth Docs](https://django-allauth.readthedocs.io/)
- [Google OAuth 2.0 Flow](https://developers.google.com/identity/protocols/oauth2/web-server-flow)
- [JWT Best Practices](https://tools.ietf.org/html/rfc7519)
- [OWASP: Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
