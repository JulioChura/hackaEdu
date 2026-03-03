from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogroViewSet

router = DefaultRouter()
router.register(r'', LogroViewSet, basename='logros')

urlpatterns = [
    path('', include(router.urls)),
]
