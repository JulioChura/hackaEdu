from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    RegisterSerializer,
    ChangePasswordSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Endpoint personalizado para obtener tokens JWT"""
    permission_classes = (AllowAny,)


class RegisterView(generics.CreateAPIView):
    """Endpoint para registrar un nuevo usuario"""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Generar tokens automáticamente después del registro
        user = CustomUser.objects.get(email=response.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Los usuarios solo ven sus propios datos"""
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Obtener perfil del usuario autenticado"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Actualizar perfil del usuario autenticado"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario autenticado"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout del usuario (en cliente-servidor, JWT se elimina en frontend)"""
        return Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)

