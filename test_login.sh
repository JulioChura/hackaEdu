#!/bin/bash
# Script de Prueba - Autenticación HackaEdu

echo "================================"
echo "PRUEBA DE AUTENTICACIÓN"
echo "================================"
echo ""

# Variables
BACKEND_URL="http://localhost:8000"
TEST_EMAIL="test@example.com"
TEST_PASSWORD="testpassword123"

echo "1. Intentando login con credenciales de prueba..."
echo "URL: $BACKEND_URL/auth/token/"
echo "Email: $TEST_EMAIL"
echo "Password: $TEST_PASSWORD"
echo ""

# Hacer request de login
LOGIN_RESPONSE=$(curl -s -X POST \
  "$BACKEND_URL/auth/token/" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

echo "Respuesta del servidor:"
echo "$LOGIN_RESPONSE" | python3 -m json.tool
echo ""

# Extraer tokens
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access', ''))" 2>/dev/null)
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('refresh', ''))" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ ERROR: No se pudo obtener el token"
  echo ""
  echo "POSIBLES CAUSAS:"
  echo "1. El usuario no existe - Crear usuario en Django admin"
  echo "2. La contraseña es incorrecta"
  echo "3. El servidor no está corriendo en http://localhost:8000"
  echo "4. Las credenciales JWT no están configuradas"
  exit 1
fi

echo "✅ Tokens obtenidos correctamente!"
echo ""
echo "Access Token (primeros 50 caracteres):"
echo "${ACCESS_TOKEN:0:50}..."
echo ""

echo "2. Obteniendo perfil del usuario..."
echo "Usando Access Token: ${ACCESS_TOKEN:0:50}..."
echo ""

PROFILE_RESPONSE=$(curl -s -X GET \
  "$BACKEND_URL/auth/users/profile/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Respuesta del servidor:"
echo "$PROFILE_RESPONSE" | python3 -m json.tool
echo ""

echo "================================"
echo "PRUEBA COMPLETADA"
echo "================================"
echo ""
echo "Si ambas respuestas fueron exitosas, el login está funcionando correctamente!"
