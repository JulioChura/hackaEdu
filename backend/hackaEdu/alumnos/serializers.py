from rest_framework import serializers
from .models import Alumno, Evaluacion

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class EvaluacionSerializer(serializers.ModelSerializer):
    alumno = AlumnoSerializer(read_only=True)

    class Meta:
        model = Evaluacion
        fields = '__all__'
