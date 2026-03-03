"""
Views para app usuarios - Endpoints del dashboard
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .dashboard_service import DashboardService


def _build_player_entry(ranking_obj, request_user_id, request):
    """Converts a Ranking instance to the dict the frontend expects."""
    user = ranking_obj.usuario
    # Avatar: prefer uploaded file, then Google picture
    avatar_url = ""
    if user.avatar:
        avatar_url = request.build_absolute_uri(user.avatar.url)
    elif hasattr(user, 'google_picture') and user.google_picture:
        avatar_url = user.google_picture

    # Level code from ProgresionNivel
    try:
        level = user.progresion.nivel_actual.codigo
    except Exception:
        level = "A1"

    return {
        "userId": user.id,
        "rank": ranking_obj.posicion,
        "name": user.get_full_name() or user.email,
        "avatar": avatar_url,
        "level": level,
        "points": ranking_obj.puntos_totales,
        "isCurrentUser": user.id == request_user_id,
    }


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para endpoints del dashboard
    
    Devuelve exactamente la estructura que el frontend espera.
    Todos los nombres de campos coinciden con lo que el frontend espera.
    """
    permission_classes = [IsAuthenticated]
    
    # ENDPOINT: GET /usuarios/dashboard/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener datos básicos del estudiante autenticado"""
        data = DashboardService.get_student_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/progress/
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """Obtener datos de progreso del estudiante"""
        data = DashboardService.get_progress_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/streak/
    @action(detail=False, methods=['get'])
    def streak(self, request):
        """Obtener datos de racha del estudiante"""
        data = DashboardService.get_streak_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/active-courses/
    @action(detail=False, methods=['get'])
    def active_courses(self, request):
        """Obtener cursos activos (lecturas) del estudiante"""
        data = DashboardService.get_active_courses(request.user)

        # Asegurar que las URLs de thumbnail sean absolutas para que el frontend
        # (que puede estar en otro host/puerto) pueda cargarlas directamente.
        processed = []
        for item in data:
            thumb = item.get('courseThumbnail') or ''
            if thumb.startswith('http://') or thumb.startswith('https://'):
                item['courseThumbnail'] = thumb
            elif thumb.startswith('/'):
                item['courseThumbnail'] = request.build_absolute_uri(thumb)
            elif thumb:
                # Path relativo sin leading slash
                item['courseThumbnail'] = request.build_absolute_uri('/' + thumb)
            else:
                # Fallback genérico
                item['courseThumbnail'] = request.build_absolute_uri('/media/categorias/general.avif')

            processed.append(item)

        return Response(processed)
    
    # ENDPOINT: GET /usuarios/dashboard/ranking/
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        """Obtener datos de ranking del usuario"""
        data = DashboardService.get_ranking_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/achievements/
    @action(detail=False, methods=['get'])
    def achievements(self, request):
        """Obtener logros obtenidos por el usuario"""
        data = DashboardService.get_achievements_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/global-ranking/
    @action(detail=False, methods=['get'], url_path='global-ranking')
    def global_ranking(self, request):
        """
        Ranking global completo para la página de Ranking.

        Query params:
          - limit (int, default 50): rows to return in the leaderboard section

        Response:
        {
          userRank: int,
          userPoints: int,
          userTopPercentage: int,
          totalUsers: int,
          topThree: [PlayerEntry],
          leaderboard: [PlayerEntry],   # positions 4+ (user row always included)
        }

        PlayerEntry:
        {
          userId, rank, name, avatar, level, points, isCurrentUser
        }
        """
        from ranking.models import Ranking

        limit = min(int(request.query_params.get('limit', 50)), 200)

        # Recalculate so positions are fresh (lightweight - O(n) update)
        Ranking.recalcular_ranking_global()

        total_users = Ranking.objects.count()
        uid = request.user.id

        # Current user's rank info
        user_rank = 0
        user_points = 0
        user_top_pct = 0
        try:
            ur = Ranking.objects.get(usuario=request.user)
            user_rank = ur.posicion
            user_points = ur.puntos_totales
            if total_users > 0:
                user_top_pct = max(1, round((total_users - user_rank) / total_users * 100))
        except Ranking.DoesNotExist:
            pass

        # Top 3
        top_qs = (
            Ranking.objects
            .select_related('usuario', 'usuario__progresion', 'usuario__progresion__nivel_actual')
            .order_by('posicion')[:3]
        )
        top_three = [_build_player_entry(r, uid, request) for r in top_qs]

        # Leaderboard positions 4..limit
        board_qs = (
            Ranking.objects
            .select_related('usuario', 'usuario__progresion', 'usuario__progresion__nivel_actual')
            .order_by('posicion')[3:limit]
        )
        leaderboard = [_build_player_entry(r, uid, request) for r in board_qs]

        # Ensure current user is always visible in leaderboard if > pos 3
        user_in_board = any(p['isCurrentUser'] for p in leaderboard)
        user_in_top = any(p['isCurrentUser'] for p in top_three)
        if not user_in_board and not user_in_top and user_rank > 3:
            try:
                ur_obj = Ranking.objects.select_related(
                    'usuario', 'usuario__progresion', 'usuario__progresion__nivel_actual'
                ).get(usuario=request.user)
                leaderboard.append(_build_player_entry(ur_obj, uid, request))
            except Ranking.DoesNotExist:
                pass

        return Response({
            'userRank': user_rank,
            'userPoints': user_points,
            'userTopPercentage': user_top_pct,
            'totalUsers': total_users,
            'topThree': top_three,
            'leaderboard': leaderboard,
        })

    # ENDPOINT (BONUS): GET /usuarios/dashboard/full/
    @action(detail=False, methods=['get'])
    def full(self, request):
        """Obtener TODOS los datos del dashboard en una sola llamada"""
        data = DashboardService.get_full_dashboard(request.user)

        # Procesar thumbnails en activeCourses para devolver URLs absolutas
        active = data.get('activeCourses') or []
        processed = []
        for item in active:
            thumb = item.get('courseThumbnail') or ''
            if thumb.startswith('http://') or thumb.startswith('https://'):
                item['courseThumbnail'] = thumb
            elif thumb.startswith('/'):
                item['courseThumbnail'] = request.build_absolute_uri(thumb)
            elif thumb:
                item['courseThumbnail'] = request.build_absolute_uri('/' + thumb)
            else:
                item['courseThumbnail'] = request.build_absolute_uri('/media/categorias/general.avif')

            processed.append(item)

        data['activeCourses'] = processed
        return Response(data)
