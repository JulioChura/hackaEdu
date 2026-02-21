"""
Script para cargar datos iniciales en la base de datos
Ejecutar: python manage.py shell < initialize_data.py
"""

from niveles.models import NivelCEFR
from logros.models import Logro
from contenido.models import Modalidad, Categoria
from habilidades.models import CriterioHabilidad

# ============================================================
# 1. CREAR NIVELES CEFR
# ============================================================

print("📚 Inicializando Niveles CEFR...")

niveles_data = [
    {
        'codigo': 'A1',
        'nombre': 'Beginner',
        'categoria': 'BASICO',
        'vocab_min': 500,
        'vocab_max': 1000,
        'cantidad_preguntas': 10,
        'puntos_requeridos': 50,
        'multiplicador_puntos': 1.0,
    },
    {
        'codigo': 'A2',
        'nombre': 'Elementary',
        'categoria': 'BASICO',
        'vocab_min': 750,
        'vocab_max': 1200,
        'cantidad_preguntas': 10,
        'puntos_requeridos': 50,
        'multiplicador_puntos': 1.0,
    },
    {
        'codigo': 'B1',
        'nombre': 'Intermediate',
        'categoria': 'INTERMEDIO',
        'vocab_min': 1000,
        'vocab_max': 1500,
        'cantidad_preguntas': 12,
        'puntos_requeridos': 60,
        'multiplicador_puntos': 1.5,
    },
    {
        'codigo': 'B2',
        'nombre': 'Upper Intermediate',
        'categoria': 'INTERMEDIO',
        'vocab_min': 1200,
        'vocab_max': 1800,
        'cantidad_preguntas': 12,
        'puntos_requeridos': 60,
        'multiplicador_puntos': 1.5,
    },
    {
        'codigo': 'C1',
        'nombre': 'Advanced',
        'categoria': 'AVANZADO',
        'vocab_min': 1500,
        'vocab_max': 2500,
        'cantidad_preguntas': 15,
        'puntos_requeridos': 70,
        'multiplicador_puntos': 2.0,
    },
    {
        'codigo': 'C2',
        'nombre': 'Mastery',
        'categoria': 'AVANZADO',
        'vocab_min': 2000,
        'vocab_max': 3000,
        'cantidad_preguntas': 15,
        'puntos_requeridos': 70,
        'multiplicador_puntos': 2.0,
    },
]

for nivel_data in niveles_data:
    nivel, created = NivelCEFR.objects.get_or_create(
        codigo=nivel_data['codigo'],
        defaults=nivel_data
    )
    status = "✅ Creado" if created else "⏭️ Ya existe"
    print(f"  {status}: {nivel.codigo} - {nivel.nombre}")

# ============================================================
# 2. CREAR MODALIDADES
# ============================================================

print("\n🎬 Inicializando Modalidades...")

modalidades_data = [
    {
        'codigo': 'IA_GENERADA',
        'nombre': 'Generada por IA',
        'descripcion': 'Lectura generada automáticamente por IA',
        'activa': True,
    },
    {
        'codigo': 'TEXTO_SUBIDO',
        'nombre': 'Texto Subido',
        'descripcion': 'Texto proporcionado manualmente',
        'activa': True,
    },
    {
        'codigo': 'PDF_SUBIDO',
        'nombre': 'PDF Subido',
        'descripcion': 'PDF convertido a texto',
        'activa': True,
    },
    {
        'codigo': 'API_NOTICIAS',
        'nombre': 'API Noticias',
        'descripcion': 'Contenido de noticias externas',
        'activa': True,
    },
]

for modalidad_data in modalidades_data:
    modalidad, created = Modalidad.objects.get_or_create(
        codigo=modalidad_data['codigo'],
        defaults=modalidad_data
    )
    status = "✅ Creado" if created else "⏭️ Ya existe"
    print(f"  {status}: {modalidad.nombre}")

# ============================================================
# 3. CREAR CATEGORÍAS
# ============================================================

print("\n📁 Inicializando Categorías...")

categorias_data = [
    {'codigo': 'tecnologia', 'nombre': 'Tecnología', 'icono': '💻'},
    {'codigo': 'ciencia', 'nombre': 'Ciencia', 'icono': '🔬'},
    {'codigo': 'negocios', 'nombre': 'Negocios', 'icono': '💼'},
    {'codigo': 'salud', 'nombre': 'Salud', 'icono': '⚕️'},
    {'codigo': 'viajes', 'nombre': 'Viajes', 'icono': '✈️'},
    {'codigo': 'cultura', 'nombre': 'Cultura', 'icono': '🎭'},
    {'codigo': 'deportes', 'nombre': 'Deportes', 'icono': '⚽'},
    {'codigo': 'educacion', 'nombre': 'Educación', 'icono': '🎓'},
    {'codigo': 'general', 'nombre': 'General', 'icono': '📖'},
]

