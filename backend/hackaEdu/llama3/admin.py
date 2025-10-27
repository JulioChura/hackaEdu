from django.contrib import admin
from .models import Evaluacion

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'fecha')
    search_fields = ('alumno', 'rubrica', 'respuesta_alumno')
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)
