"""
LLM Views - Endpoints para generar contenido con IA
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import GenerateBundleSerializer
from .llm_service import LLMService


class LLMViewSet(viewsets.ViewSet):
    """
    ViewSet para generar contenido con IA
    
    Endpoints:
      POST /api/llm/create-reading-with-questions/  - Generar lectura + preguntas
    """
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_reading_with_questions(self, request):
        """
        Crea lectura + preguntas en UNA sola llamada (RECOMENDADO)
        
        POST /api/llm/create-reading-with-questions/
        Body: {"tema": "inteligencia artificial", "nivel": "B1", "cantidad_preguntas": 5}
        """
        serializer = GenerateBundleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tema = serializer.validated_data['tema']
        nivel = serializer.validated_data['nivel']
        cantidad = serializer.validated_data.get('cantidad_preguntas', 5)
        skills = serializer.validated_data.get('skills', [])
        
        resultado = LLMService.create_reading_with_questions(tema, nivel, cantidad, skills)
        
        if not resultado.get('success'):
            return Response(
                {"error": resultado.get('error')},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response(resultado)