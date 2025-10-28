# GUÍA RÁPIDA - EMPEZAR EN 5 MINUTOS
## Módulo IA - ReConéctate IA

---

## PASO 1: INSTALAR OLLAMA (2 minutos)

### Opción A - Automático (RECOMENDADO)

1. Abre PowerShell como **Administrador**
2. Ejecuta:
```powershell
cd "e:\Archivos\2025 B\hack4edu\hackaEdu\backend\hackaEdu\llama3"
.\instalar_ollama.ps1
```

3. Espera que termine (2-10 minutos dependiendo de tu internet)

### Opción B - Manual

1. Descarga: https://ollama.com/download/windows
2. Instala el ejecutable
3. Abre PowerShell normal y ejecuta:
```powershell
ollama pull llama3.2:3b
```

### Verificar instalación:
```powershell
ollama list
```

**Debes ver algo como:**
```
NAME              ID              SIZE      MODIFIED
llama3.2:3b       abc123def       2.0 GB    5 minutes ago
```

---

## PASO 2: PROBAR EL MÓDULO (1 minuto)

```powershell
cd "e:\Archivos\2025 B\hack4edu\hackaEdu\backend\hackaEdu\llama3"
python test_evaluador.py
```

**Menú que aparece:**
```
PRUEBAS DEL MÓDULO DE EVALUACIÓN CON IA

Selecciona una opción:
  1. Probar construcción de prompt
  2. Verificar conexión con Ollama
  3. Evaluación completa con IA (requiere Ollama)
  4. Ejecutar todas las pruebas
  0. Salir

Opción:
```

**Selecciona opción 2** para verificar que Ollama funciona

---

## PASO 3: EVALUACIÓN DE PRUEBA (2 minutos)

En el mismo menú, **selecciona opción 3**

Esto:
1. Toma datos de ejemplo (alumno Miguel, sesión "Lenguaje Corporal")
2. Construye el prompt
3. Llama a Ollama (tarda 10-30 segundos)
4. Muestra resultados en JSON

**Resultado esperado:**
```json
{
  "alumno_id": 123,
  "evaluacion_id": 456,
  "evaluaciones": [
    {
      "respuesta_id": 1,
      "criterio_id": 1,
      "puntaje_obtenido": 4.0,
      "justificacion": "Miguel identifica correctamente...",
      ...
    }
  ],
  "diagnostico_general": "Miguel muestra buena comprensión...",
  "fortalezas": [...],
  "areas_mejora": [...]
}
```

---

## PASO 4: INTEGRAR CON TU BACKEND (MAÑANA)

### 4.1 Coordinar con PERSONA 4

Necesitas que te diga:
- ¿Cómo se llaman los modelos Django? (Sesion, Criterio, etc.)
- ¿Cómo obtienes las respuestas del alumno?
- ¿Dónde guardas los resultados?

### 4.2 Completar 2 métodos en `evaluador.py`

**Método 1: `_obtener_datos_evaluacion()` (línea 113)**
```python
def _obtener_datos_evaluacion(self, evaluacion_id, alumno_id):
    # TODO: Reemplazar con consultas reales a tu BD
    from evaluacion.models import Evaluacion, Criterio, RespuestaAlumno
    
    # Obtener evaluación
    evaluacion = Evaluacion.objects.get(id=evaluacion_id)
    
    # Obtener criterios
    criterios = Criterio.objects.filter(sesion=evaluacion.sesion)
    
    # Obtener respuestas
    respuestas = RespuestaAlumno.objects.filter(
        evaluacion=evaluacion,
        alumno_id=alumno_id
    )
    
    # Estructurar datos
    return {
        'sesion': {...},
        'criterios': [...],
        'respuestas': [...],
        ...
    }
```

**Método 2: `_guardar_evaluaciones()` (línea 264)**
```python
def _guardar_evaluaciones(self, evaluaciones):
    from evaluacion.models import EvaluacionCriterioRespuesta, ReporteIA
    
    with transaction.atomic():
        # Guardar reporte general
        reporte = ReporteIA.objects.create(
            evaluacion_id=evaluaciones['evaluacion_id'],
            alumno_id=evaluaciones['alumno_id'],
            diagnostico_general=evaluaciones['diagnostico_general'],
            ...
        )
        
        # Guardar cada evaluación
        for eval_item in evaluaciones['evaluaciones']:
            EvaluacionCriterioRespuesta.objects.create(
                respuesta_id=eval_item['respuesta_id'],
                criterio_id=eval_item['criterio_id'],
                puntaje_obtenido=eval_item['puntaje_obtenido'],
                ...
            )
        
        return reporte
```

### 4.3 Probar endpoint

```powershell
# Iniciar Django
cd "e:\Archivos\2025 B\hack4edu\hackaEdu\backend\hackaEdu"
python manage.py runserver
```

**Probar con curl o Postman:**
```http
POST http://localhost:8000/api/llama3/evaluar-respuestas/
Content-Type: application/json

{
  "evaluacion_id": 1,
  "alumno_id": 1
}
```

---

## ARCHIVOS IMPORTANTES

### Estructura creada:
```
backend/hackaEdu/llama3/
├── prompts.py              ← Construcción de prompts
├── evaluador.py            ← Lógica principal 
├── views.py                ← Endpoints API
├── urls.py                 ← Rutas
├── test_evaluador.py       ← Pruebas
├── datos_ejemplo.json      ← Datos de prueba
├── instalar_ollama.ps1     ← Instalador
└── README_IA.md            ← Documentación completa 
```

### Documentación:
1. **`README_IA.md`** - Guía completa (400+ líneas)
2. **`RESUMEN_MODULO_IA.md`** - Resumen ejecutivo
3. **Este archivo** - Quick start