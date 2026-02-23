from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import SesionDetailSerializer
from .session_service import SessionService


class SesionViewSet(viewsets.ViewSet):
	"""Gestion de sesiones de lectura con estado y reanudacion."""

	permission_classes = [IsAuthenticated]

	def retrieve(self, request, pk=None):
		sesion = SessionService.obtener_sesion(request.user, pk)
		if not sesion:
			return Response({'detail': 'Sesion no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
		return Response(SesionDetailSerializer(sesion).data)

	@action(detail=False, methods=['post'])
	def iniciar(self, request):
		lectura_id = request.data.get('lectura_id')
		skills_objetivo = request.data.get('skills_objetivo', [])
		tiempo_total = request.data.get('tiempo_total_segundos', 900)
		if not lectura_id:
			return Response({'detail': 'lectura_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

		sesion, error = SessionService.iniciar_sesion(
			request.user,
			lectura_id,
			skills_objetivo,
			tiempo_total
		)
		if error == 'LECTURA_NO_ENCONTRADA':
			return Response({'detail': 'Lectura no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

		return Response(SesionDetailSerializer(sesion).data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['get'])
	def estado(self, request):
		lectura_id = request.query_params.get('lectura_id')
		if not lectura_id:
			return Response({'detail': 'lectura_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

		return Response(SessionService.obtener_estado(request.user, lectura_id))

	@action(detail=True, methods=['patch'])
	def guardar(self, request, pk=None):
		respuestas = request.data.get('respuestas', [])
		tiempo_restante = request.data.get('tiempo_restante_segundos')

		sesion, error = SessionService.guardar_progreso(
			request.user,
			pk,
			respuestas,
			tiempo_restante
		)
		if error == 'SESION_NO_ENCONTRADA':
			return Response({'detail': 'Sesion no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
		if error == 'SESION_COMPLETADA':
			return Response({'detail': 'La sesion ya fue completada.'}, status=status.HTTP_409_CONFLICT)

		return Response(SesionDetailSerializer(sesion).data)

	@action(detail=True, methods=['post'])
	def finalizar(self, request, pk=None):
		respuestas = request.data.get('respuestas', [])
		tiempo_restante = request.data.get('tiempo_restante_segundos')

		sesion, error = SessionService.finalizar_sesion(
			request.user,
			pk,
			respuestas,
			tiempo_restante
		)
		if error == 'SESION_NO_ENCONTRADA':
			return Response({'detail': 'Sesion no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

		return Response(SesionDetailSerializer(sesion).data)
