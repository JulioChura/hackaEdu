"""
Logros Selectors - Queries optimizadas para datos de logros

Los selectors son funciones puras que solo leen datos de BD.
No tienen efectos secundarios.
"""

from .models import LogroUsuario


def get_user_achievements(user, limit=None):
    """
    Obtiene los logros obtenidos por el usuario.
    
    Args:
        user: Usuario del que se quieren obtener los logros
        limit: Número máximo de logros a retornar (None = todos)
    
    Returns:
        QuerySet de LogroUsuario ordenados por fecha de obtención (más recientes primero)
    
    Optimización:
    - select_related('logro') para evitar N+1 queries
    - Ordenado por fecha de obtención descendente
    """
    queryset = LogroUsuario.objects.filter(
        usuario=user
    ).select_related('logro').order_by('-fecha_obtencion')
    
    if limit:
        queryset = queryset[:limit]
    
    return queryset
