from django.db import transaction
from django.utils import timezone

from contenido.models import Pregunta
from .models import Sesion, Respuesta
from .helpers import compute_duracion, compute_puntajes, normalize_skills
from .selectors import (
    get_active_session,
    get_completed_session,
    get_latest_session_by_lectura,
    get_lectura_by_id,
    get_session_by_id_user,
)
from datetime import timedelta
from niveles.config import LEVEL_ORDER, POINTS_TO_LEVEL_UP, POINTS_MULTIPLIER


class SessionService:
    @staticmethod
    def iniciar_sesion(user, lectura_id, skills_objetivo=None, tiempo_total_segundos=900):
        lectura = get_lectura_by_id(lectura_id)
        if not lectura:
            return None, 'LECTURA_NO_ENCONTRADA'

        sesion_activa = get_active_session(user, lectura)
        if sesion_activa:
            return sesion_activa, None

        sesion_completada = get_completed_session(user, lectura)
        if sesion_completada:
            return sesion_completada, None

        skills_objetivo = normalize_skills(skills_objetivo)
        total_preguntas = lectura.preguntas.count()
        tiempo_total = int(tiempo_total_segundos)

        now = timezone.now()
        sesion = Sesion.objects.create(
            usuario=user,
            lectura=lectura,
            total_preguntas=total_preguntas,
            estado='INICIADA',
            fecha_inicio=now,
            fecha_fin_plazo=now + timedelta(seconds=tiempo_total),
            tiempo_total_segundos=tiempo_total,
            tiempo_restante_segundos=tiempo_total,
            skills_objetivo=skills_objetivo
        )
        return sesion, None

    @staticmethod
    def obtener_sesion(user, sesion_id):
        sesion = get_session_by_id_user(sesion_id, user)
        if not sesion:
            return None

        # Si la sesión todavía está activa pero la fecha límite ya pasó, finalizarla automáticamente
        if sesion.estado in ['INICIADA', 'EN_PROGRESO'] and sesion.fecha_fin_plazo:
            now = timezone.now()
            if now >= sesion.fecha_fin_plazo:
                # finalizar sin respuestas adicionales (se utilizarán las guardadas)
                SessionService.finalizar_sesion(user, sesion.id, respuestas=[], tiempo_restante_segundos=0)
                # recargar sesión finalizada
                sesion = get_session_by_id_user(sesion_id, user)

        return sesion

    @staticmethod
    def obtener_estado(user, lectura_id):
        sesion = get_latest_session_by_lectura(user, lectura_id)
        if not sesion:
            return {'estado': 'NO_INICIADA'}
        return {'estado': sesion.estado, 'sesion_id': sesion.id}

    @staticmethod
    def guardar_progreso(user, sesion_id, respuestas, tiempo_restante_segundos=None):
        sesion = get_session_by_id_user(sesion_id, user)
        if not sesion:
            return None, 'SESION_NO_ENCONTRADA'
        if sesion.estado == 'COMPLETADA':
            return None, 'SESION_COMPLETADA'

        with transaction.atomic():
            SessionService._upsert_respuestas(sesion, respuestas)

            update_fields = ['estado']
            if tiempo_restante_segundos is not None:
                sesion.tiempo_restante_segundos = max(int(tiempo_restante_segundos), 0)
                sesion.duracion_segundos = compute_duracion(
                    sesion.tiempo_total_segundos,
                    sesion.tiempo_restante_segundos
                )
                update_fields.extend(['tiempo_restante_segundos', 'duracion_segundos'])

            sesion.estado = 'EN_PROGRESO'
            sesion.save(update_fields=update_fields)

        return sesion, None

    @staticmethod
    def finalizar_sesion(user, sesion_id, respuestas, tiempo_restante_segundos=None):
        sesion = get_session_by_id_user(sesion_id, user)
        if not sesion:
            return None, 'SESION_NO_ENCONTRADA'
        if sesion.estado == 'COMPLETADA':
            return sesion, None

        with transaction.atomic():
            SessionService._upsert_respuestas(sesion, respuestas)
            respuestas_qs = sesion.respuestas.all()
            puntaje_total, puntajes_por_criterio = compute_puntajes(respuestas_qs)

            if tiempo_restante_segundos is not None:
                sesion.tiempo_restante_segundos = max(int(tiempo_restante_segundos), 0)

            sesion.estado = 'COMPLETADA'
            sesion.puntaje_total = puntaje_total
            sesion.puntajes_por_criterio = puntajes_por_criterio
            sesion.fecha_fin = timezone.now()
            sesion.duracion_segundos = compute_duracion(
                sesion.tiempo_total_segundos,
                sesion.tiempo_restante_segundos
            )
            sesion.save(
                update_fields=[
                    'estado', 'puntaje_total', 'puntajes_por_criterio',
                    'fecha_fin', 'duracion_segundos', 'tiempo_restante_segundos'
                ]
            )

            # Propagar puntos y actualizar racha
            SessionService._post_session_updates(user, sesion)

        return sesion, None

    @staticmethod
    def _post_session_updates(user, sesion):
        """
        Actualiza progresión de nivel, puntos y racha tras completar una sesión.
        Se ejecuta dentro de la transacción de finalizar_sesion.
        """
        from usuarios.models import ProgresionNivel, PerfilUsuario
        from ranking.models import RachaUsuario, Ranking

        # ── 1. Puntos y nivel ──────────────────────────────────────────────────
        try:
            progresion = ProgresionNivel.objects.select_related('nivel_actual').get(usuario=user)
            nivel = progresion.nivel_actual
            # Multiplicador: desde BD primero, config como fallback
            multiplicador = float(nivel.multiplicador_puntos) if nivel.multiplicador_puntos else \
                POINTS_MULTIPLIER.get(nivel.codigo, 1.0)
            puntos_ganados = round(float(sesion.puntaje_total) * multiplicador)

            progresion.puntos_acumulativos += puntos_ganados
            progresion.puntos_en_nivel += puntos_ganados
            progresion.lecturas_completadas_en_nivel += 1

            # Umbral de nivel: desde BD primero, config como fallback
            umbral = nivel.puntos_requeridos if nivel.puntos_requeridos else \
                POINTS_TO_LEVEL_UP.get(nivel.codigo, 9999)
            if progresion.puntos_en_nivel >= umbral:
                progresion.listo_para_ascenso = True

            progresion.save(update_fields=[
                'puntos_acumulativos', 'puntos_en_nivel',
                'lecturas_completadas_en_nivel', 'listo_para_ascenso',
            ])

            # ── 2. Perfil (puntos totales + lecturas completadas) ────────────────
            try:
                perfil = user.perfil_hackaedu
                perfil.puntos_totales = progresion.puntos_acumulativos
                perfil.lecturas_completadas += 1
                perfil.save(update_fields=['puntos_totales', 'lecturas_completadas'])
            except Exception:
                pass

        except ProgresionNivel.DoesNotExist:
            pass

        # ── 3. Racha diaria ────────────────────────────────────────────────────
        try:
            hoy = timezone.now().date()
            racha, _ = RachaUsuario.objects.get_or_create(usuario=user)
            racha.ultima_lectura_fecha = hoy
            racha.calcular_racha()  # actualiza ultimo_acceso y dias_consecutivos
        except Exception:
            pass

        # ── 4. Recalcular posición en ranking global ────────────────────────────
        try:
            Ranking.recalcular_ranking_global()
        except Exception:
            pass
        # ── 5. Verificar y otorgar logros ───────────────────────────────────────────
        try:
            from logros.services import check_and_award_logros
            check_and_award_logros(user)
        except Exception:
            pass
    @staticmethod
    def _upsert_respuestas(sesion, respuestas):
        for item in respuestas or []:
            pregunta_id = item.get('pregunta_id')
            respuesta_texto = item.get('respuesta')
            if not pregunta_id or respuesta_texto is None:
                continue
            pregunta = Pregunta.objects.filter(id=pregunta_id, lectura=sesion.lectura).first()
            if not pregunta:
                continue
            es_correcta = respuesta_texto == pregunta.respuesta_correcta
            puntos_obtenidos = pregunta.puntos_directos if es_correcta else 0

            Respuesta.objects.update_or_create(
                sesion=sesion,
                pregunta=pregunta,
                defaults={
                    'criterio': pregunta.criterio,
                    'respuesta': respuesta_texto,
                    'es_correcta': es_correcta,
                    'puntos_obtenidos': puntos_obtenidos,
                    'tiempo_respuesta_segundos': item.get('tiempo_respuesta_segundos', 0)
                }
            )
