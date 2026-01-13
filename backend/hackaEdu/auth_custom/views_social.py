from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Redirige al usuario a Google para autenticación
    Frontend debe llamar: GET /api/auth/google/login/
    """
    # Redirigir a la URL de AllAuth para Google
    return redirect('/accounts/google/login/')




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_token(request):
    """
    Después de login con Google, el usuario es redirigido a Vue
    Vue llama este endpoint con la sesión de Django para obtener JWT tokens
    """
    user = request.user
    
    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    # Obtener datos de Google si existen
    google_data = None
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        google_data = {
            'google_id': social_account.uid,
            'picture': social_account.extra_data.get('picture'),
            'email': social_account.extra_data.get('email'),
        }
    except SocialAccount.DoesNotExist:
        pass
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'google_data': google_data
        }
    })
@api_view(['POST'])
@permission_classes([AllowAny])
def google_login_api(request):
    """
    Para login con Google desde API REST (usando token de Google)
    Frontend envía el token de Google que obtuvo del SDK de Google
    """
    google_token = request.data.get('token')
    
    if not google_token:
        return Response({'error': 'Token de Google requerido'}, status=400)
    
    # Aquí validarías el token con Google
    # Por ahora, esto es para login tradicional con redirect
    return Response({'detail': 'Use /api/auth/google/login/ para redirect flow'})
