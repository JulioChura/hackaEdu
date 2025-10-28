from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class EvaluarAlumnoView(APIView):
    def post(self, request):
        try:
            rubrica = request.data.get("rubrica")
            respuesta_alumno = request.data.get("respuesta_alumno")

            if not rubrica or not respuesta_alumno:
                return Response({"error": "Faltan campos"}, status=400)

            prompt = f"""Evalúa según rúbrica: {rubrica}
            Respuesta: {respuesta_alumno}
            Devuelve evaluación con puntuación 1-10 y observaciones."""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                resultado_ia = response.json().get("response", "").strip()
                return Response({"resultado_ia": resultado_ia}, status=200)
            else:
                return Response({"error": "Error con Llama3"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)