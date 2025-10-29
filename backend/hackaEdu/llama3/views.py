from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .evaluador import EvaluadorIA
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def evaluar_respuestas(request):
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
    
    evaluador = EvaluadorIA()
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
    Verifica la disponibilidad de Groq API y/o Ollama según configuración
    """
    evaluador = EvaluadorIA()
    resultado = evaluador.verificar_conexion_ia()
    
    if resultado['disponible']:
        return Response(resultado, status=status.HTTP_200_OK)
    else:
        return Response(resultado, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def prueba_prompt(request):
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
