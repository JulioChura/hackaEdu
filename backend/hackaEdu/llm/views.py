"""
LLM Views - Endpoints para generar contenido con IA
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import GenerateReadingSerializer, GenerateQuestionsSerializer, EvaluateAnswerSerializer
from .llm_service import LLMService


class LLMViewSet(viewsets.ViewSet):
    """
    ViewSet para generar contenido con IA
    
    Endpoints:
      POST /api/llm/create-reading-with-questions/  - Generar lectura + preguntas
      POST /api/llm/generate-reading/               - Generar lectura
      POST /api/llm/generate-questions/             - Generar preguntas
      POST /api/llm/evaluate-answer/                - Evaluar respuesta
    """
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_reading_with_questions(self, request):
        """
        Crea lectura + preguntas en UNA sola llamada (RECOMENDADO)
        
        POST /api/llm/create-reading-with-questions/
        Body: {"tema": "inteligencia artificial", "nivel": "B1", "cantidad_preguntas": 5}
        """
        tema = request.data.get('tema')
        nivel = request.data.get('nivel')
        cantidad = request.data.get('cantidad_preguntas', 5)
        
        if not tema or not nivel:
            return Response(
                {"error": "tema y nivel son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultado = LLMService.create_reading_with_questions(tema, nivel, cantidad)
        
        if not resultado.get('success'):
            return Response(
                {"error": resultado.get('error')},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response(resultado)
    
    @action(detail=False, methods=['post'], serializer_class=GenerateReadingSerializer)
    def generate_reading(self, request):
        """
        Genera una lectura sobre un tema específico
        
        POST /api/llm/generate-reading/
        Body: {"tema": "inteligencia artificial", "nivel": "B1"}
        """
        serializer = GenerateReadingSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        tema = serializer.validated_data['tema']
        nivel = serializer.validated_data['nivel']
        
        resultado = LLMService.generate_reading(tema, nivel)
        
        if not resultado.get('success'):
            return Response(
                {"error": resultado.get('error', 'Error generando lectura')},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({
            "titulo": resultado['titulo'],
            "contenido": resultado['contenido'],
            "palabras": resultado['palabras']
        })
    
    @action(detail=False, methods=['post'], serializer_class=GenerateQuestionsSerializer)
    def generate_questions(self, request):
        """
        Genera preguntas para una lectura
        
        POST /api/llm/generate-questions/
        Body: {"lectura": "...", "nivel": "B1", "cantidad": 5}
        """
        serializer = GenerateQuestionsSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        lectura = serializer.validated_data['lectura']
        nivel = serializer.validated_data['nivel']
        cantidad = serializer.validated_data.get('cantidad', 5)
        
        resultado = LLMService.generate_questions(lectura, nivel, cantidad)
        
        if not resultado.get('success'):
            return Response(
                {"error": resultado.get('error', 'Error generando preguntas')},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({"preguntas": resultado['preguntas']})
    
    @action(detail=False, methods=['post'], serializer_class=EvaluateAnswerSerializer)
    def evaluate_answer(self, request):
        """
        Evalúa una respuesta del usuario
        
        POST /api/llm/evaluate-answer/
        Body: {"pregunta": "...", "respuesta_usuario": "...", "respuesta_correcta": "...", "nivel": "B1"}
        """
        serializer = EvaluateAnswerSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        pregunta = serializer.validated_data['pregunta']
        respuesta_usuario = serializer.validated_data['respuesta_usuario']
        respuesta_correcta = serializer.validated_data['respuesta_correcta']
        nivel = serializer.validated_data['nivel']
        
        resultado = LLMService.evaluate_answer(pregunta, respuesta_usuario, respuesta_correcta, nivel)
        
        if not resultado.get('success'):
            return Response(
                {"error": resultado.get('error', 'Error evaluando respuesta')},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({
            "es_correcta": resultado['es_correcta'],
            "puntos": resultado['puntos'],
            "feedback": resultado['feedback']
        })