for categoria_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        codigo=categoria_data['codigo'],
        defaults=categoria_data
    )
    status = "✅ Creado" if created else "⏭️ Ya existe"
    print(f"  {status}: {categoria.nombre}")

# ============================================================
# 4. CREAR CRITERIOS DE HABILIDAD
# ============================================================

print("\n🎯 Inicializando Criterios de Habilidad...")

criterios_data = [
    {'codigo': 'vocabulario', 'nombre': 'Vocabulario', 'descripcion': 'Comprensión de vocabulario', 'peso_evaluacion': 2},
    {'codigo': 'gramática', 'nombre': 'Gramática', 'descripcion': 'Comprensión de estructura gramatical', 'peso_evaluacion': 2},
    {'codigo': 'comprensión_general', 'nombre': 'Comprensión General', 'descripcion': 'Comprensión general del texto', 'peso_evaluacion': 3},
    {'codigo': 'inferencia', 'nombre': 'Inferencia', 'descripcion': 'Capacidad de inferir información', 'peso_evaluacion': 2},
    {'codigo': 'detalles_específicos', 'nombre': 'Detalles Específicos', 'descripcion': 'Identificación de detalles específicos', 'peso_evaluacion': 1},
]

for criterio_data in criterios_data:
    criterio, created = CriterioHabilidad.objects.get_or_create(
        codigo=criterio_data['codigo'],
        defaults=criterio_data
    )
    status = "✅ Creado" if created else "⏭️ Ya existe"
    print(f"  {status}: {criterio.nombre} (Peso: {criterio.peso_evaluacion})")

# ============================================================
# 5. CREAR LOGROS
# ============================================================

print("\n🏆 Inicializando Logros...")

logros_data = [
    {
        'codigo': 'primer_paso',
        'nombre': 'Primer Paso',
        'descripcion': 'Completa tu registro',
        'puntos_recompensa': 5,
        'icono': '🎯',
        'criterios': {},
    },
    {
        'codigo': 'estudiante_dedicado',
        'nombre': 'Estudiante Dedicado',
        'descripcion': 'Completa tu primera lectura',
        'puntos_recompensa': 10,
        'icono': '📚',
        'criterios': {},
    },
    {
        'codigo': 'domina_a1',
        'nombre': 'Domina A1',
        'descripcion': 'Alcanza nivel A2',
        'puntos_recompensa': 25,
        'icono': '🏆',
        'criterios': {'nivel': 'A2'},
    },
    {
        'codigo': 'en_ascenso',
        'nombre': 'En Ascenso',
        'descripcion': 'Alcanza nivel B1',
        'puntos_recompensa': 50,
        'icono': '🚀',
        'criterios': {'nivel': 'B1'},
    },
    {
        'codigo': 'erudito',
        'nombre': 'Erudito',
        'descripcion': 'Alcanza nivel C1',
        'puntos_recompensa': 75,
        'icono': '📖',
        'criterios': {'nivel': 'C1'},
    },
    {
        'codigo': 'maestro_absoluto',
        'nombre': 'Maestro Absoluto',
        'descripcion': 'Alcanza nivel C2 (máximo)',
        'puntos_recompensa': 100,
        'icono': '👑',
        'criterios': {'nivel': 'C2'},
    },
    {
        'codigo': 'leyenda_global',
        'nombre': 'Leyenda Global',
        'descripcion': 'Alcanza top 10 en ranking',
        'puntos_recompensa': 150,
        'icono': '🌟',
        'criterios': {'posicion': '<=10'},
    },
    {
        'codigo': 'imparable',
        'nombre': 'Imparable',
        'descripcion': 'Mantén una racha de 7 días consecutivos',
        'puntos_recompensa': 20,
        'icono': '🔥',
        'criterios': {'dias_consecutivos': 7},
    },
    {
        'codigo': 'perseverante',
        'nombre': 'Perseverante',
        'descripcion': 'Completa 100 lecturas',
        'puntos_recompensa': 50,
        'icono': '💪',
        'criterios': {'lecturas_completadas': 100},
    },
]

for logro_data in logros_data:
    logro, created = Logro.objects.get_or_create(
        codigo=logro_data['codigo'],
        defaults=logro_data
    )
    status = "✅ Creado" if created else "⏭️ Ya existe"
    print(f"  {status}: {logro.nombre} (+{logro.puntos_recompensa}pts)")

# ============================================================
# FIN
# ============================================================

print("\n✨ ¡Inicialización completada!")
print(f"  - Niveles CEFR: {len(niveles_data)}")
print(f"  - Modalidades: {len(modalidades_data)}")
print(f"  - Categorías: {len(categorias_data)}")
print(f"  - Criterios: {len(criterios_data)}")
print(f"  - Logros: {len(logros_data)}")
