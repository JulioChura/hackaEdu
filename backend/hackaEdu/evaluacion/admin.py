from django.contrib import admin
from .models import *

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto_pregunta', 'sesion', 'orden']
    list_filter = ['sesion']
    search_fields = ['texto_pregunta']
    ordering = ['sesion', 'orden']

@admin.register(PreguntaCriterio)
class PreguntaCriterioAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'criterio', 'activo']
    list_filter = ['criterio', 'activo']
    list_editable = ['activo']

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo_evaluacion', 'sesion', 'docente', 'fecha_aplicacion', 'activo']
    list_filter = ['sesion', 'docente', 'fecha_aplicacion', 'activo']
    search_fields = ['titulo_evaluacion', 'instrucciones']
    list_editable = ['activo']
    date_hierarchy = 'fecha_aplicacion'

@admin.register(RespuestaAlumno)
class RespuestaAlumnoAdmin(admin.ModelAdmin):
    list_display = ['alumno', 'evaluacion', 'pregunta', 'fecha_respuesta']
    list_filter = ['evaluacion', 'fecha_respuesta']
    search_fields = ['alumno__usuario__username', 'texto_respuesta']
    readonly_fields = ['fecha_respuesta']