"""
LLM URLs - Rutas para endpoints de generación de contenido
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LLMViewSet

router = DefaultRouter()
router.register('', LLMViewSet, basename='llm')

urlpatterns = [
    path('', include(router.urls)),
]
