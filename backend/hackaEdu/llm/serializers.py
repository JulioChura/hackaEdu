"""
LLM Serializers - Serialización de requests/responses para generación de contenido
"""

from rest_framework import serializers


class GenerateBundleSerializer(serializers.Serializer):
    """Serializer para generar lectura + preguntas en una sola llamada"""

    tema = serializers.CharField(
        max_length=200,
        help_text="Tema de la lectura (ej: inteligencia artificial)"
    )
    nivel = serializers.ChoiceField(
        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
        help_text="Nivel CEFR"
    )
    categoria = serializers.CharField(
        max_length=50,
        help_text="Codigo de categoria (Categoria.codigo)"
    )
    modalidad = serializers.CharField(
        max_length=50,
        help_text="Codigo de modalidad (Modalidad.codigo)"
    )
    cantidad_preguntas = serializers.IntegerField(
        default=5,
        min_value=1,
        max_value=10,
        help_text="Cantidad de preguntas (1-10)"
    )
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True,
        help_text="Lista de skills a mejorar"
    )
