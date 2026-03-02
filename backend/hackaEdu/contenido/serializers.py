from rest_framework import serializers
from .models import Lectura, Categoria, Modalidad, Pregunta
from evaluacion.models import Sesion


CATEGORIA_IMAGEN_MAP = {
    'Ciencia': '/media/categorias/ciencia.jpg',
    'Literatura': '/media/categorias/literatura.jpg',
    'Historia': '/media/categorias/historia.jpg',
    'Tecnología': '/media/categorias/tecnologia.jpg',
    'Arte': '/media/categorias/arte.jpg',
    'Negocios': '/media/categorias/negocios.jpg',
    'Viajes': '/media/categorias/viajes.jpg',
    'Salud': '/media/categorias/salud.jpg',
    'Deportes': '/media/categorias/deportes.jpg',
    'Política': '/media/categorias/politica.jpg',
}


class LecturaSerializer(serializers.ModelSerializer):
    """Serializer para Lectura con fallback de imagen genérica"""
    
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    modalidad_nombre = serializers.CharField(source='modalidad.nombre', read_only=True)
    nivel_codigo = serializers.CharField(source='nivel_cefr.codigo', read_only=True)
    estado_usuario = serializers.SerializerMethodField()
    progreso_usuario = serializers.SerializerMethodField()
    
    class Meta:
        model = Lectura
        fields = [
            'id', 'titulo', 'contenido', 'palabras_count', 'imagen_url',
            'categoria', 'categoria_nombre', 'modalidad', 'modalidad_nombre',
            'nivel_cefr', 'nivel_codigo', 'usuario_creador', 'fecha_creacion',
            'fecha_actualizacion', 'publicada', 'estado_usuario', 'progreso_usuario'
        ]
        read_only_fields = ['palabras_count', 'fecha_creacion', 'fecha_actualizacion']

    def _get_latest_sesion(self, instance):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return None

        return (
            Sesion.objects
            .filter(usuario=request.user, lectura=instance)
            .order_by('-fecha')
            .first()
        )

    def get_estado_usuario(self, instance):
        sesion = self._get_latest_sesion(instance)
        if not sesion:
            return 'not-started'
        if sesion.estado == 'COMPLETADA':
            return 'completed'
        return 'in-progress'

    def get_progreso_usuario(self, instance):
        sesion = self._get_latest_sesion(instance)
        if not sesion:
            return 0

        if sesion.estado == 'COMPLETADA':
            return 100

        if sesion.total_preguntas <= 0:
            return 0

        respuestas_count = sesion.respuestas.count()
        return min(99, round((respuestas_count / sesion.total_preguntas) * 100))
    
    def to_representation(self, instance):
        """Agregar imagen_genérica como fallback si imagen_url es null"""
        data = super().to_representation(instance)
        
        # Si imagen_url existe, usarla
        if data.get('imagen_url'):
            data['imagen_url_final'] = data['imagen_url']
        else:
            # Fallback: imagen genérica según categoría
            categoria_nombre = data.get('categoria_nombre', 'default')
            data['imagen_url_final'] = CATEGORIA_IMAGEN_MAP.get(
                categoria_nombre, 
                '/media/categorias/default.jpg'
            )
        
        return data


class PreguntaSerializer(serializers.ModelSerializer):
    """Serializer para Pregunta"""
    
    criterio_nombre = serializers.CharField(source='criterio.codigo', read_only=True)
    
    class Meta:
        model = Pregunta
        fields = [
            'id', 'lectura', 'criterio', 'criterio_nombre', 'texto',
            'tipo', 'opciones', 'respuesta_correcta', 'explicacion', 'orden'
        ]


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para Categoría"""
    
    class Meta:
        model = Categoria
        fields = ['codigo', 'nombre', 'icono']


class ModalidadSerializer(serializers.ModelSerializer):
    """Serializer para Modalidad"""
    
    class Meta:
        model = Modalidad
        fields = ['codigo', 'nombre', 'descripcion', 'activa']
