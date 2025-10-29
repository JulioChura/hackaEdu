from django.contrib import admin
from .models import Docente, Curso, Sesion, Tema, CriterioEvaluacion, NivelDesempeno

admin.site.register(NivelDesempeno)
admin.site.register(Docente)
admin.site.register(Curso)
admin.site.register(Tema)
admin.site.register(Sesion)
admin.site.register(CriterioEvaluacion)
