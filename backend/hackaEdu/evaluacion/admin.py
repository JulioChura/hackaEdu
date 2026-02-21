from django.contrib import admin
from .models import Sesion, Respuesta, DesempenoCriterio


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'lectura', 'estado', 'puntaje_total', 'total_preguntas', 'fecha', 'duracion_minutos')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__email', 'lectura__titulo')
    readonly_fields = ('fecha', 'fecha_inicio', 'fecha_fin', 'duracion_segundos')
    ordering = ('-fecha',)


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_lectura', 'pregunta', 'es_correcta', 'puntos_obtenidos', 'fecha')
    list_filter = ('es_correcta', 'fecha')
    search_fields = ('sesion__usuario__email', 'pregunta__texto')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)
    
    def get_usuario(self, obj):
        return obj.sesion.usuario
    get_usuario.short_description = 'Usuario'
    
    def get_lectura(self, obj):
        return obj.sesion.lectura
    get_lectura.short_description = 'Lectura'


@admin.register(DesempenoCriterio)
class DesempenoCriterioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'criterio', 'intentos', 'aciertos', 'porcentaje_promedio', 'ultima_actualizacion')
    list_filter = ('criterio',)
    search_fields = ('usuario__email', 'criterio__nombre')
    readonly_fields = ('ultima_actualizacion',)
    ordering = ('usuario', 'criterio')
