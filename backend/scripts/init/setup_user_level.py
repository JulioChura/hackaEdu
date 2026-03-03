"""
Script para crear/actualizar el perfil y progresión de nivel de un usuario
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from auth_custom.models import CustomUser
from usuarios.models import PerfilUsuario, ProgresionNivel
from niveles.models import NivelCEFR

def setup_user_level(email, nivel_codigo='B1'):
    """
    Crea o actualiza el perfil y progresión de un usuario
    
    Args:
        email: Email del usuario
        nivel_codigo: Código del nivel (A1, A2, B1, B2, C1, C2)
    """
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        print(f"❌ Usuario con email '{email}' no encontrado")
        return
    
    try:
        nivel = NivelCEFR.objects.get(codigo=nivel_codigo)
    except NivelCEFR.DoesNotExist:
        print(f"❌ Nivel '{nivel_codigo}' no encontrado")
        print(f"   Niveles disponibles: {list(NivelCEFR.objects.values_list('codigo', flat=True))}")
        return
    
    print(f"\n{'='*60}")
    print(f"👤 Configurando usuario: {user.email}")
    print(f"📊 Nivel: {nivel.codigo} - {nivel.nombre}")
    print(f"{'='*60}\n")
    
    # Crear o actualizar PerfilUsuario (sin nivel_cefr, está en ProgresionNivel)
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=user,
        defaults={
            'rol': 'USUARIO',
            'puntos_totales': 0,
            'lecturas_completadas': 0
        }
    )
    
    if created:
        print(f"✅ PerfilUsuario creado")
    else:
        print(f"✅ PerfilUsuario ya existe")
    
    print(f"   - Rol: {perfil.rol}")
    print(f"   - Puntos totales: {perfil.puntos_totales}")
    
    print()
    
    # Crear o actualizar ProgresionNivel
    progresion, created = ProgresionNivel.objects.get_or_create(
        usuario=user,
        defaults={
            'nivel_actual': nivel,
            'puntos_acumulativos': 0,
            'puntos_en_nivel': 0,
            'lecturas_completadas_en_nivel': 0,
            'promedio_puntos_en_nivel': 0,
            'criterios_dominados': {},
            'listo_para_ascenso': False,
            'ascenso_ofrecido': False
        }
    )
    
    if not created:
        progresion.nivel_actual = nivel
        progresion.save()
        print(f"✅ ProgresionNivel actualizado")
    else:
        print(f"✅ ProgresionNivel creado")
    
    print(f"   - Nivel actual: {progresion.nivel_actual.codigo}")
    print(f"   - Puntos en nivel: {progresion.puntos_en_nivel}")
    print(f"   - Puntos acumulativos: {progresion.puntos_acumulativos}")
    
    print(f"\n{'='*60}")
    print(f"✨ Usuario configurado correctamente con nivel {nivel.codigo}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("\n⚠️  USO: python setup_user_level.py <email> [nivel]")
        print("   Ejemplo: python setup_user_level.py admin@admin.com B1")
        print(f"\n   Niveles disponibles: {', '.join(NivelCEFR.objects.values_list('codigo', flat=True))}\n")
        
        # Mostrar usuarios existentes
        users = CustomUser.objects.all()
        if users.exists():
            print("   Usuarios disponibles:")
            for u in users:
                print(f"      - {u.email}")
            print()
        
        sys.exit(1)
    
    email = sys.argv[1]
    nivel = sys.argv[2] if len(sys.argv) > 2 else 'B1'
    
    setup_user_level(email, nivel.upper())
