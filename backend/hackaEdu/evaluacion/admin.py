from django.contrib import admin
from .models import Evaluacion, Pregunta, PreguntaCriterio, RespuestaAlumno

admin.site.register(Evaluacion)
admin.site.register(Pregunta)
admin.site.register(PreguntaCriterio)
admin.site.register(RespuestaAlumno)
