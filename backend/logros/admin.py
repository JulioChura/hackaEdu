from django.contrib import admin
from .models import Logro, LogroUsuario


@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'puntos_recompensa', 'icono', 'fecha_creacion')
    search_fields = ('codigo', 'nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    ordering = ('nombre',)


@admin.register(LogroUsuario)
class LogroUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'logro', 'fecha_obtencion', 'notificacion_enviada')
    list_filter = ('notificacion_enviada', 'fecha_obtencion')
    search_fields = ('usuario__email', 'logro__nombre')
    readonly_fields = ('fecha_obtencion',)
    ordering = ('-fecha_obtencion',)
