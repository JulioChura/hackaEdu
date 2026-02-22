"""
Niveles Serializers - Serialización de datos de progresión

Cada serializer define un formato de respuesta específico.
Pueden crearse múltiples serializers para diferentes contextos.
"""

from rest_framework import serializers


class DashboardProgressDataSerializer(serializers.Serializer):
    """
    Datos de progreso del estudiante para dashboard
    
    Estructura esperada:
    {
        currentLevel: 'A2',
        levelTitle: 'Elementary Mastery',
        currentPoints: 25,
        nextLevelPoints: 40,
        nextLevel: 'B1 Intermediate'
    }
    """
    currentLevel = serializers.SerializerMethodField()
    levelTitle = serializers.SerializerMethodField()
    currentPoints = serializers.SerializerMethodField()
    nextLevelPoints = serializers.IntegerField(default=40)
    nextLevel = serializers.SerializerMethodField()
    
    def get_currentLevel(self, obj):
        """Nivel CEFR actual (ej: A2)"""
        try:
            return obj.progresion.nivel_actual.codigo
        except:
            return "A1"
    
    def get_levelTitle(self, obj):
        """Descripción del nivel (ej: Elementary Mastery)"""
        try:
            return obj.progresion.nivel_actual.descripcion
        except:
            return "Beginner"
    
    def get_currentPoints(self, obj):
        """Puntos en el nivel actual"""
        try:
            return obj.progresion.puntos_en_nivel
        except:
            return 0
    
    def get_nextLevel(self, obj):
        """Siguiente nivel"""
        try:
            nivel_actual = obj.progresion.nivel_actual
            # Obtener siguiente nivel basado en orden
            siguientes = nivel_actual.siguiente_nivel.all()
            if siguientes.exists():
                siguiente = siguientes.first()
                return f"{siguiente.codigo} {siguiente.descripcion}"
            return "Expert"
        except:
            return "B1 Intermediate"
    
    class Meta:
        fields = ['currentLevel', 'levelTitle', 'currentPoints', 'nextLevelPoints', 'nextLevel']
