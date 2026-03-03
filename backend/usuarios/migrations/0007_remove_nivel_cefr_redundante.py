# Generated manually - Remove redundant nivel_cefr field from PerfilUsuario
# The source of truth for user level is ProgresionNivel.nivel_actual

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_remove_modalidades_preferidas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilusuario',
            name='nivel_cefr',
        ),
    ]
