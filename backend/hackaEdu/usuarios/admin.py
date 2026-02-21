from django.contrib import admin
from .models import PerfilUsuario, ProgresionNivel, PreferenciasUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'nivel_cefr', 'puntos_totales', 'lecturas_completadas')
    list_filter = ('rol', 'nivel_cefr')
    search_fields = ('usuario__email', 'usuario__nombre', 'usuario__apellido')
    readonly_fields = ('usuario',)


@admin.register(ProgresionNivel)
class ProgresionNivelAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel_actual', 'puntos_acumulativos', 'puntos_en_nivel', 'lecturas_completadas_en_nivel', 'listo_para_ascenso')
    list_filter = ('nivel_actual', 'listo_para_ascenso', 'ascenso_ofrecido')
    search_fields = ('usuario__email', 'usuario__nombre')
    readonly_fields = ('usuario', 'fecha_actualizacion')


@admin.register(PreferenciasUsuario)
class PreferenciasUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dificultad_inicial', 'fecha_creacion')
    list_filter = ('dificultad_inicial',)
    search_fields = ('usuario__email', 'usuario__nombre')
    filter_horizontal = ('categorias_preferidas',)
    readonly_fields = ('usuario', 'fecha_creacion', 'fecha_actualizacion')
