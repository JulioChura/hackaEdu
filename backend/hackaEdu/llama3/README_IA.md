# MÓDULO DE IA - CONTENIDO DEL MÓDULO

Este módulo contiene la implementación completa para evaluación automática de respuestas abiertas usando IA local (Ollama + Llama 3.2).

### Archivos creados:

1. **`prompts.py`** - Construcción de prompts estructurados
2. **`evaluador.py`** - Lógica principal de evaluación con IA
3. **`views.py`** - Endpoints de la API
4. **`urls.py`** - Rutas actualizadas
5. **`test_evaluador.py`** - Script de pruebas
6. **`README_IA.md`** - Esta documentación

---

## INSTALACIÓN Y CONFIGURACIÓN

### Paso 1: Instalar Ollama

**Windows (PowerShell como Administrador):**
```powershell
# Descargar instalador
Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "$env:TEMP\OllamaSetup.exe"

# Ejecutar instalador
Start-Process -Wait -FilePath "$env:TEMP\OllamaSetup.exe"

# Verificar instalación
ollama --version
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Paso 2: Descargar Modelo

```powershell
# Descargar Llama 3.2 3B (recomendado para la hackathon)
ollama pull llama3.2:3b

# Verificar que se instaló
ollama list
```

**Modelos alternativos (si llama3.2:3b es muy lento):**
- `llama3.2:1b` - Más rápido pero menos preciso
- `phi3:mini` - Alternativa ligera de Microsoft
- `mistral:7b` - Más potente pero más lento

### Paso 3: Probar Ollama

```powershell
# Iniciar Ollama (debería iniciar automáticamente)
ollama serve

# En otra terminal, probar el modelo
ollama run llama3.2:3b "Hola, ¿funcionas correctamente?"
```

### Paso 4: Instalar dependencias Python

```powershell
cd backend\hackaEdu
pip install requests
```

---

## PRUEBAS

### Opción 1: Script de prueba interactivo

```powershell
cd backend\hackaEdu\llama3
python test_evaluador.py
```

Esto abrirá un menú con opciones:
1. Probar construcción de prompt (sin IA)
2. Verificar conexión con Ollama
3. Evaluación completa con IA
4. Ejecutar todas las pruebas

### Opción 2: Probar endpoints con HTTP

**1. Verificar que Ollama esté disponible:**
```http
GET http://localhost:8000/api/llama3/verificar-ia/
```

Respuesta esperada:
```json
{
  "disponible": true,
  "modelos": ["llama3.2:3b"],
  "error": null
}
```

**2. Generar prompt de prueba (sin ejecutar IA):**
```http
POST http://localhost:8000/api/llama3/prueba-prompt/
Content-Type: application/json

{
  "evaluacion_id": 123,
  "alumno_id": 456
}
```

**3. Evaluación completa:**
```http
POST http://localhost:8000/api/llama3/evaluar-respuestas/
Content-Type: application/json

{
  "evaluacion_id": 123,
  "alumno_id": 456
}
```

---

## FLUJO DE DATOS

```
1. Frontend/Backend llama: POST /api/llama3/evaluar-respuestas/
   Body: { evaluacion_id, alumno_id }

2. evaluador.py obtiene datos de BD:
   - Sesión (nombre, tema, objetivo)
   - Criterios de evaluación
   - Preguntas con criterios vinculados
   - Respuestas del alumno

3. prompts.py construye prompt estructurado:
   - Contexto educativo
   - Lista de criterios
   - Respuestas a evaluar
   - Instrucciones de formato JSON

4. evaluador.py llama a Ollama:
   POST http://localhost:11434/api/generate
   { model, prompt, options }

5. Ollama (Llama 3.2) genera evaluación en JSON

6. evaluador.py parsea y valida JSON:
   - Verifica campos requeridos
   - Valida rangos de puntajes (0-5)
   - Estructura de evaluaciones

7. evaluador.py guarda en BD:
   - Tabla: evaluacion_criterio_respuesta
   - Tabla: reporte_ia

8. Retorna respuesta al frontend:
   { success, data, reporte_id }
```

---

## INTEGRACIÓN

**Necesita tablas/modelos:**

```python
# evaluacion/models.py

class Sesion(models.Model):
    sesion_id = models.AutoField(primary_key=True)
    nombre_sesion = models.CharField(max_length=200)
    objetivo_sesion = models.TextField()
    # ... más campos

class CriterioEvaluacion(models.Model):
    criterio_id = models.AutoField(primary_key=True)
    sesion = models.ForeignKey(Sesion)
    nombre_criterio = models.CharField(max_length=200)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=3, decimal_places=1)
    # ... más campos

class Pregunta(models.Model):
    pregunta_id = models.AutoField(primary_key=True)
    sesion = models.ForeignKey(Sesion)
    texto_pregunta = models.TextField()
    # ... más campos

class PreguntaCriterio(models.Model):
    """Tabla de unión: qué criterios evalúan cada pregunta"""
    pregunta_criterio_id = models.AutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta)
    criterio = models.ForeignKey(CriterioEvaluacion)
    activo = models.BooleanField(default=True)

class RespuestaAlumno(models.Model):
    respuesta_id = models.AutoField(primary_key=True)
    evaluacion = models.ForeignKey('Evaluacion')
    alumno = models.ForeignKey('alumnos.Alumno')
    pregunta = models.ForeignKey(Pregunta)
    texto_respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

class EvaluacionCriterioRespuesta(models.Model):
    """AQUÍ GUARDAS TUS RESULTADOS"""
    evaluacion_criterio_id = models.AutoField(primary_key=True)
    respuesta = models.ForeignKey(RespuestaAlumno)
    criterio = models.ForeignKey(CriterioEvaluacion)
    puntaje_obtenido = models.DecimalField(max_digits=3, decimal_places=1)
    puntaje_maximo = models.DecimalField(max_digits=3, decimal_places=1)
    justificacion = models.TextField()
    evidencia = models.TextField()
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

class ReporteIA(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    evaluacion = models.ForeignKey('Evaluacion')
    alumno = models.ForeignKey('alumnos.Alumno')
    diagnostico_general = models.TextField()
    fortalezas_identificadas = models.TextField()
    areas_mejora = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
```

**Coordinar con PERSONA 4:**
1. Nombres exactos de modelos y campos
2. Relaciones entre tablas (ForeignKey)
3. Endpoint para obtener datos: `GET /api/evaluaciones/{id}/datos-ia/`

## CONFIGURACIÓN AVANZADA

### Ajustar parámetros de IA

En `evaluador.py`, método `_llamar_ia()`:

```python
"options": {
    "temperature": 0.3,  # 0.0-1.0 (más bajo = más consistente)
    "top_p": 0.9,        # Núcleo de probabilidad
    "num_predict": 2000, # Máximo tokens de respuesta
}
```

**Recomendaciones:**
- **Temperature 0.3**: Evaluaciones consistentes (recomendado)
- **Temperature 0.7**: Más creativo pero menos predecible
- **num_predict**: Aumentar si necesitas respuestas más largas

### Timeout

```python
evaluador = EvaluadorIA()
respuesta = evaluador._llamar_ia(prompt, timeout=60)  # 60 segundos
```

**Tiempos esperados:**
- CPU: 15-30 segundos
- GPU: 3-8 segundos

### Cambiar modelo

```python
# En evaluador.py o al instanciar
evaluador = EvaluadorIA(modelo="llama3.2:1b")  # Modelo más rápido
```

---