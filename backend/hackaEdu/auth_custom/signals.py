"""
SIGNALS - Módulo de Autenticación
===================================
🔧 REUTILIZABLE EN OTROS PROYECTOS: Sí

Este módulo contiene las señales (signals) que se ejecutan automáticamente
cuando se crean nuevos usuarios. Se disparan INDEPENDIENTEMENTE del método
de creación (formulario, Google OAuth, admin, etc.)

Flujo:
  1. User created (cualquier método) → post_save signal dispara
  2. Verifica si es la PRIMERA VEZ (signal recibido 'created=True')
  3. Crea: ProgresionNivel, RachaUsuario, Ranking (si existen en el proyecto)

⚠️ IMPORTANTE: Este módulo debe ser importado en apps.py en el método ready()
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.apps import apps

CustomUser = get_user_model()


@receiver(post_save, sender=CustomUser)
def crear_datos_iniciales_usuario(sender, instance, created, **kwargs):
    """
    ✨ SIGNAL: Se ejecuta cada vez que se crea un CustomUser
    
    Crea automáticamente los datos iniciales del usuario:
      - Progresión de nivel (comienza en A1)
      - Racha de usuario
      - Entrada en ranking
    
    📌 Reutilizable: Sí (compatible con cualquier CustomUser)
    
    Args:
        sender: Modelo que envía el signal (CustomUser)
        instance: Instancia del usuario recién creado
        created: Boolean que indica si fue CREADO (True) o ACTUALIZADO (False)
        **kwargs: Argumentos adicionales del signal
    """
    
    # Solo actuar si el usuario fue CREADO (no actualizado)
    if not created:
        return
    
    # Intentar crear ProgresionNivel si el app existe
    try:
        # ✅ Evitamos import directo al inicio para prevenir circular imports
        ProgresionNivel = apps.get_model('usuarios', 'ProgresionNivel')
        NivelCEFR = apps.get_model('niveles', 'NivelCEFR')
        
        # Obtener nivel inicial (A1)
        nivel_inicial = NivelCEFR.objects.get(codigo='A1')
        
        # Crear progresión inicial
        ProgresionNivel.objects.get_or_create(
            usuario=instance,
            defaults={
                'nivel_actual': nivel_inicial,
                'puntos_acumulativos': 0,
                'puntos_en_nivel': 0,
                'lecturas_completadas_en_nivel': 0,
                'promedio_puntos_en_nivel': 0.00,
            }
        )
    except (LookupError, Exception) as e:
        # LookupError: Apps no están disponibles
        # Exception: Nivel A1 no existe
        print(f"⚠️ No se pudo crear ProgresionNivel: {e}")
    
    # Intentar crear RachaUsuario si el app existe
    try:
        RachaUsuario = apps.get_model('ranking', 'RachaUsuario')
        
        RachaUsuario.objects.get_or_create(
            usuario=instance,
            defaults={
                'dias_consecutivos': 0,
            }
        )
    except (LookupError, Exception) as e:
        print(f"⚠️ No se pudo crear RachaUsuario: {e}")
    
    # Intentar crear Ranking si el app existe
    try:
        Ranking = apps.get_model('ranking', 'Ranking')
        
        Ranking.objects.get_or_create(
            usuario=instance,
            defaults={
                'posicion': 0,
            }
        )
    except (LookupError, Exception) as e:
        print(f"⚠️ No se pudo crear Ranking: {e}")
    
    # Intentar crear PreferenciasUsuario si el app existe
    try:
        PreferenciasUsuario = apps.get_model('usuarios', 'PreferenciasUsuario')
        
        PreferenciasUsuario.objects.get_or_create(
            usuario=instance,
            defaults={
                'dificultad_inicial': 'BASIC',
            }
        )
    except (LookupError, Exception) as e:
        print(f"⚠️ No se pudo crear PreferenciasUsuario: {e}")
