"""
Views para app usuarios - Endpoints del dashboard
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .dashboard_service import DashboardService


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para endpoints del dashboard
    
    Devuelve exactamente la estructura que el frontend espera.
    Todos los nombres de campos coinciden con lo que el frontend espera.
    """
    permission_classes = [IsAuthenticated]
    
    # ENDPOINT: GET /usuarios/dashboard/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener datos básicos del estudiante autenticado"""
        data = DashboardService.get_student_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/progress/
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """Obtener datos de progreso del estudiante"""
        data = DashboardService.get_progress_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/streak/
    @action(detail=False, methods=['get'])
    def streak(self, request):
        """Obtener datos de racha del estudiante"""
        data = DashboardService.get_streak_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/active-courses/
    @action(detail=False, methods=['get'])
    def active_courses(self, request):
        """Obtener cursos activos (lecturas) del estudiante"""
        data = DashboardService.get_active_courses(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/ranking/
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        """Obtener datos de ranking del usuario"""
        data = DashboardService.get_ranking_data(request.user)
        return Response(data)
    
    # ENDPOINT: GET /usuarios/dashboard/achievements/
    @action(detail=False, methods=['get'])
    def achievements(self, request):
        """Obtener logros obtenidos por el usuario"""
        data = DashboardService.get_achievements_data(request.user)
        return Response(data)
    
    # ENDPOINT (BONUS): GET /usuarios/dashboard/full/
    @action(detail=False, methods=['get'])
    def full(self, request):
        """Obtener TODOS los datos del dashboard en una sola llamada"""
        data = DashboardService.get_full_dashboard(request.user)
        return Response(data)


