"""
VIEWS - Autenticación Social (Google OAuth)
=============================================
🔧 REUTILIZABLE EN OTROS PROYECTOS: Sí (con django-allauth)

Arquitectura de autenticación con Google OAuth:
  1. google_login():        Frontend → Redirige a Google
  2. [Callback automático]  Google envía usuario a Django (allauth)
  3. convert_token():       Frontend obtiene JWT tokens
  4. Signal post_save:      Crea datos iniciales automáticamente

Flujo de autenticación:
═══════════════════════════════════════════════════════════════
| Frontend          | Backend (Django)    | Google            |
├──────────────────┼──────────────────────┼───────────────────┤
| GET /api/auth/   | Redirige a Google    |                   |
| google/login/    | OAuth consent page   | Muestra formulario |
│                  │                      │                   |
|                  | ← Usuario autoriza ← |                   |
│                  │                      │                   |
|                  | AllAuth callback     |                   |
|                  | → Crea/actualiza user|                   |
|                  | → Signal dispara     |                   |
|                  | → Crea ProgresionNiv,|                   |
|                  |   RachaUsuario,      |                   |
|                  |   Ranking (si no    |                   |
|                  |   existen)           |                   |
│                  │                      │                   |
| GET /api/auth/   | Devuelve JWT tokens  |                   |
| convert-token/   | + datos del usuario  |                   |
│                  │                      │                   |
| Almacena JWT     |                      |                   |
| en localStorage  |                      |                   |
└──────────────────┴──────────────────────┴───────────────────┘

Dependencias requeridas:
  - django-allauth
  - djangorestframework-simplejwt
  - Configuración de Google OAuth en settings.py
"""

from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Reutilizable: Sí (requiere django-allauth)
    
    INICIO del flujo OAuth con Google.
    
    Flujo:
       1. Frontend hace GET a este endpoint
       2. Redirige al usuario a /accounts/google/login/ (AllAuth)
       3. AllAuth muestra la página de consentimiento de Google
       4. Usuario autoriza
       5. Google redirige de vuelta a AllAuth callback
       6. AllAuth crea/actualiza el usuario
       7. Signal post_save en signals.py crea datos iniciales
       8. Frontend debe llamar a convert_token() después
    
    Endpoint: GET /api/auth/google/login/
    Parámetros: ninguno
    Respuesta: Redirect a Google OAuth consent page
    
    Nota: AllAuth maneja automáticamente el callback y creación de usuario
    """
    # django-allauth ya tiene configurado el endpoint
    return redirect('/accounts/google/login/')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_token(request):
    """
    Reutilizable: Sí (requiere JWT tokens)
    
    Obtener JWT tokens y datos. Se llama DESPUÉS del login con Google.
    
    Qué sucede:
       1. Usuario ya está autenticado (por sesión Django)
       2. Este endpoint genera JWT tokens
       3. Retorna tokens + datos del usuario
       4. Frontend guarda tokens en localStorage
    
    Al llegar aquí:
       - Usuario fue creado por AllAuth (si es la primera vez)
       - Signal ya ejecutó y creó ProgresionNivel, RachaUsuario, Ranking
       - SocialAccount está creada con datos de Google
    
    Endpoint: GET /api/auth/convert-token/
    Autenticación: Requerido (sesión o JWT)
    Respuesta: {"access": JWT token, "refresh": JWT refresh, "user": {...}}
    
    Frontend debe:
       1. Hacer GET a google_login() → redirige a Google
       2. Después del callback → hacer GET a este endpoint
       3. Guardar tokens en localStorage
       4. Usar access token en headers: Authorization: Bearer <token>
    """
    user = request.user
    
    # Generar JWT tokens
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
    
    # IMPORTANTE: En este punto, el signal ya ejecutó y creó:
    #    - ProgresionNivel (nivel A1)
    #    - RachaUsuario (racha de días)
    #    - Ranking (entrada en ranking)
    
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
    ⚠️ NO IMPLEMENTADO (Mantener solo para referencia)
    
    📌 Reutilizable: Parcialmente
    
    Endpoint alternativo para login con token de Google directamente.
    Útil si el frontend captura el token de Google y lo envía al backend.
    
    Actualmente NO se usa en el proyecto (usando redirect flow).
    Se puede implementar si se necesita autenticación desde mobile apps
    o cuando el frontend usa Google SDK directamente.
    
    Flujo alternativo:
      1. Frontend usa Google SDK → obtiene token
      2. Frontend hace POST con token a este endpoint
      3. Backend valida token con Google
      4. Backend crea/autentica usuario
      5. Retorna JWT tokens
    
    Ventajas del redirect flow actual:
      - Más seguro (Google maneja la autenticación)
      - Menos código en backend
      - Compatible con allauth
    """
    google_token = request.data.get('token')
    
    if not google_token:
        return Response({'error': 'Token de Google requerido'}, status=400)
    
    # TODO: Implementar si se necesita
    return Response({'detail': 'Use /api/auth/google/login/ para redirect flow'})

