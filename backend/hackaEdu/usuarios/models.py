from django.db import models


class PerfilUsuario(models.Model):
    """Perfil HackaEdu del usuario - Lógica de negocio - Modelo Relacional"""
    
    ROL_CHOICES = [
        ('ESTUDIANTE', 'Estudiante'),
        ('PROFESOR', 'Profesor'),
    ]
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='perfil_hackaedu', verbose_name='usuario')
    rol = models.CharField('rol', max_length=20, choices=ROL_CHOICES, default='ESTUDIANTE')
    nivel_cefr = models.ForeignKey('niveles.NivelCEFR', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='nivel CEFR')
    puntos_totales = models.IntegerField('puntos totales', default=0)
    lecturas_completadas = models.IntegerField('lecturas completadas', default=0)
    
    class Meta:
        db_table = 'perfil_usuario'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f'{self.usuario.email} - {self.rol}'


class ProgresionNivel(models.Model):
    """Tracking de progresión de usuario en nivel actual (Modelo Relacional)"""
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='progresion', verbose_name='usuario')
    nivel_actual = models.ForeignKey('niveles.NivelCEFR', on_delete=models.PROTECT, verbose_name='nivel actual')
    lecturas_completadas_en_nivel = models.IntegerField('lecturas completadas en nivel', default=0)
    promedio_puntos_en_nivel = models.DecimalField('promedio puntos en nivel', max_digits=5, decimal_places=2, default=0)
    criterios_dominados = models.JSONField('criterios dominados', default=dict, blank=True)
    listo_para_ascenso = models.BooleanField('listo para ascenso', default=False)
    ascenso_ofrecido = models.BooleanField('ascenso ofrecido', default=False)
    fecha_actualizacion = models.DateTimeField('fecha actualización', auto_now=True)
    
    class Meta:
        db_table = 'progresion_nivel'
        verbose_name = 'Progresión de Nivel'
        verbose_name_plural = 'Progresiones de Nivel'
    
    def __str__(self):
        return f'{self.usuario.email} - {self.nivel_actual.codigo}'
