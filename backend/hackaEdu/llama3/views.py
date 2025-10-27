from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from alumnos.models import Alumno, Evaluacion
from alumnos.serializers import EvaluacionSerializer
import requests

class EvaluarAlumnoView(APIView):
    def post(self, request):
        try:
            rubrica = request.data.get("rubrica")
            respuesta_alumno = request.data.get("respuesta_alumno")

            if not rubrica or not respuesta_alumno:
                return Response({"error": "Faltan campos (rúbrica o respuesta_alumno)"}, status=400)

            # Prompt para el modelo Llama3
            prompt = f"""Evalúa la siguiente respuesta según la rúbrica dada:
            Rúbrica: {rubrica}
            Respuesta del alumno: {respuesta_alumno}
            Devuelve una evaluación breve con una puntuación de 1 a 10 y observaciones claras.
            """

            #  Llamada al modelo Llama3 (Ollama)
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code != 200:
                return Response({"error": "Error al comunicarse con el modelo Llama3"}, status=500)

            resultado_ia = response.json().get("response", "").strip()

            # Alumno por defecto (id=1)
            alumno = Alumno.objects.get(id=1)

            evaluacion = Evaluacion.objects.create(
                alumno=alumno,
                rubrica=rubrica,
                respuesta_alumno=respuesta_alumno,
                resultado_ia=resultado_ia
            )

            return Response({
                "mensaje": "Evaluación generada correctamente",
                "evaluacion": EvaluacionSerializer(evaluacion).data
            }, status=status.HTTP_201_CREATED)

        except Alumno.DoesNotExist:
            return Response({"error": "El alumno con id=1 no existe"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
