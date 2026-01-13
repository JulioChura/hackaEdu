from django.db import models


class Categoria(models.Model):
    """Categorías de lecturas - Modelo Relacional"""
    
    codigo = models.CharField('código', max_length=50, unique=True, primary_key=True)
    nombre = models.CharField('nombre', max_length=100)
    icono = models.CharField('icono', max_length=50, blank=True)  # Código de icono (ej: "book", "science")
    
    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Modalidad(models.Model):
    """Modalidades de creación de lecturas (Manual, IA, API News, etc) - Modelo Relacional"""
    
    codigo = models.CharField('código', max_length=50, unique=True, primary_key=True)
    nombre = models.CharField('nombre', max_length=100)
    descripcion = models.TextField('descripción', blank=True)
    activa = models.BooleanField('activa', default=True)
    
    class Meta:
        db_table = 'modalidad'
        verbose_name = 'Modalidad'
        verbose_name_plural = 'Modalidades'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Lectura(models.Model):
    """Lecturas creadas por profesores - Modelo Relacional"""
    
    usuario_creador = models.ForeignKey('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='lecturas_creadas', verbose_name='usuario creador')
    nivel_cefr = models.ForeignKey('niveles.NivelCEFR', on_delete=models.PROTECT, verbose_name='nivel CEFR')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, verbose_name='categoría')
    modalidad = models.ForeignKey(Modalidad, on_delete=models.SET_NULL, null=True, verbose_name='modalidad')
    
    titulo = models.CharField('título', max_length=255)
    contenido = models.TextField('contenido')
    palabras_count = models.IntegerField('contador de palabras', default=0)
    imagen_url = models.URLField('URL de imagen', blank=True, null=True, help_text='Imagen personalizada (scraping futuro). Si está vacía, usa genérica de categoría')
    
    fecha_creacion = models.DateTimeField('fecha de creación', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('fecha de actualización', auto_now=True)
    publicada = models.BooleanField('publicada', default=False)
    
    class Meta:
        db_table = 'lectura'
        verbose_name = 'Lectura'
        verbose_name_plural = 'Lecturas'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nivel_cefr']),
            models.Index(fields=['categoria']),
            models.Index(fields=['publicada']),
        ]
    
    def __str__(self):
        return f'{self.titulo} ({self.nivel_cefr.codigo})'
    
    def save(self, *args, **kwargs):
        """Actualizar contador de palabras automáticamente"""
        if self.contenido:
            self.palabras_count = len(self.contenido.split())
        super().save(*args, **kwargs)


class Pregunta(models.Model):
    """Preguntas de una lectura - Modelo Relacional"""
    
    TIPO_CHOICES = [
        ('MULTIPLE', 'Opción Múltiple'),
        ('COMPLETAR', 'Completar'),
        ('VERDADERO_FALSO', 'Verdadero/Falso'),
    ]
    
    lectura = models.ForeignKey(Lectura, on_delete=models.CASCADE, related_name='preguntas', verbose_name='lectura')
    criterio = models.ForeignKey('habilidades.CriterioHabilidad', on_delete=models.PROTECT, verbose_name='criterio de habilidad')
    
    texto = models.TextField('texto de pregunta')
    tipo = models.CharField('tipo', max_length=20, choices=TIPO_CHOICES, default='MULTIPLE')
    opciones = models.JSONField('opciones', default=list, blank=True)  # Para multiple choice: ["opción1", "opción2", ...]
    respuesta_correcta = models.CharField('respuesta correcta', max_length=500)
    explicacion = models.TextField('explicación', blank=True)
    
    orden = models.IntegerField('orden', default=0)
    
    class Meta:
        db_table = 'pregunta'
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['lectura', 'orden']
        indexes = [
            models.Index(fields=['lectura']),
        ]
    
    def __str__(self):
        truncado = (self.texto[:50] + '...') if len(self.texto) > 50 else self.texto
        return f'P{self.orden}: {truncado}'
