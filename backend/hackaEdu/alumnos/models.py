from django.db import models
from django.contrib.auth.models import User
from profesores.models import NivelEducativo, Curso

class Alumno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE)
    grado_actual = models.CharField(max_length=50)
    colegio = models.CharField(max_length=200)
    nombre_tutor = models.CharField(max_length=200)
    telefono_emergencia = models.CharField(max_length=15)

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    codigo_acceso = models.CharField(max_length=20)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)