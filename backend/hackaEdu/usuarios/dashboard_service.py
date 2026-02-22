"""
Dashboard Service - Lógica de negocio para construir datos del dashboard

El service:
- Llama a selectores de cada app para obtener datos
- Usa serializers para transformar datos  
- Contiene lógica de negocio del dashboard
"""

# Importar selectores de cada app responsable
from ranking.selectors import get_user_ranking, get_user_streak
from logros.selectors import get_user_achievements
from niveles.selectors import get_user_progress

# Importar serializers desde cada app responsable
from usuarios.serializers import DashboardStudentDataSerializer
from niveles.serializers import DashboardProgressDataSerializer
from ranking.serializers import DashboardStreakDataSerializer, DashboardRankingDataSerializer
from logros.serializers import DashboardAchievementsDataSerializer


class DashboardService:
    """Servicio central para obtener datos del dashboard"""
    
    @staticmethod
    def get_student_data(user):
        """Obtiene datos del estudiante serializados"""
        serializer = DashboardStudentDataSerializer(user)
        return serializer.data
    
    @staticmethod
    def get_progress_data(user):
        """Obtiene datos de progreso serializados"""
        progress_obj = get_user_progress(user) or user
        serializer = DashboardProgressDataSerializer(progress_obj)
        return serializer.data
    
    @staticmethod
    def get_streak_data(user):
        """Obtiene datos de racha serializados"""
        streak_obj = get_user_streak(user) or user
        serializer = DashboardStreakDataSerializer(streak_obj)
        return serializer.data
    
    @staticmethod
    def get_ranking_data(user):
        """Obtiene datos de ranking serializados"""
        ranking_obj = get_user_ranking(user) or user
        serializer = DashboardRankingDataSerializer(ranking_obj)
        return serializer.data
    
    @staticmethod
    def get_achievements_data(user):
        """Obtiene logros del usuario serializados"""
        logros = get_user_achievements(user, limit=3)
        
        # Transformar a lista de dicts con la estructura esperada
        achievements = []
        for logro_usuario in logros:
            logro = logro_usuario.logro
            achievements.append({
                'achievementId': logro.codigo,
                'title': logro.nombre,
                'description': logro.descripcion,
                'iconName': logro.icono or 'star'
            })
        
        return achievements
    
    @staticmethod
    def get_active_courses(user):
        """
        Obtiene cursos activos del usuario.
        
        TODO: Implementar lógica de asignación de cursos/lecturas a usuarios
        """
        # Por ahora retorna lista vacía
        # Cuando tengas relación entre usuario y lectura, implementarlo aquí
        return []
    
    @staticmethod
    def get_full_dashboard(user):
        """
        Obtiene todos los datos del dashboard en una sola llamada.
        
        Útil para optimizar cuando necesitas todos los datos.
        """
        return {
            'studentData': DashboardService.get_student_data(user),
            'progressData': DashboardService.get_progress_data(user),
            'streakData': DashboardService.get_streak_data(user),
            'rankingData': DashboardService.get_ranking_data(user),
            'achievementsData': DashboardService.get_achievements_data(user),
            'activeCourses': DashboardService.get_active_courses(user),
        }
