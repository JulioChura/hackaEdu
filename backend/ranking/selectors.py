"""
Ranking Selectors - Queries optimizadas para datos de ranking

Los selectors son funciones puras que solo leen datos de BD.
No tienen efectos secundarios.
"""

from .models import Ranking, RachaUsuario


def get_user_ranking(user):
    """
    Obtiene el ranking del usuario.
    
    Returns:
        Ranking object o None si no existe
    """
    try:
        return user.ranking
    except Ranking.DoesNotExist:
        return None


def get_top_players(limit=3):
    """
    Obtiene los top jugadores del ranking.
    
    Args:
        limit: Número de jugadores a retornar (default: 3)
    
    Optimización:
    - select_related('usuario') para evitar N+1 queries
    - Order by posicion (ya tiene index)
    """
    return Ranking.objects.select_related('usuario').order_by('posicion')[:limit]


def get_user_streak(user):
    """
    Obtiene los datos de racha del usuario.
    
    Returns:
        RachaUsuario object o None si no existe
    """
    try:
        return user.racha
    except RachaUsuario.DoesNotExist:
        return None
