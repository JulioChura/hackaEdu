from django.db import models


class Logro(models.Model):
    """Logros desbloqueables por usuarios - Modelo Relacional"""
    
    codigo = models.CharField('código', max_length=50, unique=True, primary_key=True)
    nombre = models.CharField('nombre', max_length=100)
    descripcion = models.TextField('descripción')
    criterios = models.JSONField('criterios para desbloqueo', default=dict, blank=True)  # Ej: {"lecturas_minimas": 5, "promedio_minimo": 70}
    puntos_recompensa = models.IntegerField('puntos recompensa', default=10)
    icono = models.CharField('icono', max_length=100, blank=True)  # Ej: "medal", "star"
    fecha_creacion = models.DateTimeField('fecha creación', auto_now_add=True)
    
    class Meta:
        db_table = 'logro'
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre} (+{self.puntos_recompensa}pts)'


class LogroUsuario(models.Model):
    """Logros desbloqueados por usuarios - Modelo Relacional"""
    
    usuario = models.ForeignKey('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='logros_obtenidos', verbose_name='usuario')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name='usuarios_obtenidos', verbose_name='logro')
    
    fecha_obtencion = models.DateTimeField('fecha obtención', auto_now_add=True)
    notificacion_enviada = models.BooleanField('notificación enviada', default=False)
    
    class Meta:
        db_table = 'logro_usuario'
        verbose_name = 'Logro del Usuario'
        verbose_name_plural = 'Logros del Usuario'
        unique_together = ('usuario', 'logro')
        ordering = ['-fecha_obtencion']
        indexes = [
            models.Index(fields=['usuario']),
        ]
    
    def __str__(self):
        return f'{self.usuario.username} - {self.logro.nombre}'
