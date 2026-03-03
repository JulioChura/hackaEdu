"""
niveles/config.py — Configuración flexible del sistema de puntos y niveles.

Estos valores son los DEFAULTS usados cuando no se encuentran en la base de datos.
Para cambiar umbrales de nivel, editar este archivo (o actualizar los registros NivelCEFR en BD).

LEVEL_ORDER: orden ascendente de niveles CEFR.
POINTS_TO_LEVEL_UP: puntos necesarios en el nivel actual para subir al siguiente.
POINTS_MULTIPLIER: multiplicador de puntos por nivel (a más alto nivel, más valen las respuestas).
STREAK_BONUS: puntos bonus por racha de días consecutivos (clave = días mínimos, valor = puntos extra).

NOTA: los puntos por respuesta correcta se definen en llm/metrics.py (DEFAULT_POINTS_PER_QUESTION)
      y en el campo `puntos_directos` de cada Pregunta (fuente de verdad en BD).
"""

# Orden de niveles de menor a mayor
LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Puntos requeridos en el nivel para subir (fallback si no está en BD)
POINTS_TO_LEVEL_UP: dict[str, int] = {
    "A1": 50,
    "A2": 60,
    "B1": 80,
    "B2": 100,
    "C1": 130,
    "C2": 999999,   # C2 es el tope, no sube
}

# Multiplicador de puntos por nivel (fallback si no está en BD)
POINTS_MULTIPLIER: dict[str, float] = {
    "A1": 1.0,
    "A2": 1.1,
    "B1": 1.2,
    "B2": 1.4,
    "C1": 1.6,
    "C2": 2.0,
}

# Puntos bonus por racha diaria (clave = días consecutivos mínimos, valor = bonus)
STREAK_BONUS: dict[int, int] = {
    3: 1,
    5: 3,
    7: 5,
    14: 10,
    30: 20,
}
