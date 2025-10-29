def construir_prompt(datos_evaluacion):
    
    prompt = f"""Eres un evaluador pedagógico experto en educación básica. Analiza las respuestas de un estudiante según criterios específicos.

CONTEXTO:
- Sesión: {datos_evaluacion['sesion']['nombre']}
- Tema: {datos_evaluacion['sesion']['tema']}
- Objetivo: {datos_evaluacion['sesion']['objetivo']}
- Nivel: {datos_evaluacion['sesion']['nivel_educativo']}
- Estudiante: {datos_evaluacion['alumno']['nombre']} ({datos_evaluacion['alumno']['grado']})

CRITERIOS (escala 0-5):
"""
    
    for i, criterio in enumerate(datos_evaluacion['criterios'], 1):
        prompt += f"""
{i}. {criterio['nombre_criterio']} (ID: {criterio['criterio_id']}, Peso: {criterio['peso']})
   {criterio['descripcion']}
"""
    
    prompt += "\n\nRESPUESTAS:\n"
    
    for i, resp in enumerate(datos_evaluacion['respuestas'], 1):
        criterios_str = ', '.join([str(c) for c in resp['criterios_vinculados']])
        prompt += f"""
--- Respuesta {i} (ID: {resp['respuesta_id']}) ---
Pregunta: {resp['pregunta']}
Respuesta: {resp['texto_respuesta']}
Criterios a evaluar: {criterios_str}

"""
    
    prompt += f"""
INSTRUCCIONES DE EVALUACIÓN:

1. Analiza CADA respuesta del estudiante contra los criterios vinculados
2. Para cada evaluación, proporciona:
   - **Puntaje**: Usa la escala 0.0-5.0 (usa decimales: 3.5, 4.0, 4.5, etc.)
   - **Justificación**: Explica ESPECÍFICAMENTE qué hizo bien o mal el estudiante
   - **Evidencia**: Cita EXACTA de la respuesta (copia las palabras del alumno)

3. ESCALA DE PUNTAJES (nivel {datos_evaluacion['sesion']['nivel_educativo']}):
   • 0.0-1.0: No responde correctamente o no demuestra comprensión
   • 1.5-2.5: Respuesta muy básica, incompleta o con errores conceptuales
   • 3.0-3.5: Respuesta parcialmente correcta, falta profundidad o ejemplos
   • 4.0-4.5: Buena respuesta, demuestra comprensión con ejemplos claros
   • 5.0: Excelente respuesta, completa, con ejemplos y reflexión profunda

4. DIAGNÓSTICO FINAL - Debes incluir:
   - **Diagnóstico general**: Resume el desempeño global del estudiante en 2-3 oraciones específicas
   - **Fortalezas**: Identifica 2-3 aspectos CONCRETOS donde el estudiante destacó (con ejemplos)
   - **Áreas de mejora**: Señala 2-3 aspectos ESPECÍFICOS que debe mejorar (con sugerencias)

IMPORTANTE:
- NO uses frases genéricas como "Fortaleza1" o "Area1"
- SÉ ESPECÍFICO: menciona conceptos, ejemplos y habilidades concretas
- Basa TODO en las respuestas reales del estudiante

RESPONDE ÚNICAMENTE EN FORMATO JSON (sin markdown, sin texto adicional):

{{
  "alumno_id": {datos_evaluacion['alumno']['alumno_id']},
  "evaluacion_id": {datos_evaluacion['evaluacion_id']},
  "evaluaciones": [
    {{
      "respuesta_id": 1,
      "pregunta": "texto completo de la pregunta",
      "criterio_id": 1,
      "criterio_nombre": "nombre del criterio",
      "puntaje_obtenido": 4.5,
      "puntaje_maximo": 5.0,
      "justificacion": "Explica específicamente qué aspectos de la respuesta están bien y cuáles faltan",
      "evidencia": "Cita textual EXACTA de las palabras del estudiante que respaldan el puntaje"
    }}
  ],
  "diagnostico_general": "Resumen del desempeño global con aspectos específicos observados en las respuestas",
  "fortalezas": [
    "Fortaleza específica 1 observada en las respuestas del estudiante",
    "Fortaleza específica 2 con ejemplo concreto de su respuesta"
  ],
  "areas_mejora": [
    "Área específica de mejora 1 con sugerencia concreta",
    "Área específica de mejora 2 basada en las respuestas analizadas"
  ]
}}
"""
    
    return prompt
