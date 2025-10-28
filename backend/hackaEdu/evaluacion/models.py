from django.db import models
from profesores.models import Sesion, Docente, CriterioEvaluacion
from alumnos.models import Alumno

class Pregunta(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    texto_pregunta = models.TextField()
    orden = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class PreguntaCriterio(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    criterio = models.ForeignKey(CriterioEvaluacion, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

class Evaluacion(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    titulo_evaluacion = models.CharField(max_length=200)
    instrucciones = models.TextField()
    fecha_aplicacion = models.DateTimeField()
    fecha_limite = models.DateTimeField()
    tiempo_limite = models.IntegerField()
    intentos_permitidos = models.IntegerField(default=1)
    mostrar_resultados = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class RespuestaAlumno(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)