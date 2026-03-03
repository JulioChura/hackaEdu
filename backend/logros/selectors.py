"""
Logros Selectors - Queries optimizadas para datos de logros

Los selectors son funciones puras que solo leen datos de BD.
No tienen efectos secundarios.
"""

from .models import Logro, LogroUsuario


def get_user_achievements(user, limit=None):
    """
    Obtiene los logros YA OBTENIDOS por el usuario.
    """
    queryset = LogroUsuario.objects.filter(
        usuario=user
    ).select_related('logro').order_by('-fecha_obtencion')

    if limit:
        queryset = queryset[:limit]

    return queryset


def get_all_achievements_for_user(user):
    """
    Retorna todos los logros con estado de desbloqueo para el usuario.

    Returns:
        list of dicts:
          {
            'logro': Logro,
            'unlocked': bool,
            'fecha_obtencion': datetime | None,
          }
    """
    unlocked_map = {
        lu.logro_id: lu.fecha_obtencion
        for lu in LogroUsuario.objects.filter(usuario=user)
    }

    result = []
    for logro in Logro.objects.all().order_by('nombre'):
        result.append({
            'logro': logro,
            'unlocked': logro.codigo in unlocked_map,
            'fecha_obtencion': unlocked_map.get(logro.codigo),
        })

    return result
