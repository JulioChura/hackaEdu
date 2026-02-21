from django.contrib import admin
from .models import NivelCEFR


@admin.register(NivelCEFR)
class NivelCEFRAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'vocab_min', 'vocab_max', 'puntos_requeridos', 'multiplicador_puntos', 'cantidad_preguntas')
    list_filter = ('categoria',)
    search_fields = ('codigo', 'nombre')
    ordering = ('codigo',)
