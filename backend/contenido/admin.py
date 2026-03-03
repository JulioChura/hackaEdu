from django.contrib import admin
from .models import Categoria, Modalidad, Lectura, Pregunta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'icono')
    search_fields = ('codigo', 'nombre')
    ordering = ('nombre',)


@admin.register(Modalidad)
class ModalidadAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'activa')
    list_filter = ('activa',)
    search_fields = ('codigo', 'nombre')
    ordering = ('nombre',)


@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel_cefr', 'categoria', 'modalidad', 'usuario_creador', 'palabras_count', 'publicada', 'fecha_creacion')
    list_filter = ('nivel_cefr', 'categoria', 'modalidad', 'publicada', 'dificultad')
    search_fields = ('titulo', 'contenido', 'usuario_creador__email')
    readonly_fields = ('palabras_count', 'fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('get_lectura_titulo', 'tipo', 'criterio', 'orden', 'puntos_directos')
    list_filter = ('tipo', 'criterio')
    search_fields = ('texto', 'lectura__titulo')
    ordering = ('lectura', 'orden')
    
    def get_lectura_titulo(self, obj):
        return obj.lectura.titulo
    get_lectura_titulo.short_description = 'Lectura'
