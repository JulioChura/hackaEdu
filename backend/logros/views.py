"""
Logros Views — Endpoint para listar todos los logros con estado del usuario.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .selectors import get_all_achievements_for_user

NIVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _build_progress_text(criterios: dict, user) -> str | None:
    """Genera texto de progreso para logros bloqueados."""
    from ranking.models import RachaUsuario

    texts = []
    for criterio, valor in (criterios or {}).items():
        if criterio == 'lecturas_completadas':
            try:
                actual = user.perfil_hackaedu.lecturas_completadas
            except Exception:
                actual = 0
            texts.append(f"{actual}/{valor} readings")

        elif criterio == 'nivel':
            texts.append(f"Reach level {valor}")

        elif criterio == 'dias_consecutivos':
            try:
                racha = RachaUsuario.objects.get(usuario=user)
                actual = racha.dias_consecutivos
            except Exception:
                actual = 0
            texts.append(f"{actual}/{valor} day streak")

        elif criterio == 'posicion':
            texts.append(f"Top {str(valor).replace('<=', '')} ranking")

    return " · ".join(texts) if texts else None


class LogroViewSet(viewsets.ViewSet):
    """
    GET /logros/  → lista todos los logros con estado unlocked/locked para el usuario.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = get_all_achievements_for_user(request.user)

        result = []
        unlocked_count = 0

        for item in items:
            logro = item['logro']
            unlocked = item['unlocked']
            fecha = item['fecha_obtencion']

            if unlocked:
                unlocked_count += 1

            achieved_date = None
            if fecha:
                achieved_date = f"Achieved {fecha.strftime('%b %d, %Y')}"

            progress = None if unlocked else _build_progress_text(logro.criterios, request.user)

            result.append({
                'achievementId': logro.codigo,
                'title': logro.nombre,
                'description': logro.descripcion,
                'emoji': logro.icono or '⭐',
                'unlocked': unlocked,
                'achievedDate': achieved_date,
                'progress': progress,
                'pointsReward': logro.puntos_recompensa,
            })

        return Response({
            'achievements': result,
            'unlockedCount': unlocked_count,
            'totalCount': len(result),
        })
