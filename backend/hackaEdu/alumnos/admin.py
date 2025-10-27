from django.contrib import admin
from .models import Alumno, Evaluacion

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('alumno__nombre',)
    readonly_fields = ('fecha',)
