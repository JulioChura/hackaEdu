"""
Logros Serializers - Serialización de datos de logros/achievements

Cada serializer define un formato de respuesta específico.
Pueden crearse múltiples serializers para diferentes contextos.
"""

from rest_framework import serializers


class AchievementSerializer(serializers.Serializer):
    """Datos de un logro obtenido"""
    achievementId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    iconName = serializers.CharField()


class DashboardAchievementsDataSerializer(serializers.ListSerializer):
    """
    Datos de logros del usuario para dashboard
    
    Estructura esperada:
    [
        {
            achievementId: 1,
            title: 'First Step',
            description: 'Completed first lesson',
            iconName: 'footprint'
        }
    ]
    """
    child = AchievementSerializer()
