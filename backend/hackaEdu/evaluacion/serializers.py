from rest_framework import serializers
from contenido.models import Lectura, Pregunta
from contenido.serializers import LecturaSerializer, PreguntaSerializer
from .models import Sesion, Respuesta


class PreguntaPublicSerializer(serializers.ModelSerializer):
    """Serializer de pregunta sin respuesta correcta (para sesiones activas)."""

    criterio_nombre = serializers.CharField(source='criterio.codigo', read_only=True)

    class Meta:
        model = Pregunta
        fields = [
            'id', 'lectura', 'criterio', 'criterio_nombre', 'texto',
            'tipo', 'opciones', 'explicacion', 'orden'
        ]


class RespuestaSerializer(serializers.ModelSerializer):
    """Serializer para respuestas de usuario."""

    class Meta:
        model = Respuesta
        fields = [
            'id', 'pregunta', 'respuesta', 'es_correcta',
            'puntos_obtenidos', 'tiempo_respuesta_segundos', 'fecha'
        ]
        read_only_fields = ['es_correcta', 'puntos_obtenidos', 'fecha']


class SesionSerializer(serializers.ModelSerializer):
    """Serializer basico para sesiones."""

    class Meta:
        model = Sesion
        fields = [
            'id', 'usuario', 'lectura', 'estado', 'total_preguntas',
            'puntaje_total', 'tiempo_total_segundos', 'tiempo_restante_segundos',
            'fecha_fin_plazo',
            'skills_objetivo', 'fecha', 'fecha_inicio', 'fecha_fin', 'duracion_segundos'
        ]
        read_only_fields = ['usuario', 'puntaje_total', 'fecha', 'fecha_inicio', 'fecha_fin', 'duracion_segundos']


class SesionDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado con lectura, preguntas y respuestas."""

    lectura = LecturaSerializer(read_only=True)
    preguntas = serializers.SerializerMethodField()
    respuestas = RespuestaSerializer(many=True, read_only=True)

    class Meta:
        model = Sesion
        fields = [
            'id', 'usuario', 'lectura', 'estado', 'total_preguntas',
            'puntaje_total', 'puntajes_por_criterio', 'recomendaciones_ia',
            'tiempo_total_segundos', 'tiempo_restante_segundos',
            'fecha_fin_plazo',
            'fecha', 'fecha_inicio', 'fecha_fin', 'duracion_segundos',
            'skills_objetivo', 'preguntas', 'respuestas'
        ]
        read_only_fields = ['usuario', 'puntaje_total', 'fecha', 'fecha_inicio', 'fecha_fin', 'duracion_segundos']

    def get_preguntas(self, obj):
        queryset = obj.lectura.preguntas.order_by('orden')
        if obj.estado == 'COMPLETADA':
            return PreguntaSerializer(queryset, many=True).data
        return PreguntaPublicSerializer(queryset, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Calcular tiempo restante dinámicamente usando fecha_fin_plazo si está disponible
        fecha_fin_plazo = instance.fecha_fin_plazo
        if fecha_fin_plazo and instance.estado in ['INICIADA', 'EN_PROGRESO']:
            from django.utils import timezone
            remaining = int((fecha_fin_plazo - timezone.now()).total_seconds())
            data['tiempo_restante_segundos'] = max(0, remaining)
        else:
            # dejar el valor almacenado
            data['tiempo_restante_segundos'] = instance.tiempo_restante_segundos
        return data
