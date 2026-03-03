from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SesionViewSet

router = DefaultRouter()
router.register(r'sesiones', SesionViewSet, basename='sesion')

urlpatterns = [
    path('', include(router.urls)),
]
