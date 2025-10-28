from django.db import models
from evaluacion.models import RespuestaAlumno, Evaluacion
from alumnos.models import Alumno
from profesores.models import NivelDesempeno, CriterioEvaluacion

class EvaluacionCriterioRespuesta(models.Model):
    respuesta = models.ForeignKey(RespuestaAlumno, on_delete=models.CASCADE)
    criterio = models.ForeignKey(CriterioEvaluacion, on_delete=models.CASCADE)
    puntaje_obtenido = models.DecimalField(max_digits=5, decimal_places=2)
    puntaje_maximo = models.DecimalField(max_digits=5, decimal_places=2)
    justificacion = models.TextField()
    evidencia = models.TextField()
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evaluación: {self.respuesta.alumno} - {self.criterio}"

class ReporteIA(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2)
    nivel_desempeno = models.ForeignKey(NivelDesempeno, on_delete=models.CASCADE)
    diagnostico_general = models.TextField()
    fortalezas_identificadas = models.TextField()
    areas_mejora = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reporte: {self.alumno} - {self.evaluacion}"

class DetalleReporteCriterio(models.Model):
    reporte = models.ForeignKey(ReporteIA, on_delete=models.CASCADE)
    criterio = models.ForeignKey(CriterioEvaluacion, on_delete=models.CASCADE)
    puntaje_promedio = models.DecimalField(max_digits=5, decimal_places=2)
    puntaje_maximo = models.DecimalField(max_digits=5, decimal_places=2)
    nivel_desempeno = models.CharField(max_length=100)
    diagnostico_criterio = models.TextField()
    sugerencias_especificas = models.TextField()
    
    def __str__(self):
        return f"Detalle: {self.reporte} - {self.criterio}"

class RecomendacionReporte(models.Model):
    reporte = models.ForeignKey(ReporteIA, on_delete=models.CASCADE)
    tipo_destinatario = models.CharField(max_length=20)
    categoria = models.CharField(max_length=100)
    contenido = models.TextField()
    prioridad = models.CharField(max_length=20)
    plazo_sugerido = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Recomendación: {self.tipo_destinatario} - {self.prioridad}"