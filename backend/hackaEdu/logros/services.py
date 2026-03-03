"""
Logros Services — Otorgar logros automáticamente cuando se cumplen criterios.

Se llama tras finalizar una sesión (y opcionalmente al registrarse).
"""

import logging

from .models import Logro, LogroUsuario

logger = logging.getLogger(__name__)

NIVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


def check_and_award_logros(user) -> list[str]:
    """
    Verifica TODOS los logros y otorga los que el usuario ya cumple.
    Debe llamarse DESPUÉS de que perfil, progresion y racha hayan sido actualizados.

    Returns:
        Lista de códigos de logros recién desbloqueados (para notificaciones futuras).
    """
    from usuarios.models import PerfilUsuario, ProgresionNivel
    from ranking.models import RachaUsuario, Ranking

    # ── Obtener estado actual del usuario ──────────────────────────────────────
    try:
        perfil = user.perfil_hackaedu
        lecturas = perfil.lecturas_completadas
    except Exception:
        lecturas = 0

    try:
        progresion = ProgresionNivel.objects.select_related('nivel_actual').get(usuario=user)
        nivel_actual = progresion.nivel_actual.codigo
    except Exception:
        nivel_actual = "A1"

    try:
        racha = RachaUsuario.objects.get(usuario=user)
        dias_consecutivos = racha.dias_consecutivos
    except Exception:
        dias_consecutivos = 0

    try:
        ranking_obj = Ranking.objects.get(usuario=user)
        posicion = ranking_obj.posicion or 9999
    except Exception:
        posicion = 9999

    # ── Logros ya obtenidos (lookup O(1)) ────────────────────────────────────
    ya_obtenidos = set(
        LogroUsuario.objects.filter(usuario=user).values_list('logro_id', flat=True)
    )

    nuevos = []

    for logro in Logro.objects.all():
        if logro.codigo in ya_obtenidos:
            continue

        criterios = logro.criterios or {}
        cumple = True

        for criterio, valor in criterios.items():
            if criterio == 'lecturas_completadas':
                if lecturas < int(valor):
                    cumple = False
                    break

            elif criterio == 'nivel':
                # Requiere haber alcanzado ese nivel o superior
                try:
                    idx_actual = NIVEL_ORDER.index(nivel_actual)
                    idx_req = NIVEL_ORDER.index(str(valor))
                    if idx_actual < idx_req:
                        cumple = False
                        break
                except ValueError:
                    cumple = False
                    break

            elif criterio == 'dias_consecutivos':
                if dias_consecutivos < int(valor):
                    cumple = False
                    break

            elif criterio == 'posicion':
                # Formato: '<=10'
                if str(valor).startswith('<='):
                    limite = int(str(valor)[2:])
                    if posicion > limite:
                        cumple = False
                        break

            # Criterios desconocidos: ignorar (no bloquean)

        # Logros sin criterios ({}) se otorgan siempre (ej: primer_paso al finalizar 1ª sesión)
        if cumple:
            _, created = LogroUsuario.objects.get_or_create(usuario=user, logro=logro)
            if created:
                nuevos.append(logro.codigo)
                logger.info("Logro desbloqueado: %s → %s", user.username, logro.nombre)

    return nuevos
