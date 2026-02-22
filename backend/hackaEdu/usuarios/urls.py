"""
URLs para app usuarios - Dashboard endpoints
Rutas para obtener datos del dashboard del estudiante
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardViewSet

# Registrar el ViewSet de Dashboard
router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
