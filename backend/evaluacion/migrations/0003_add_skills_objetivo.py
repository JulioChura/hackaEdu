from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0002_add_tiempo_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='skills_objetivo',
            field=models.JSONField(blank=True, default=list, verbose_name='skills objetivo'),
        ),
    ]
