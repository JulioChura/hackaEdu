from django.db import models


class PerfilUsuario(models.Model):
    """
    Perfil del usuario - Estadísticas generales del aprendizaje
    
    Cada usuario tiene un perfil que guarda:
      - Rol en la plataforma (Usuario, Premium, Moderador)
      - Nivel CEFR actual
      - Puntos totales acumulados
      - Lecturas completadas
    
    NOTA: Para acceso al admin panel, usar CustomUser.is_staff y is_superuser
          El campo 'rol' es para lógica de negocio (premium, moderador, etc.)
    """
    
    ROL_CHOICES = [
        ('USUARIO', 'Usuario'),
        ('PREMIUM', 'Premium'),
        ('MODERADOR', 'Moderador'),
    ]
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='perfil_hackaedu', verbose_name='usuario')
    rol = models.CharField('rol', max_length=20, choices=ROL_CHOICES, default='USUARIO', help_text='Rol de negocio. Para admin usar is_staff')
    nivel_cefr = models.ForeignKey('niveles.NivelCEFR', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='nivel CEFR')
    puntos_totales = models.IntegerField('puntos totales', default=0)
    lecturas_completadas = models.IntegerField('lecturas completadas', default=0)
    
    class Meta:
        db_table = 'perfil_usuario'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f'{self.usuario.email} - {self.rol}'
    
    @property
    def es_premium(self):
        """Verifica si el usuario tiene rol premium"""
        return self.rol == 'PREMIUM'
    
    @property
    def es_moderador(self):
        """Verifica si el usuario es moderador"""
        return self.rol == 'MODERADOR'


class ProgresionNivel(models.Model):
    """Tracking de progresión de usuario en nivel actual (Modelo Relacional)"""
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='progresion', verbose_name='usuario')
    nivel_actual = models.ForeignKey('niveles.NivelCEFR', on_delete=models.PROTECT, verbose_name='nivel actual')
    
    # SISTEMA DOBLE DE PUNTOS
    puntos_acumulativos = models.IntegerField('puntos acumulativos globales', default=0)  # Para ranking global
    puntos_en_nivel = models.IntegerField('puntos en nivel actual', default=0)  # Para ascenso de nivel
    
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


class PreferenciasUsuario(models.Model):
    """
    Preferencias de usuario para personalización de contenido
    
    Captura durante el registro:
      - Categorías de interés (TEMAS: Ciencia, Deportes, Tecnología...)
      - Dificultad inicial
    
    NOTA: Modalidades (IA, PDF, Texto) NO son preferencias.
          Son opciones que el usuario usa según el momento al crear contenido.
          Se guardan en cada Lectura individual como metadata.
    
    Se usa para:
      - Recomendación inicial de lecturas
      - Algoritmo de personalización
      - Generación automática de contenido
    """
    
    DIFICULTAD_CHOICES = [
        ('BASIC', 'Básica (1-2)'),
        ('INTERMEDIATE', 'Intermedia (3-4)'),
        ('ADVANCED', 'Avanzada (5-6)'),
        ('EXPERT', 'Experto (7+)'),
    ]
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='preferencias', verbose_name='usuario')
    
    # Categorías de interés (TEMAS)
    categorias_preferidas = models.ManyToManyField(
        'contenido.Categoria',
        blank=True,
        related_name='usuarios_preferencias',
        verbose_name='categorías preferidas',
        help_text='TEMAS de interés: Ciencia, Deportes, Tecnología, Viajes...'
    )
    
    # Dificultad inicial deseada
    dificultad_inicial = models.CharField(
        'dificultad inicial',
        max_length=20,
        choices=DIFICULTAD_CHOICES,
        default='BASIC'
    )
    
    fecha_creacion = models.DateTimeField('fecha de creación', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('fecha de actualización', auto_now=True)
    
    class Meta:
        db_table = 'preferencias_usuario'
        verbose_name = 'Preferencias de Usuario'
        verbose_name_plural = 'Preferencias de Usuarios'
    
    def __str__(self):
        return f'Preferencias de {self.usuario.email}'
