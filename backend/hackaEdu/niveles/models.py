from django.db import models


class NivelCEFR(models.Model):
    """Niveles de competencia CEFR (A1 a C2) - Modelo Relacional"""
    
    codigo = models.CharField('código', max_length=5, unique=True, primary_key=True)  # A1, A2, B1, B2, C1, C2
    nombre = models.CharField('nombre', max_length=100)  # "Principiante", "Elemental", etc
    vocab_min = models.IntegerField('vocabulario mínimo')
    vocab_max = models.IntegerField('vocabulario máximo')
    cantidad_preguntas = models.IntegerField('cantidad de preguntas', default=15)
    distribucion_criterios = models.JSONField('distribución de criterios', default=dict, blank=True)
    
    class Meta:
        db_table = 'nivel_cefr'
        verbose_name = 'Nivel CEFR'
        verbose_name_plural = 'Niveles CEFR'
        ordering = ['codigo']
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
