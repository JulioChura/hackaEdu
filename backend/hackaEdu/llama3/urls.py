from django.urls import path
from .views import EvaluarAlumnoView

urlpatterns = [
    path('evaluar/', EvaluarAlumnoView.as_view(), name='evaluar_alumno'),
]
