"""
Script de demostración: PK de TEXTO vs ID numérico
Ejecutar: python manage.py shell < test_pk_type.py
"""
from contenido.models import Categoria

# Obtener una categoría
cat = Categoria.objects.first()

print("=" * 60)
print("🔍 ANÁLISIS DEL PRIMARY KEY DE CATEGORIA")
print("=" * 60)
print()

# Mostrar el valor del PK
print(f"📌 Valor del PK: {cat.pk}")
print(f"📌 Tipo de dato: {type(cat.pk).__name__}")
print()

# Verificar si tiene campo 'id'
print("🔎 ¿Tiene campo 'id' numérico?")
try:
    print(f"   cat.id = {cat.id}")
    print(f"   Tipo: {type(cat.id).__name__}")
except AttributeError as e:
    print(f"   ❌ NO - {e}")
print()

# Verificar el campo 'codigo'
print("🔎 ¿Tiene campo 'codigo'?")
try:
    print(f"   cat.codigo = {cat.codigo}")
    print(f"   Tipo: {type(cat.codigo).__name__}")
    print(f"   ¿Es el PK?: {cat.codigo == cat.pk}")
except AttributeError as e:
    print(f"   ❌ NO - {e}")
print()

# Mostrar todas las categorías
print("📋 Todas las categorías en la base de datos:")
print("-" * 60)
for c in Categoria.objects.all():
    print(f"   PK: '{c.pk}' (tipo: {type(c.pk).__name__}) → {c.nombre}")
print()

# Demostrar filtrado
print("🧪 PRUEBA: Filtrar categorías")
print("-" * 60)

# Con texto (CORRECTO)
print("✅ Con TEXTO (codigo__in=['ciencia', 'tecnologia']):")
cats_texto = Categoria.objects.filter(codigo__in=['ciencia', 'tecnologia'])
print(f"   Encontradas: {cats_texto.count()} categorías")
for c in cats_texto:
    print(f"   - {c.codigo}: {c.nombre}")
print()

# Con números (INCORRECTO)
print("❌ Con NÚMEROS (codigo__in=[1, 2]):")
cats_numeros = Categoria.objects.filter(codigo__in=[1, 2])
print(f"   Encontradas: {cats_numeros.count()} categorías")
if cats_numeros.count() == 0:
    print("   ⚠️  NO SE ENCONTRARON porque los códigos NO son '1' o '2'")
print()

print("=" * 60)
print("✅ CONCLUSIÓN:")
print("=" * 60)
print("El PRIMARY KEY de Categoria es TEXTO (codigo), NO número (id)")
print("Por lo tanto, debes enviar códigos de texto desde el frontend:")
print('  categorias_preferidas: ["ciencia", "tecnologia"]')
print()
print("NO puedes enviar números:")
print('  categorias_preferidas: [1, 2]  ← ESTO NO FUNCIONA')
print("=" * 60)
