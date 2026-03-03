"""
Ranking Serializers - Serialización de datos de ranking

Cada serializer define un formato de respuesta específico.
Pueden crearse múltiples serializers para diferentes contextos.
"""

from rest_framework import serializers
from .models import Ranking, RachaUsuario


class TopPlayerSerializer(serializers.Serializer):
    """Datos de jugador en ranking"""
    userId = serializers.SerializerMethodField()
    userName = serializers.SerializerMethodField()
    avatarUrl = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    
    def get_userId(self, obj):
        return obj.usuario.id
    
    def get_userName(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"
    
    def get_avatarUrl(self, obj):
        if obj.usuario.avatar:
            return obj.usuario.avatar.url
        if obj.usuario.has_google_account():
            return obj.usuario.google_picture or ""
        return ""
    
    def get_points(self, obj):
        return obj.puntos_totales


class DashboardRankingDataSerializer(serializers.Serializer):
    """
    Datos de ranking global para dashboard
    
    Estructura esperada:
    {
        userRank: 142,
        userTopPercentage: 5,
        topPlayers: [...]
    }
    """
    userRank = serializers.SerializerMethodField()
    userTopPercentage = serializers.SerializerMethodField()
    topPlayers = serializers.SerializerMethodField()
    
    def get_userRank(self, obj):
        """Posición del usuario en el ranking"""
        try:
            return obj.ranking.posicion
        except:
            return 0
    
    def get_userTopPercentage(self, obj):
        """Percentil del usuario (ej: top 5%)"""
        try:
            posicion = obj.ranking.posicion
            total_usuarios = Ranking.objects.count()
            percentil = round((total_usuarios - posicion) / total_usuarios * 100)
            return percentil
        except:
            return 0
    
    def get_topPlayers(self, obj):
        """Top 3 jugadores"""
        rankings = Ranking.objects.select_related('usuario').order_by('posicion')[:3]
        return TopPlayerSerializer(rankings, many=True).data
    
    class Meta:
        fields = ['userRank', 'userTopPercentage', 'topPlayers']


class DashboardStreakDataSerializer(serializers.Serializer):
    """
    Datos de racha de días para dashboard.
    Espera recibir el objeto `user` (CustomUser).
    """
    currentStreak = serializers.SerializerMethodField()
    completedDaysThisWeek = serializers.SerializerMethodField()

    def get_currentStreak(self, obj):
        """Días consecutivos actuales"""
        try:
            return obj.racha.dias_consecutivos
        except Exception:
            return 0

    def get_completedDaysThisWeek(self, obj):
        """
        Array de 7 bools [lunes, martes, ..., domingo] de la semana actual.
        True = el usuario completó al menos una sesión ese día.
        """
        from django.utils import timezone
        from datetime import timedelta
        from evaluacion.models import Sesion

        hoy = timezone.now().date()
        # Inicio de la semana actual (lunes)
        inicio_semana = hoy - timedelta(days=hoy.weekday())

        completados = []
        for i in range(7):
            dia = inicio_semana + timedelta(days=i)
            tuvo_sesion = Sesion.objects.filter(
                usuario=obj,
                estado='COMPLETADA',
                fecha__date=dia,
            ).exists()
            completados.append(tuvo_sesion)

        return completados

    class Meta:
        fields = ['currentStreak', 'completedDaysThisWeek']
