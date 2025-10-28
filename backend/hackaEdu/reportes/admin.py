from django.contrib import admin
from .models import *

@admin.register(EvaluacionCriterioRespuesta)
class EvaluacionCriterioRespuestaAdmin(admin.ModelAdmin):
    list_display = ['respuesta', 'criterio', 'puntaje_obtenido', 'puntaje_maximo', 'fecha_evaluacion']
    list_filter = ['criterio', 'fecha_evaluacion']
    readonly_fields = ['fecha_evaluacion']
    search_fields = ['respuesta__alumno__usuario__username']

@admin.register(ReporteIA)
class ReporteIAAdmin(admin.ModelAdmin):
    list_display = ['alumno', 'evaluacion', 'puntaje_total', 'nivel_desempeno', 'fecha_generacion']
    list_filter = ['evaluacion', 'nivel_desempeno', 'fecha_generacion']
    readonly_fields = ['fecha_generacion']
    search_fields = ['alumno__usuario__username']

@admin.register(DetalleReporteCriterio)
class DetalleReporteCriterioAdmin(admin.ModelAdmin):
    list_display = ['reporte', 'criterio', 'puntaje_promedio', 'nivel_desempeno']
    list_filter = ['criterio', 'nivel_desempeno']

@admin.register(RecomendacionReporte)
class RecomendacionReporteAdmin(admin.ModelAdmin):
    list_display = ['reporte', 'tipo_destinatario', 'categoria', 'prioridad']
    list_filter = ['tipo_destinatario', 'categoria', 'prioridad']
    list_editable = ['prioridad']