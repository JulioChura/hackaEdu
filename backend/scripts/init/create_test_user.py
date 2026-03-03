"""
Script para crear un usuario de prueba
Ejecutar: python create_test_user.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from auth_custom.models import CustomUser

# Datos del usuario de prueba
email = 'test@test.com'
password = 'test123456'
nombre = 'Test'
apellido = 'User'

# Verificar si ya existe
if CustomUser.objects.filter(email=email).exists():
    print(f'❌ El usuario {email} ya existe')
    user = CustomUser.objects.get(email=email)
    print(f'   ID: {user.id}')
    print(f'   Nombre: {user.nombre} {user.apellido}')
    print(f'   Email: {user.email}')
else:
    # Crear usuario
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        nombre=nombre,
        apellido=apellido
    )
    print(f'✅ Usuario creado exitosamente!')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
    print(f'   Nombre: {nombre} {apellido}')

print('\n📋 Credenciales para login:')
print(f'   Email: {email}')
print(f'   Password: {password}')
