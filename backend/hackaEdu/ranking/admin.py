from django.contrib import admin
from .models import RachaUsuario, Ranking


@admin.register(RachaUsuario)
class RachaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dias_consecutivos', 'ultimo_acceso', 'ultima_lectura_fecha', 'fecha_ultima_actualizacion')
    search_fields = ('usuario__email', 'usuario__nombre')
    readonly_fields = ('fecha_ultima_actualizacion',)
    ordering = ('-dias_consecutivos',)


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('posicion', 'usuario', 'puntos_totales', 'fecha_actualizacion')
    search_fields = ('usuario__email', 'usuario__nombre')
    readonly_fields = ('fecha_actualizacion',)
    ordering = ('posicion',)
