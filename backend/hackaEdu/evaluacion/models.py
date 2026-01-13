from django.db import models


class Sesion(models.Model):
    """Sesiones de lectura de usuarios - Modelo Relacional"""
    
    ESTADO_CHOICES = [
        ('INICIADA', 'Iniciada'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADA', 'Completada'),
    ]
    
    usuario = models.ForeignKey('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='sesiones', verbose_name='usuario')
    lectura = models.ForeignKey('contenido.Lectura', on_delete=models.CASCADE, related_name='sesiones', verbose_name='lectura')
    
    total_preguntas = models.IntegerField('total preguntas')
    puntaje_total = models.DecimalField('puntaje total', max_digits=5, decimal_places=2, default=0)
    puntajes_por_criterio = models.JSONField('puntajes por criterio', default=dict, blank=True)
    recomendaciones_ia = models.TextField('recomendaciones IA', blank=True)
    
    estado = models.CharField('estado', max_length=20, choices=ESTADO_CHOICES, default='INICIADA')
    fecha = models.DateTimeField('fecha', auto_now_add=True)
    fecha_inicio = models.DateTimeField('fecha inicio', null=True, blank=True)
    fecha_fin = models.DateTimeField('fecha fin', null=True, blank=True)
    duracion_segundos = models.IntegerField('duración en segundos', default=0)
    
    class Meta:
        db_table = 'sesion'
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f'{self.usuario.username} - {self.lectura.titulo} ({self.puntaje_total})'
    
    @property
    def duracion_minutos(self):
        """Retorna duración en minutos"""
        return round(self.duracion_segundos / 60, 1)


class Respuesta(models.Model):
    """Respuestas de usuarios a preguntas - Modelo Relacional"""
    
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name='respuestas', verbose_name='sesión')
    pregunta = models.ForeignKey('contenido.Pregunta', on_delete=models.CASCADE, related_name='respuestas', verbose_name='pregunta')
    criterio = models.ForeignKey('habilidades.CriterioHabilidad', on_delete=models.SET_NULL, null=True, verbose_name='criterio')
    
    respuesta = models.CharField('respuesta', max_length=500)
    es_correcta = models.BooleanField('es correcta', default=False)
    puntos_obtenidos = models.DecimalField('puntos obtenidos', max_digits=5, decimal_places=2, default=0)
    tiempo_respuesta_segundos = models.IntegerField('tiempo respuesta en segundos', default=0)
    fecha = models.DateTimeField('fecha', auto_now_add=True)
    
    class Meta:
        db_table = 'respuesta'
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['sesion', 'pregunta__orden']
        indexes = [
            models.Index(fields=['sesion']),
        ]
    
    def __str__(self):
        estado = '✓' if self.es_correcta else '✗'
        return f'{estado} P{self.pregunta.orden}: {self.respuesta[:30]}...'


class DesempenoCriterio(models.Model):
    """Desempeño acumulado por criterio de usuario - Modelo Relacional"""
    
    usuario = models.ForeignKey('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='desempenios', verbose_name='usuario')
    criterio = models.ForeignKey('habilidades.CriterioHabilidad', on_delete=models.CASCADE, related_name='desempenios', verbose_name='criterio')
    
    intentos = models.IntegerField('intentos', default=0)
    aciertos = models.IntegerField('aciertos', default=0)
    porcentaje_promedio = models.DecimalField('porcentaje promedio', max_digits=5, decimal_places=2, default=0)
    ultima_actualizacion = models.DateTimeField('última actualización', auto_now=True)
    
    class Meta:
        db_table = 'desempenio_criterio'
        verbose_name = 'Desempeño de Criterio'
        verbose_name_plural = 'Desempeños de Criterio'
        unique_together = ('usuario', 'criterio')
        ordering = ['usuario', 'criterio']
        indexes = [
            models.Index(fields=['usuario']),
        ]
    
    def __str__(self):
        return f'{self.usuario.username} - {self.criterio.nombre} ({self.porcentaje_promedio}%)'
    
    def actualizar_porcentaje(self):
        """Calcula y actualiza el porcentaje promedio"""
        if self.intentos > 0:
            self.porcentaje_promedio = (self.aciertos / self.intentos) * 100
        return self.porcentaje_promedio
