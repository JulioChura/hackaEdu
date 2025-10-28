from django.contrib import admin
from .models import *

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel', 'grado_actual', 'colegio']
    search_fields = ['usuario__username', 'grado_actual', 'colegio']
    list_filter = ['nivel', 'grado_actual']

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['alumno', 'curso', 'estado', 'fecha_inscripcion']
    list_filter = ['curso', 'estado', 'fecha_inscripcion']
    search_fields = ['alumno__usuario__username', 'curso__nombre_curso']
    list_editable = ['estado']