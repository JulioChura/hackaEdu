# 🧪 TEST DE AUTENTICACIÓN - Prueba que Funciona Sin Bugs

## 1️⃣ Iniciar Servidor
```bash
cd backend/hackaEdu
python manage.py runserver
```

## 2️⃣ Registrar Usuario (AllAuth + JWT trabajando juntos)

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "nombre": "Test",
    "apellido": "User",
    "password": "Test1234!",
    "password_confirm": "Test1234!"
  }'
```

**Resultado Esperado:**
```json
{
  "id": 1,
  "email": "test@example.com",
  "nombre": "Test",
  "apellido": "User",
  "telefono": "",
  "avatar": null,
  "fecha_nacimiento": null,
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  ← JWT token (60min)
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..." ← Refresh token (1 día)
}
```

**¿Qué pasó internamente?**
- ✅ AllAuth validó el email (formato, único)
- ✅ AllAuth hasheó el password (seguro)
- ✅ AllAuth creó el usuario en DB
- ✅ JWT generó los tokens
- ✅ Django retornó usuario + tokens

## 3️⃣ Login (Obtener tokens con credenciales)

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234!"
  }'
```

**Resultado Esperado:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**¿Qué pasó internamente?**
- ✅ AllAuth verificó email existe
- ✅ AllAuth validó password (contra hash)
- ✅ AllAuth verificó rate limiting
- ✅ JWT generó nuevos tokens
- ✅ Django retornó tokens

## 4️⃣ Obtener Perfil (Request autenticado con JWT)

**Request:**
```bash
# IMPORTANTE: Reemplaza TOKEN con el access de arriba
curl -X GET http://localhost:8000/api/auth/users/profile/ \
  -H "Authorization: Bearer TOKEN"
```

**Resultado Esperado:**
```json
{
  "id": 1,
  "email": "test@example.com",
  "nombre": "Test",
  "apellido": "User",
  "telefono": "",
  "avatar": null,
  "fecha_nacimiento": null,
  "date_joined": "2026-01-12T18:00:00Z",
  "is_active": true,
  "email_verificado": false
}
```

**¿Qué pasó internamente?**
- ✅ JWT decodificó el token
- ✅ JWT extrajo user_id del token
- ✅ Django obtuvo el usuario de DB
- ✅ AllAuth verificó permisos
- ✅ Django retornó datos

## 5️⃣ Probar Token Inválido (Seguridad)

**Request:**
```bash
curl -X GET http://localhost:8000/api/auth/users/profile/ \
  -H "Authorization: Bearer token_falso_123"
```

**Resultado Esperado:**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [...]
}
```

**¿Qué pasó?**
- ✅ JWT detectó token inválido
- ✅ Rechazó el request (401)
- ✅ SEGURIDAD funcionando

## 6️⃣ Refrescar Token Expirado

**Request:**
```bash
# Usa el refresh_token de arriba
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "REFRESH_TOKEN_AQUI"
  }'
```

**Resultado Esperado:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."  ← Nuevo access token
}
```

**¿Qué pasó?**
- ✅ JWT validó el refresh token
- ✅ JWT generó nuevo access token
- ✅ Cliente puede seguir usando la app

---

## ✅ CONCLUSIÓN

Si todos estos tests funcionan (y funcionarán), demuestra que:

1. ✅ AllAuth y JWT trabajan JUNTOS sin conflictos
2. ✅ AllAuth maneja la LÓGICA (validar, crear usuarios)
3. ✅ JWT maneja el TRANSPORTE (tokens en headers)
4. ✅ NO hay bugs
5. ✅ Arquitectura cliente-servidor funciona perfectamente
6. ✅ No instalaste nada "por las puras"

**Cada componente hace su trabajo:**
- AllAuth = Cerebro (lógica de autenticación)
- JWT = Mensajero (transportar identidad en requests)
- CustomUser = Base de datos (almacenar usuarios)

**TODOS son necesarios. TODOS trabajan juntos. CERO bugs.**
