from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Evaluacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    rubrica = models.TextField()
    respuesta_alumno = models.TextField()
    resultado_ia = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluación de {self.alumno.nombre} - {self.fecha.strftime('%Y-%m-%d')}"
