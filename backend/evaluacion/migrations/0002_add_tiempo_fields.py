from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='tiempo_total_segundos',
            field=models.IntegerField(default=900, verbose_name='tiempo total en segundos'),
        ),
        migrations.AddField(
            model_name='sesion',
            name='tiempo_restante_segundos',
            field=models.IntegerField(default=900, verbose_name='tiempo restante en segundos'),
        ),
    ]
