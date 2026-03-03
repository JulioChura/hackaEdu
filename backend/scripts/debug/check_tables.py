from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]

print("\n" + "="*60)
print("TABLAS EN LA BASE DE DATOS")
print("="*60)
for table in tables:
    print(f"  - {table}")

print("\n" + "="*60)
print("TABLAS RELACIONADAS CON USUARIOS:")
print("="*60)
user_tables = [t for t in tables if 'user' in t.lower()]
for table in user_tables:
    print(f"  - {table}")

# Verificar configuración del modelo de usuario
from django.conf import settings
print("\n" + "="*60)
print("CONFIGURACIÓN AUTH_USER_MODEL:")
print("="*60)
print(f"  {settings.AUTH_USER_MODEL}")

# Verificar el nombre de la tabla del CustomUser
from auth_custom.models import CustomUser
print("\n" + "="*60)
print("TABLA DEL MODELO CustomUser:")
print("="*60)
print(f"  {CustomUser._meta.db_table}")
