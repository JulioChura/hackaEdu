from django.urls import path
from .views import (
    EvaluarAlumnoView,
    evaluar_respuestas,
    verificar_ia,
    prueba_prompt
)

urlpatterns = [
    # Endpoint principal - evaluación completa con IA
    path('evaluar-respuestas/', evaluar_respuestas, name='evaluar_respuestas'),
    
    # Endpoint de verificación - check de Ollama
    path('verificar-ia/', verificar_ia, name='verificar_ia'),
    
    # Endpoint de prueba - generar prompt sin ejecutar IA
    path('prueba-prompt/', prueba_prompt, name='prueba_prompt'),
    
    # Legacy - compatibilidad
    path('evaluar/', EvaluarAlumnoView.as_view(), name='evaluar_alumno'),
]
