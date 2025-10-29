from django.db import models
from usuario.models import Usuario

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'nivel_educativo'

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'materia'

class NivelDesempeno(models.Model):
    nombre = models.CharField(max_length=100)
    puntaje_minimo = models.DecimalField(max_digits=5, decimal_places=2)
    puntaje_maximo = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'nivel_desempeno'
    
    def __str__(self):
        return f"{self.nombre} ({self.puntaje_minimo}-{self.puntaje_maximo})"

class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'docente'

class Curso(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT)
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    codigo_curso = models.CharField(max_length=20, unique=True)
    nombre_curso = models.CharField(max_length=200)
    objetivo = models.TextField()
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'curso'

class Tema(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='temas')
    nombre_tema = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.IntegerField()
    semanas_estimadas = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tema'
        ordering = ['orden']

class Sesion(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='sesiones')
    nombre_sesion = models.CharField(max_length=200)
    objetivo_sesion = models.TextField()
    horas_estimadas = models.IntegerField()
    orden = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sesion'
        ordering = ['orden']

class CriterioEvaluacion(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name='criterios')
    nombre_criterio = models.CharField(max_length=200)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    orden = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'criterio_evaluacion'
        ordering = ['orden']