from django.db import models

class Evaluacion(models.Model):
    alumno = models.CharField(max_length=100)
    rubrica = models.TextField()
    respuesta_alumno = models.TextField()
    evaluacion_ia = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluación de {self.alumno} - {self.fecha.strftime('%Y-%m-%d')}"
