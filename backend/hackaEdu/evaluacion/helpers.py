from typing import Iterable


def normalize_skills(skills_objetivo):
    if not isinstance(skills_objetivo, list):
        return []
    return [str(skill).strip() for skill in skills_objetivo if str(skill).strip()]


def compute_duracion(tiempo_total_segundos, tiempo_restante_segundos):
    try:
        total = int(tiempo_total_segundos)
        restante = int(tiempo_restante_segundos)
    except (TypeError, ValueError):
        return 0
    return max(total - restante, 0)


def compute_puntajes(respuestas_qs: Iterable):
    puntaje_total = 0.0
    puntajes_por_criterio = {}

    for respuesta in respuestas_qs:
        puntaje_total += float(respuesta.puntos_obtenidos)
        codigo = respuesta.criterio.codigo if respuesta.criterio else 'desconocido'
        if codigo not in puntajes_por_criterio:
            puntajes_por_criterio[codigo] = {'puntos': 0, 'aciertos': 0, 'intentos': 0}
        puntajes_por_criterio[codigo]['intentos'] += 1
        if respuesta.es_correcta:
            puntajes_por_criterio[codigo]['aciertos'] += 1
            puntajes_por_criterio[codigo]['puntos'] += float(respuesta.puntos_obtenidos)

    return puntaje_total, puntajes_por_criterio
