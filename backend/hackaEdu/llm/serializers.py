"""
LLM Serializers - Serialización de requests/responses para generación de contenido
"""

from rest_framework import serializers


class GenerateReadingSerializer(serializers.Serializer):
    """Serializer para generar lectura"""
    
    tema = serializers.CharField(
        max_length=200,
        help_text="Tema de la lectura (ej: inteligencia artificial)"
    )
    nivel = serializers.ChoiceField(
        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
        help_text="Nivel CEFR"
    )


class GenerateQuestionsSerializer(serializers.Serializer):
    """Serializer para generar preguntas"""
    
    lectura = serializers.CharField(
        help_text="Contenido de la lectura"
    )
    nivel = serializers.ChoiceField(
        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    )
    cantidad = serializers.IntegerField(
        default=5,
        min_value=1,
        max_value=10,
        help_text="Cantidad de preguntas (1-10)"
    )


class EvaluateAnswerSerializer(serializers.Serializer):
    """Serializer para evaluar respuesta"""
    
    pregunta = serializers.CharField(help_text="Texto de la pregunta")
    respuesta_usuario = serializers.CharField(help_text="Respuesta del usuario")
    respuesta_correcta = serializers.CharField(help_text="Respuesta correcta")
    nivel = serializers.ChoiceField(choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
