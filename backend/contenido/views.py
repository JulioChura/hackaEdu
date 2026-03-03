from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Modalidad, Lectura, Pregunta
from .serializers import CategoriaSerializer, ModalidadSerializer, LecturaSerializer, PreguntaSerializer


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Categorías (solo lectura)
    
    Endpoints:
      - GET /contenido/categorias/ - Listar todas las categorías
      - GET /contenido/categorias/{codigo}/ - Obtener una categoría específica
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]  # Acceso público para que el registro pueda ver categorías


class ModalidadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Modalidades (solo lectura)
    
    Endpoints:
      - GET /contenido/modalidades/ - Listar todas las modalidades
      - GET /contenido/modalidades/{codigo}/ - Obtener una modalidad específica
    """
    queryset = Modalidad.objects.filter(activa=True)
    serializer_class = ModalidadSerializer
    permission_classes = [permissions.AllowAny]


class LecturaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Lecturas (solo lectura)

    Endpoints:
      - GET /contenido/lecturas/ - Listar lecturas publicadas
      - GET /contenido/lecturas/{id}/ - Obtener detalle de lectura
      - GET /contenido/lecturas/mias/ - Listar lecturas del usuario autenticado
    """

    serializer_class = LecturaSerializer

    def get_queryset(self):
        queryset = Lectura.objects.select_related('categoria', 'modalidad', 'nivel_cefr', 'usuario_creador')

        if self.action == 'mias':
            return queryset.filter(usuario_creador=self.request.user)

        return queryset.filter(publicada=True)

    def get_permissions(self):
        if self.action == 'mias':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'])
    def mias(self, request):
        """Obtiene las lecturas creadas por el usuario autenticado."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

