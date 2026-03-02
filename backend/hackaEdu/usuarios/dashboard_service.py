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
from contenido.models import Lectura
from evaluacion.models import Sesion


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
        # Always serialize from the `user` object. The serializer methods
        # access `obj.progresion` and handle missing progression. Passing a
        # `ProgresionNivel` instance caused attribute lookups like
        # `obj.progresion` to fail and return the default 'A1'. Ensure the
        # progression is loaded but serialize from the user.
        _ = get_user_progress(user)
        serializer = DashboardProgressDataSerializer(user)
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
        """Obtiene lecturas creadas por el usuario con progreso estimado por sesión."""
        lecturas = (
            Lectura.objects
            .filter(usuario_creador=user)
            .select_related('categoria')
            .order_by('-fecha_creacion')[:5]
        )

        active_courses = []

        for lectura in lecturas:
            sesion = (
                Sesion.objects
                .filter(usuario=user, lectura=lectura)
                .order_by('-fecha')
                .first()
            )

            if sesion and sesion.total_preguntas > 0:
                if sesion.estado == 'COMPLETADA':
                    progreso = 100
                else:
                    respuestas_count = sesion.respuestas.count()
                    progreso = min(99, round((respuestas_count / sesion.total_preguntas) * 100))
            else:
                progreso = 0

            active_courses.append({
                'courseId': lectura.id,
                'courseTitle': lectura.titulo,
                'courseCategory': lectura.categoria.nombre if lectura.categoria else 'General',
                'courseThumbnail': lectura.imagen_url or '',
                'courseProgress': progreso,
            })

        return active_courses
    
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
