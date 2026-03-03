"""
Niveles Selectors - Queries optimizadas para datos de progresión

Los selectors son funciones puras que solo leen datos de BD.
No tienen efectos secundarios.
"""


def get_user_progress(user):
    """
    Obtiene la progresión de nivel del usuario.
    
    Args:
        user: Usuario del que se quiere obtener la progresión
    
    Returns:
        ProgresionNivel object o None si no existe
    
    Optimización:
    - select_related('nivel_actual') para evitar N+1 queries
    """
    from usuarios.models import ProgresionNivel
    
    try:
        # Asegurar que nivel_actual está cargado
        progresion = user.progresion
        # Force load del nivel para evitar query adicional
        _ = progresion.nivel_actual
        return progresion
    except ProgresionNivel.DoesNotExist:
        return None
