"""
Script para verificar el nivel del usuario en la base de datos
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from auth_custom.models import CustomUser
from usuarios.models import PerfilUsuario, ProgresionNivel

# Obtener el primer usuario (ajusta esto si necesitas otro usuario)
user = CustomUser.objects.first()

if not user:
    print("❌ No hay usuarios en la base de datos")
    exit()

print(f"\n{'='*60}")
print(f"👤 USUARIO: {user.email}")
print(f"{'='*60}\n")

# Verificar PerfilUsuario
try:
    perfil = user.perfil_hackaedu
    print(f"✅ PERFIL USUARIO encontrado:")
    print(f"   - Rol: {perfil.rol}")
    print(f"   - Puntos totales: {perfil.puntos_totales}")
    print(f"   - Lecturas completadas: {perfil.lecturas_completadas}")
except Exception as e:
    print(f"❌ PERFIL USUARIO no encontrado: {e}")

print()

# Verificar ProgresionNivel
try:
    progresion = user.progresion
    print(f"✅ PROGRESION NIVEL encontrada:")
    print(f"   - Nivel actual: {progresion.nivel_actual.codigo}")
    print(f"   - Puntos en nivel: {progresion.puntos_en_nivel}")
    print(f"   - Puntos acumulativos: {progresion.puntos_acumulativos}")
    print(f"   - Listo para ascenso: {progresion.listo_para_ascenso}")
except Exception as e:
    print(f"❌ PROGRESION NIVEL no encontrada: {e}")

print(f"\n{'='*60}")
print("💡 CONCLUSIÓN:")
print("   El nivel se debería tomar de: ProgresionNivel.nivel_actual")
print("   Si no existe, crear un registro de ProgresionNivel")
print(f"{'='*60}\n")
