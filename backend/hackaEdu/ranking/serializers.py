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
    Datos de racha de días para dashboard
    
    Estructura esperada:
    {
        currentStreak: 5,
        completedDaysThisWeek: [true, true, true, true, true, false, false]
    }
    """
    currentStreak = serializers.SerializerMethodField()
    completedDaysThisWeek = serializers.SerializerMethodField()
    
    def get_currentStreak(self, obj):
        """Días consecutivos actuales"""
        try:
            return obj.racha.dias_consecutivos
        except:
            return 0
    
    def get_completedDaysThisWeek(self, obj):
        """Array de 7 días de la semana [lunes, martes, ..., domingo]"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Obtener últimos 7 días
        hoy = timezone.now().date()
        
        completados = []
        try:
            # Aquí necesitarías una tabla que registre lecturas por día
            # Por ahora retornamos array de 7 elementos basados en ultima_lectura_fecha
            racha = obj.racha
            for i in range(7):
                dia = hoy - timedelta(days=6-i)
                # Si la última lectura fue hace X días, la incluimos
                completados.append(dia == racha.ultima_lectura_fecha or False)
        except:
            completados = [False] * 7
        
        return completados
    
    class Meta:
        fields = ['currentStreak', 'completedDaysThisWeek']
