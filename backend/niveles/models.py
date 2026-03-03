from django.db import models


class NivelCEFR(models.Model):
    """Niveles de competencia CEFR (A1 a C2) - Modelo Relacional"""
    
    CATEGORIA_NIVEL = [
        ('BASICO', 'Básico (A1-A2)'),
        ('INTERMEDIO', 'Intermedio (B1-B2)'),
        ('AVANZADO', 'Avanzado (C1-C2)'),
    ]
    
    codigo = models.CharField('código', max_length=5, unique=True, primary_key=True)  # A1, A2, B1, B2, C1, C2
    nombre = models.CharField('nombre', max_length=100)  # "Principiante", "Elemental", etc
    categoria = models.CharField('categoría', max_length=20, choices=CATEGORIA_NIVEL)  # Para multiplicadores
    
    vocab_min = models.IntegerField('vocabulario mínimo')
    vocab_max = models.IntegerField('vocabulario máximo')
    cantidad_preguntas = models.IntegerField('cantidad de preguntas', default=10)
    
    # MÉTRICAS DE PUNTOS
    puntos_requeridos = models.IntegerField('puntos requeridos para ascenso')  # 50 básico, 60 intermedio, 70 avanzado
    multiplicador_puntos = models.DecimalField('multiplicador de puntos', max_digits=3, decimal_places=2, default=1.0)
    
    distribucion_criterios = models.JSONField('distribución de criterios', default=dict, blank=True)
    
    class Meta:
        db_table = 'nivel_cefr'
        verbose_name = 'Nivel CEFR'
        verbose_name_plural = 'Niveles CEFR'
        ordering = ['codigo']
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
