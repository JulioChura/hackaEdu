from django.db import models
from usuario.models import Usuario
from profesores.models import NivelEducativo, Curso

class Alumno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT, null=True, blank=True)
    grado_actual = models.CharField(max_length=50)
    colegio = models.CharField(max_length=200, blank=True)
    nombre_tutor = models.CharField(max_length=200, blank=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'alumno'
    
    def __str__(self):
        return f"{self.usuario.nombres} {self.usuario.apellidos}"

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    codigo_acceso = models.CharField(max_length=50, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='activo')
    
    class Meta:
        db_table = 'inscripcion'
        unique_together = ['alumno', 'curso']
    
    def __str__(self):
        return f"{self.alumno} - {self.curso.nombre_curso}"
