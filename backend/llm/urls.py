"""
LLM URLs - Rutas para endpoints de generación de contenido
"""

from django.urls import path
from .views import LLMViewSet

urlpatterns = [
    path('create-reading-with-questions/', 
         LLMViewSet.as_view({'post': 'create_reading_with_questions'}),
         name='create-reading-with-questions'),
]
