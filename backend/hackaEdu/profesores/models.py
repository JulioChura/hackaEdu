from django.db import models
from django.contrib.auth.models import User

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=50)

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

class NivelDesempeno(models.Model):
    nombre = models.CharField(max_length=100)
    puntaje_min = models.DecimalField(max_digits=5, decimal_places=2)
    puntaje_max = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=20)

class RolUsuario(models.Model):
    nombre = models.CharField(max_length=50)

class Docente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)

class Curso(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    codigo_curso = models.CharField(max_length=20)
    nombre_curso = models.CharField(max_length=200)
    objetivo = models.TextField()
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

class Tema(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre_tema = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.IntegerField()
    semanas_estimadas = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Sesion(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    nombre_sesion = models.CharField(max_length=200)
    objetivo_sesion = models.TextField()
    horas_estimadas = models.IntegerField()
    orden = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class CriterioEvaluacion(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    nombre_criterio = models.CharField(max_length=200)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    orden = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)