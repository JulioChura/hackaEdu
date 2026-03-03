"""
Niveles Serializers - Serialización de datos de progresión
"""

from rest_framework import serializers
from niveles.config import POINTS_TO_LEVEL_UP, LEVEL_ORDER


class DashboardProgressDataSerializer(serializers.Serializer):
    """
    Datos de progreso del estudiante para dashboard.
    Recibe el objeto `user` (CustomUser).
    """
    currentLevel = serializers.SerializerMethodField()
    levelTitle = serializers.SerializerMethodField()
    currentPoints = serializers.SerializerMethodField()
    nextLevelPoints = serializers.SerializerMethodField()
    nextLevel = serializers.SerializerMethodField()

    def get_currentLevel(self, obj):
        try:
            return obj.progresion.nivel_actual.codigo
        except Exception:
            return "A1"

    def get_levelTitle(self, obj):
        """Nombre descriptivo del nivel (ej: Beginner, Elementary…)"""
        try:
            return obj.progresion.nivel_actual.nombre
        except Exception:
            return "Beginner"

    def get_currentPoints(self, obj):
        """Puntos acumulados en el nivel actual (para barra de progreso)"""
        try:
            return obj.progresion.puntos_en_nivel
        except Exception:
            return 0

    def get_nextLevelPoints(self, obj):
        """Puntos requeridos para subir al siguiente nivel"""
        try:
            nivel = obj.progresion.nivel_actual
            # Usar el campo de la BD como fuente primaria
            if nivel.puntos_requeridos:
                return nivel.puntos_requeridos
            return POINTS_TO_LEVEL_UP.get(nivel.codigo, 100)
        except Exception:
            return 100

    def get_nextLevel(self, obj):
        """Código + nombre del siguiente nivel"""
        try:
            codigo_actual = obj.progresion.nivel_actual.codigo
            idx = LEVEL_ORDER.index(codigo_actual)
            if idx + 1 < len(LEVEL_ORDER):
                siguiente_codigo = LEVEL_ORDER[idx + 1]
                from niveles.models import NivelCEFR
                siguiente = NivelCEFR.objects.filter(codigo=siguiente_codigo).first()
                if siguiente:
                    return f"{siguiente.codigo} {siguiente.nombre}"
                return siguiente_codigo
            return "Max Level"
        except Exception:
            return "Next Level"

    class Meta:
        fields = ['currentLevel', 'levelTitle', 'currentPoints', 'nextLevelPoints', 'nextLevel']
