from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ModalidadViewSet, LecturaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'modalidades', ModalidadViewSet, basename='modalidad')
router.register(r'lecturas', LecturaViewSet, basename='lectura')

urlpatterns = [
    path('', include(router.urls)),
]
