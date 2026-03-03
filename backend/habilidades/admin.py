from django.contrib import admin
from .models import CriterioHabilidad


@admin.register(CriterioHabilidad)
class CriterioHabilidadAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'peso_evaluacion')
    search_fields = ('codigo', 'nombre', 'descripcion')
    ordering = ('nombre',)
