# Script de Prueba - Autenticación HackaEdu (Windows)
# Ejecutar: powershell -ExecutionPolicy Bypass -File test_login.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "PRUEBA DE AUTENTICACIÓN" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$BackendUrl = "http://localhost:8000"
$TestEmail = "test@example.com"
$TestPassword = "testpassword123"

Write-Host "1. Intentando login con credenciales de prueba..." -ForegroundColor Yellow
Write-Host "URL: $BackendUrl/auth/token/" -ForegroundColor Gray
Write-Host "Email: $TestEmail" -ForegroundColor Gray
Write-Host "Password: $TestPassword" -ForegroundColor Gray
Write-Host ""

# Hacer request de login
try {
    $loginBody = @{
        email = $TestEmail
        password = $TestPassword
    } | ConvertTo-Json

    $loginResponse = Invoke-WebRequest `
        -Uri "$BackendUrl/auth/token/" `
        -Method POST `
        -Headers @{"Content-Type" = "application/json"} `
        -Body $loginBody

    $loginData = $loginResponse.Content | ConvertFrom-Json
    
    Write-Host "Respuesta del servidor:" -ForegroundColor Green
    Write-Host ($loginData | ConvertTo-Json -Depth 10) -ForegroundColor White
    Write-Host ""

    # Extraer tokens
    $AccessToken = $loginData.access
    $RefreshToken = $loginData.refresh

    if ([string]::IsNullOrEmpty($AccessToken)) {
        Write-Host "❌ ERROR: No se pudo obtener el token" -ForegroundColor Red
        Write-Host ""
        Write-Host "POSIBLES CAUSAS:" -ForegroundColor Yellow
        Write-Host "1. El usuario no existe - Crear usuario en Django admin" -ForegroundColor Gray
        Write-Host "2. La contraseña es incorrecta" -ForegroundColor Gray
        Write-Host "3. El servidor no está corriendo en http://localhost:8000" -ForegroundColor Gray
        Write-Host "4. Las credenciales JWT no están configuradas" -ForegroundColor Gray
        exit 1
    }

    Write-Host "✅ Tokens obtenidos correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access Token (primeros 50 caracteres):" -ForegroundColor Yellow
    Write-Host $AccessToken.Substring(0, [Math]::Min(50, $AccessToken.Length)) + "..." -ForegroundColor White
    Write-Host ""

    Write-Host "2. Obteniendo perfil del usuario..." -ForegroundColor Yellow
    Write-Host "Usando Access Token: $($AccessToken.Substring(0, 50))..." -ForegroundColor Gray
    Write-Host ""

    # Obtener perfil
    $profileResponse = Invoke-WebRequest `
        -Uri "$BackendUrl/auth/users/profile/" `
        -Method GET `
        -Headers @{
            "Content-Type" = "application/json"
            "Authorization" = "Bearer $AccessToken"
        }

    $profileData = $profileResponse.Content | ConvertFrom-Json

    Write-Host "Respuesta del servidor:" -ForegroundColor Green
    Write-Host ($profileData | ConvertTo-Json -Depth 10) -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host "❌ ERROR EN LA SOLICITUD:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Asegúrate de que:" -ForegroundColor Yellow
    Write-Host "1. El servidor Django está corriendo" -ForegroundColor Gray
    Write-Host "2. El usuario existe en la base de datos" -ForegroundColor Gray
    Write-Host "3. La contraseña es correcta" -ForegroundColor Gray
    exit 1
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "PRUEBA COMPLETADA" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Si ambas respuestas fueron exitosas, el login está funcionando correctamente!" -ForegroundColor Green
