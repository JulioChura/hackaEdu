from django.urls import path
from .views import evaluar_respuestas, verificar_ia, prueba_prompt

urlpatterns = [
    path('evaluar-respuestas/', evaluar_respuestas, name='evaluar_respuestas'),
    path('verificar-ia/', verificar_ia, name='verificar_ia'),
    path('prueba-prompt/', prueba_prompt, name='prueba_prompt'),
]
