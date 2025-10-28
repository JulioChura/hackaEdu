# Script de instalación de Ollama y modelo Llama 3.2
# Proyecto: ReConéctate IA - Hackathon 2025
# Ejecutar en PowerShell como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INSTALACIÓN DE OLLAMA + LLAMA 3.2" -ForegroundColor Cyan
Write-Host "Proyecto: ReConéctate IA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Verificar si Ollama ya está instalado
Write-Host "Paso 1: Verificando si Ollama está instalado..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>$null
    if ($ollamaVersion) {
        Write-Host "✓ Ollama ya está instalado: $ollamaVersion" -ForegroundColor Green
        $instalarOllama = $false
    } else {
        throw "Ollama no encontrado"
    }
} catch {
    Write-Host "✗ Ollama no está instalado" -ForegroundColor Red
    $instalarOllama = $true
}

# Paso 2: Descargar e instalar Ollama si es necesario
if ($instalarOllama) {
    Write-Host ""
    Write-Host "Paso 2: Descargando Ollama..." -ForegroundColor Yellow
    
    $installerPath = "$env:TEMP\OllamaSetup.exe"
    $downloadUrl = "https://ollama.com/download/OllamaSetup.exe"
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "✓ Descarga completada" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Paso 3: Instalando Ollama..." -ForegroundColor Yellow
        Write-Host "   (Se abrirá el instalador - sigue las instrucciones)" -ForegroundColor Cyan
        
        Start-Process -Wait -FilePath $installerPath
        Write-Host "✓ Instalación completada" -ForegroundColor Green
        
        # Limpiar archivo temporal
        Remove-Item $installerPath -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "✗ Error descargando/instalando Ollama: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Descarga manualmente desde: https://ollama.com/download" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "Paso 2: Ollama ya instalado, continuando..." -ForegroundColor Green
}

# Paso 3: Verificar que Ollama esté corriendo
Write-Host ""
Write-Host "Paso 4: Verificando que Ollama esté corriendo..." -ForegroundColor Yellow

$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($ollamaProcess) {
    Write-Host "✓ Ollama está corriendo (PID: $($ollamaProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "⚠ Ollama no está corriendo, iniciando..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "✓ Ollama iniciado" -ForegroundColor Green
}

# Paso 4: Listar modelos instalados
Write-Host ""
Write-Host "Paso 5: Verificando modelos instalados..." -ForegroundColor Yellow

try {
    $modelosOutput = ollama list 2>&1 | Out-String
    Write-Host $modelosOutput -ForegroundColor Cyan
    
    # Verificar si llama3.2:3b está instalado
    if ($modelosOutput -match "llama3.2:3b") {
        Write-Host "✓ Modelo llama3.2:3b ya está instalado" -ForegroundColor Green
        $descargarModelo = $false
    } else {
        Write-Host "✗ Modelo llama3.2:3b no encontrado" -ForegroundColor Red
        $descargarModelo = $true
    }
} catch {
    Write-Host "⚠ No se pudieron listar modelos" -ForegroundColor Yellow
    $descargarModelo = $true
}

# Paso 5: Descargar modelo si es necesario
if ($descargarModelo) {
    Write-Host ""
    Write-Host "Paso 6: Descargando modelo llama3.2:3b..." -ForegroundColor Yellow
    Write-Host "   (Esto puede tardar 5-10 minutos dependiendo de tu conexión)" -ForegroundColor Cyan
    Write-Host "   Tamaño: ~2GB" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        ollama pull llama3.2:3b
        Write-Host ""
        Write-Host "✓ Modelo descargado exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "✗ Error descargando modelo: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Intenta manualmente: ollama pull llama3.2:3b" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "Paso 6: Modelo ya instalado, continuando..." -ForegroundColor Green
}

# Paso 6: Probar el modelo
Write-Host ""
Write-Host "Paso 7: Probando el modelo..." -ForegroundColor Yellow
Write-Host "   (Enviando prompt de prueba)" -ForegroundColor Cyan

try {
    $testPrompt = "Di solo 'OK' si estás funcionando correctamente"
    Write-Host ""
    Write-Host "   Prompt: $testPrompt" -ForegroundColor Gray
    
    $response = ollama run llama3.2:3b "$testPrompt" --verbose 2>&1
    
    Write-Host ""
    Write-Host "   Respuesta: $response" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✓ Modelo funcionando correctamente" -ForegroundColor Green
} catch {
    Write-Host "✗ Error probando modelo: $($_.Exception.Message)" -ForegroundColor Red
}

# Resumen final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Ollama instalado y corriendo" -ForegroundColor Green
Write-Host "✓ Modelo llama3.2:3b descargado" -ForegroundColor Green
Write-Host "✓ Prueba exitosa" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Yellow
Write-Host "  - Listar modelos:     ollama list" -ForegroundColor Cyan
Write-Host "  - Probar modelo:      ollama run llama3.2:3b" -ForegroundColor Cyan
Write-Host "  - Detener Ollama:     Stop-Process -Name ollama" -ForegroundColor Cyan
Write-Host "  - Iniciar Ollama:     ollama serve" -ForegroundColor Cyan
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Yellow
Write-Host "  cd backend\hackaEdu\llama3" -ForegroundColor Cyan
Write-Host "  python test_evaluador.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "¡Listo para la hackathon! 🚀" -ForegroundColor Green
Write-Host ""
