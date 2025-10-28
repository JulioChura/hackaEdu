"""
Módulo para construcción de prompts para evaluación con IA
Proyecto: ReConéctate IA - Hackathon 2025
Autor: PERSONA 1 (IA + PROMPTS)
"""

def construir_prompt(datos_evaluacion):
    """
    Construye el prompt estructurado para evaluación de respuestas con IA
    
    Args:
        datos_evaluacion (dict): Diccionario con la siguiente estructura:
            {
                'sesion': {
                    'nombre': str,
                    'tema': str,
                    'objetivo': str,
                    'nivel_educativo': str
                },
                'criterios': [
                    {
                        'criterio_id': int,
                        'nombre_criterio': str,
                        'descripcion': str,
                        'peso': float
                    },
                    ...
                ],
                'respuestas': [
                    {
                        'respuesta_id': int,
                        'pregunta': str,
                        'texto_respuesta': str,
                        'criterios_vinculados': [int, ...]
                    },
                    ...
                ],
                'alumno': {
                    'alumno_id': int,
                    'nombre': str,
                    'grado': str
                },
                'evaluacion_id': int
            }
    
    Returns:
        str: Prompt formateado para enviar a la IA
    """
    
    prompt = f"""Eres un evaluador pedagógico experto en educación básica. Tu tarea es analizar las respuestas de un estudiante según criterios específicos definidos por el docente.

CONTEXTO DE LA EVALUACIÓN:
- Sesión: {datos_evaluacion['sesion']['nombre']}
- Tema: {datos_evaluacion['sesion']['tema']}
- Objetivo de aprendizaje: {datos_evaluacion['sesion']['objetivo']}
- Nivel educativo: {datos_evaluacion['sesion']['nivel_educativo']}
- Estudiante: {datos_evaluacion['alumno']['nombre']} ({datos_evaluacion['alumno']['grado']})

CRITERIOS DE EVALUACIÓN (escala 0.0 - 5.0):
"""
    
    # Agregar criterios
    for i, criterio in enumerate(datos_evaluacion['criterios'], 1):
        prompt += f"""
{i}. {criterio['nombre_criterio']} (ID: {criterio['criterio_id']}, Peso: {criterio['peso']})
   Descripción: {criterio['descripcion']}
   Puntaje máximo: 5.0
"""
    
    prompt += "\n\nRESPUESTAS DEL ESTUDIANTE A EVALUAR:\n"
    
    # Agregar respuestas
    for i, resp in enumerate(datos_evaluacion['respuestas'], 1):
        criterios_str = ', '.join([str(c) for c in resp['criterios_vinculados']])
        prompt += f"""
--- Respuesta {i} (ID: {resp['respuesta_id']}) ---
Pregunta: {resp['pregunta']}
Respuesta del alumno: {resp['texto_respuesta']}
Criterios a evaluar para esta respuesta: {criterios_str}

"""
    
    prompt += f"""
INSTRUCCIONES PARA LA EVALUACIÓN:

1. Evalúa CADA respuesta ÚNICAMENTE contra los criterios vinculados a esa pregunta.

2. Para cada par (respuesta, criterio), asigna:
   - Puntaje de 0.0 a 5.0 (usa decimales: 3.5, 4.0, 4.5, etc.)
   - Justificación breve (1-2 oraciones) explicando el puntaje
   - Evidencia: cita textual específica de la respuesta del alumno que sustenta tu evaluación

3. Sé apropiado para el nivel educativo indicado:
   - Primaria: lenguaje simple, no muy exigente
   - Secundaria: mayor rigor conceptual
   - Evalúa según la edad del estudiante

4. Escala de puntajes:
   - 0.0 - 1.0: No demuestra comprensión / respuesta incorrecta o vacía
   - 1.5 - 2.5: Comprensión muy básica / errores significativos
   - 3.0 - 3.5: Comprensión parcial / respuesta incompleta
   - 4.0 - 4.5: Buena comprensión / respuesta adecuada con detalles menores faltantes
   - 5.0: Excelente comprensión / respuesta completa y precisa

5. Al final, proporciona:
   - Diagnóstico general (2-3 oraciones sobre el desempeño global del estudiante)
   - 2-3 fortalezas identificadas (aspectos que el alumno maneja bien)
   - 2-3 áreas de mejora (aspectos a reforzar)

FORMATO DE RESPUESTA REQUERIDO (JSON válido, sin texto adicional):

{{
  "alumno_id": {datos_evaluacion['alumno']['alumno_id']},
  "evaluacion_id": {datos_evaluacion['evaluacion_id']},
  "evaluaciones": [
    {{
      "respuesta_id": 1,
      "pregunta": "texto de la pregunta evaluada",
      "criterio_id": 1,
      "criterio_nombre": "nombre del criterio",
      "puntaje_obtenido": 4.0,
      "puntaje_maximo": 5.0,
      "justificacion": "explicación clara y concisa del puntaje asignado",
      "evidencia": "cita textual exacta de la respuesta del alumno"
    }}
  ],
  "diagnostico_general": "texto del diagnóstico general del estudiante",
  "fortalezas": ["fortaleza 1", "fortaleza 2", "fortaleza 3"],
  "areas_mejora": ["área 1", "área 2"]
}}

IMPORTANTE:
- Devuelve ÚNICAMENTE el JSON, sin texto adicional antes o después
- Usa los IDs exactos proporcionados en el contexto
- Incluye una entrada en "evaluaciones" por cada par (respuesta, criterio vinculado)
- Si una pregunta tiene 3 criterios vinculados, debe haber 3 entradas en "evaluaciones" para esa respuesta_id
- Las comillas dentro de textos deben escaparse correctamente para JSON válido
- No inventes información, basa tu evaluación únicamente en lo que el alumno escribió
- Sé constructivo en las justificaciones y sugerencias

Genera la evaluación ahora:
"""
    
    return prompt


def construir_prompt_simple(pregunta, respuesta, criterio_nombre, criterio_descripcion):
    """
    Versión simplificada para pruebas rápidas (un solo criterio)
    
    Args:
        pregunta (str): Texto de la pregunta
        respuesta (str): Respuesta del alumno
        criterio_nombre (str): Nombre del criterio
        criterio_descripcion (str): Descripción del criterio
    
    Returns:
        str: Prompt simplificado
    """
    
    prompt = f"""Eres un evaluador educativo. Evalúa esta respuesta según el criterio especificado.

PREGUNTA:
{pregunta}

RESPUESTA DEL ALUMNO:
{respuesta}

CRITERIO DE EVALUACIÓN:
{criterio_nombre}: {criterio_descripcion}

Asigna un puntaje de 0.0 a 5.0 y explica brevemente tu evaluación.

Responde en formato JSON:
{{
  "puntaje": 4.0,
  "justificacion": "tu explicación aquí",
  "evidencia": "cita de la respuesta"
}}
"""
    
    return prompt
