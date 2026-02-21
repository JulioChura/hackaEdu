from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ModalidadViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'modalidades', ModalidadViewSet, basename='modalidad')

urlpatterns = [
    path('', include(router.urls)),
]
