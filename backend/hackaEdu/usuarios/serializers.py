"""
Usuarios Serializers - Serialización de datos de usuarios

Cada serializer define un formato de respuesta específico.
Pueden crearse múltiples serializers para diferentes contextos.
"""

from rest_framework import serializers


class DashboardStudentDataSerializer(serializers.Serializer):
    """
    Datos básicos del estudiante para el dashboard
    
    Estructura esperada por frontend:
    {
        userId: 1,
        fullName: 'Alex Chen',
        userLevelTitle: 'Advanced Learner',
        avatarUrl: 'https://...',
        isPro: false
    }
    """
    userId = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()
    userLevelTitle = serializers.SerializerMethodField()
    avatarUrl = serializers.SerializerMethodField()
    isPro = serializers.SerializerMethodField()
    
    def get_userId(self, obj):
        """ID del usuario"""
        return obj.id
    
    def get_fullName(self, obj):
        """Nombre completo: nombre + apellido"""
        return f"{obj.nombre} {obj.apellido}"
    
    def get_userLevelTitle(self, obj):
        """Título del nivel actual del usuario"""
        try:
            progresion = obj.progresion
            return f"{progresion.nivel_actual.codigo} Learner"
        except:
            return "Beginner"
    
    def get_avatarUrl(self, obj):
        """URL del avatar"""
        if obj.avatar:
            return obj.avatar.url
        # Avatar por defecto desde Google si tiene
        if obj.has_google_account():
            return obj.google_picture or ""
        return ""
    
    def get_isPro(self, obj):
        """Es usuario premium?"""
        try:
            return obj.perfil_hackaedu.es_premium
        except:
            return False
    
    class Meta:
        fields = ['userId', 'fullName', 'userLevelTitle', 'avatarUrl', 'isPro']

