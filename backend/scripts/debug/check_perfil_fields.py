"""
Comprueba si PerfilUsuario tiene el campo `nivel_cefr` en el modelo.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hackaEdu.settings')
django.setup()
from usuarios.models import PerfilUsuario

fields = [f.name for f in PerfilUsuario._meta.get_fields()]
print('PerfilUsuario fields:')
for f in fields:
    print(' -', f)

print('\nHas attribute nivel_cefr?', hasattr(PerfilUsuario, 'nivel_cefr'))
