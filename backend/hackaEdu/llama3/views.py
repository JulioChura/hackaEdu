"""
API Views para evaluación con IA
Proyecto: ReConéctate IA - Hackathon 2025
Autor: PERSONA 1 (IA + PROMPTS)
"""

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .evaluador import EvaluadorIA
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def evaluar_respuestas(request):
    """
    Endpoint principal para evaluar respuestas de un alumno con IA
    
    POST /api/llama3/evaluar-respuestas/
    
    Body (JSON):
    {
        "evaluacion_id": 123,
        "alumno_id": 456
    }
    
    Response exitosa:
    {
        "success": true,
        "reporte_id": 789,
        "data": {
            "alumno_id": 456,
            "evaluacion_id": 123,
            "evaluaciones": [...],
            "diagnostico_general": "...",
            "fortalezas": [...],
            "areas_mejora": [...]
        }
    }
    
    Response error:
    {
        "success": false,
        "error": "mensaje de error"
    }
    """
    # Validar datos de entrada
    evaluacion_id = request.data.get('evaluacion_id')
    alumno_id = request.data.get('alumno_id')
    
    if not evaluacion_id or not alumno_id:
        return Response(
            {
                "success": False,
                "error": "Se requieren los campos 'evaluacion_id' y 'alumno_id'"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Instanciar evaluador
    evaluador = EvaluadorIA()
    
    # Ejecutar evaluación
    resultado = evaluador.evaluar_respuestas(evaluacion_id, alumno_id)
    
    if resultado['success']:
        logger.info(f"Evaluación exitosa - Evaluacion: {evaluacion_id}, Alumno: {alumno_id}")
        return Response(resultado, status=status.HTTP_200_OK)
    else:
        logger.error(f"Error en evaluación: {resultado.get('error')}")
        return Response(
            {
                "success": False,
                "error": resultado.get('error', 'Error desconocido')
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def verificar_ia(request):
    """
    Endpoint para verificar que Ollama esté disponible
    
    GET /api/llama3/verificar-ia/
    
    Response:
    {
        "disponible": true/false,
        "modelos": ["llama3.2:3b", ...],
        "error": null o "mensaje de error"
    }
    """
    evaluador = EvaluadorIA()
    resultado = evaluador.verificar_conexion_ollama()
    
    if resultado['disponible']:
        return Response(resultado, status=status.HTTP_200_OK)
    else:
        return Response(resultado, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def prueba_prompt(request):
    """
    Endpoint de prueba para generar un prompt sin ejecutar la IA
    Útil para debugging y ajustar el formato del prompt
    
    POST /api/llama3/prueba-prompt/
    
    Body (JSON):
    {
        "evaluacion_id": 123,
        "alumno_id": 456
    }
    
    Response:
    {
        "prompt": "texto del prompt generado",
        "longitud": 1234
    }
    """
    evaluacion_id = request.data.get('evaluacion_id')
    alumno_id = request.data.get('alumno_id')
    
    if not evaluacion_id or not alumno_id:
        return Response(
            {"error": "Se requieren evaluacion_id y alumno_id"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        evaluador = EvaluadorIA()
        datos = evaluador._obtener_datos_evaluacion(evaluacion_id, alumno_id)
        prompt = evaluador._construir_prompt(datos)
        
        return Response({
            "prompt": prompt,
            "longitud": len(prompt),
            "num_criterios": len(datos['criterios']),
            "num_respuestas": len(datos['respuestas'])
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Vista legacy (mantener por compatibilidad)
class EvaluarAlumnoView(APIView):
    """
    Vista antigua - se mantiene por compatibilidad
    Usar 'evaluar_respuestas' en su lugar
    """
    def post(self, request):
        logger.warning("Usando vista legacy EvaluarAlumnoView - migrar a evaluar_respuestas")
        
        try:
            rubrica = request.data.get("rubrica")
            respuesta_alumno = request.data.get("respuesta_alumno")

            if not rubrica or not respuesta_alumno:
                return Response({"error": "Faltan campos"}, status=400)

            # Usar evaluador nuevo
            from .prompts import construir_prompt_simple
            prompt = construir_prompt_simple(
                pregunta="Evaluación general",
                respuesta=respuesta_alumno,
                criterio_nombre="Rúbrica",
                criterio_descripcion=rubrica
            )
            
            evaluador = EvaluadorIA()
            respuesta_ia = evaluador._llamar_ia(prompt)

            return Response({"resultado_ia": respuesta_ia}, status=200)

        except Exception as e:
            logger.error(f"Error en vista legacy: {str(e)}")
            return Response({"error": str(e)}, status=500)