from django.db import models


class CriterioHabilidad(models.Model):
    """Criterios de evaluación de habilidades de lectura - Modelo Relacional"""
    
    codigo = models.CharField('código', max_length=50, unique=True, primary_key=True)
    nombre = models.CharField('nombre', max_length=100)
    descripcion = models.TextField('descripción', blank=True)
    peso_evaluacion = models.IntegerField('peso en evaluación', default=1)
    
    class Meta:
        db_table = 'criterio_habilidad'
        verbose_name = 'Criterio de Habilidad'
        verbose_name_plural = 'Criterios de Habilidad'
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre} (Peso: {self.peso_evaluacion})'
