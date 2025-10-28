from django.contrib import admin
from .models import *

@admin.register(NivelEducativo)
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciclo']
    search_fields = ['nombre']

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'area']
    search_fields = ['nombre', 'area']

@admin.register(NivelDesempeno)
class NivelDesempenoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puntaje_min', 'puntaje_max', 'color']
    list_editable = ['puntaje_min', 'puntaje_max', 'color']

@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'institucion', 'fecha_registro']
    search_fields = ['usuario__username', 'especialidad']
    list_filter = ['especialidad', 'institucion']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre_curso', 'docente', 'nivel', 'materia', 'activo']
    list_filter = ['nivel', 'materia', 'activo']
    search_fields = ['nombre_curso', 'codigo_curso']
    list_editable = ['activo']

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_tema', 'curso', 'orden', 'semanas_estimadas']
    list_filter = ['curso']
    ordering = ['curso', 'orden']

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ['nombre_sesion', 'tema', 'orden', 'horas_estimadas']
    list_filter = ['tema__curso']
    ordering = ['tema', 'orden']

@admin.register(CriterioEvaluacion)
class CriterioEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_criterio', 'sesion', 'peso', 'orden']
    list_filter = ['sesion']
    ordering = ['sesion', 'orden']