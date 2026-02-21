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

